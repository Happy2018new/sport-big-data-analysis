import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path
from typing import Any


class ColumnConfig:
    COLUMN_MAPPING: dict[str, str] = {
        "Country": "country",
        "Year": "year",
        "Status": "status",
        "Life expectancy": "life_expectancy",
        "Adult Mortality": "adult_mortality",
        "infant deaths": "infant_deaths",
        "Alcohol": "alcohol",
        "percentage expenditure": "percentage_expenditure",
        "Hepatitis B": "hepatitis_b",
        "Measles": "measles",
        "BMI": "bmi",
        "under-five deaths": "under_five_deaths",
        "Polio": "polio",
        "Total expenditure": "total_expenditure",
        "Diphtheria": "diphtheria",
        "HIV/AIDS": "hiv_aids",
        "GDP": "gdp",
        "Population": "population",
        "thinness  1-19 years": "thinness_1_19_years",
        "thinness 5-9 years": "thinness_5_9_years",
        "Income composition of resources": "income_composition_of_resources",
        "Schooling": "schooling",
    }
    INTEGER_COLUMNS: tuple[str, ...] = (
        "year",
        "adult_mortality",
        "infant_deaths",
        "hepatitis_b",
        "measles",
        "under_five_deaths",
        "polio",
        "diphtheria",
        "population",
    )
    ALL_COLUMNS: tuple[str, ...] = tuple(COLUMN_MAPPING.values())
    ZERO_AS_MISSING_COLUMNS: tuple[str, ...] = (
        "income_composition_of_resources", "schooling", "percentage_expenditure",
    )
    SECOND_ROUND_DROP_COLUMNS: tuple[str, ...] = ("gdp", "population", "bmi")


class ValidationRules:
    STATUS_VALUES: set[str] = {"Developed", "Developing"}
    VALUE_RANGES: dict[str, tuple[int, int | None]] = {
        "year": (2000, 2015),
        "life_expectancy": (0, 150),
        "adult_mortality": (0, 1000),
        "infant_deaths": (0, 1000),
        "alcohol": (0, None),
        "percentage_expenditure": (0, 1000),
        "hepatitis_b": (0, 100),
        "measles": (0, 1000),
        "bmi": (0, None),
        "under_five_deaths": (0, 1000),
        "polio": (0, 100),
        "total_expenditure": (0, 100),
        "diphtheria": (0, 100),
        "hiv_aids": (0, 1000),
        "gdp": (0, None),
        "population": (0, None),
        "thinness_1_19_years": (0, 100),
        "thinness_5_9_years": (0, 100),
        "income_composition_of_resources": (0, 1),
        "schooling": (0, 150),
    }


class PlotConfig:
    BOX_GROUPS: dict[str, tuple[str, ...]] = {
        "寿命与疾病": (
            "life_expectancy", "adult_mortality", "infant_deaths",
            "under_five_deaths", "measles", "hiv_aids",
        ),
        "健康行为与卫生服务": (
            "alcohol", "percentage_expenditure", "hepatitis_b", "bmi",
            "polio", "total_expenditure", "diphtheria",
        ),
        "社会经济与营养": (
            "gdp", "population", "thinness_1_19_years", "thinness_5_9_years",
            "income_composition_of_resources", "schooling",
        ),
    }
    STYLE: dict[str, Any] = {
        "font.family": ["Latin Modern Math", "SimSun"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
    }


def load_data(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = Path(__file__).with_name("寿命数据.csv")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df.rename(columns=ColumnConfig.COLUMN_MAPPING)


def is_missing(value: object) -> bool:
    if pd.isna(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def check_value(column: str, value: Any) -> tuple[Any, bool]:
    if is_missing(value):
        return value, True
    if column == "country":
        return value, isinstance(value, str)
    if column == "status":
        return value, isinstance(value, str) and value in ValidationRules.STATUS_VALUES
    if isinstance(value, (bool, np.bool_)):
        return value, False
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number) or not np.isfinite(number):
        return value, False

    if column == "population" and number >= 0 and number % 1 != 0:
        integer_part = math.floor(number)
        if number - integer_part >= 0.5:
            integer_part += 1
        number = integer_part
        value = number

    if column in ColumnConfig.INTEGER_COLUMNS and number % 1 != 0:
        return value, False
    lower, upper = ValidationRules.VALUE_RANGES[column]
    return value, bool(number >= lower and (upper is None or number <= upper))


def drop_problem_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    for column in ColumnConfig.ALL_COLUMNS:
        if column not in df.columns:
            raise ValueError(f"缺少必需列：{column}")

    prepared_df = df.copy()
    population_column = df.columns.get_loc("population")
    keep_positions: list[int] = []
    removed_counts: dict[str, int] = {column: 0 for column in ColumnConfig.ALL_COLUMNS}

    for position in range(len(df)):
        row = df.iloc[position]
        row_has_problem = False
        for column in ColumnConfig.ALL_COLUMNS:
            value = row[column]
            if is_missing(value):
                continue
            checked_value, valid = check_value(column, value)
            if column == "population" and checked_value != value:
                prepared_df.iloc[position, population_column] = checked_value
            if not valid:
                removed_counts[column] += 1
                row_has_problem = True
        if not row_has_problem:
            keep_positions.append(position)

    return prepared_df.iloc[keep_positions].copy(), removed_counts


def find_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """对清理后的数值指标逐列忽略缺失值，统计离群值。"""
    results: list[dict[str, str | int | float]] = []
    for column in ValidationRules.VALUE_RANGES:
        if column == "year":
            continue
        values = pd.to_numeric(df[column], errors="coerce").dropna()
        q1 = float(values.quantile(0.25)) if len(values) else np.nan
        q3 = float(values.quantile(0.75)) if len(values) else np.nan
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outlier_count = 0
        for value in values:
            if value < lower or value > upper:
                outlier_count += 1
        percentage = outlier_count / len(values) * 100 if len(values) else np.nan
        results.append(
            {
                "字段": column,
                "非缺失数量": len(values),
                "下四分位数": q1,
                "上四分位数": q3,
                "四分位距": iqr,
                "下界": lower,
                "上界": upper,
                "离群值数量": outlier_count,
                "离群值比例（%）": percentage,
            }
        )
    return pd.DataFrame(results)


def plot_boxplot_group(
    df: pd.DataFrame, columns: tuple[str, ...], output_path: Path
) -> None:
    """六个字段排成两行各三个，七个字段排成上三下四。"""
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(12, 7))
        for index, column in enumerate(columns):
            if len(columns) == 7 and index >= 3:
                plt.subplot(2, 4, index + 2)
            else:
                plt.subplot(2, 3, index + 1)
            values = pd.to_numeric(df[column], errors="coerce").dropna()
            plt.boxplot(values)
            plt.title(column, fontsize=11)
            plt.xticks([])
        plt.subplots_adjust(wspace=0.35, hspace=0.3)
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_outlier_counts(df: pd.DataFrame, output_path: Path) -> None:
    """按离群值数量降序绘制堆叠条形图，缺失值不参与统计。"""
    report = find_outliers_iqr(df)
    report = report.sort_values("离群值数量", ascending=False)
    outlier_counts = report["离群值数量"]
    non_outlier_counts = report["非缺失数量"] - outlier_counts

    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(14, 10))
        plt.barh(report["字段"], non_outlier_counts, color="#497f72", label="非离群值")
        plt.barh(report["字段"], outlier_counts, left=non_outlier_counts, color="#d88b67", label="离群值")
        for position, (non_outlier, outlier) in enumerate(zip(non_outlier_counts, outlier_counts)):
            if non_outlier:
                plt.text(non_outlier / 2, position, str(non_outlier), ha="center", va="center", color="white")
            plt.text(len(df) + max(len(df), 1) * 0.015, position, f"离群值：{outlier}", va="center")
        plt.gca().invert_yaxis()
        plt.title("各字段离群值与非离群值数量", fontsize=16, pad=50)
        plt.xlabel("记录数量")
        plt.ylabel("字段")
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2)
        plt.grid(axis="x", alpha=0.25)
        plt.gca().set_axisbelow(True)
        plt.xlim(0, max(len(df), 1) * 1.18)
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_missing_pie(df: pd.DataFrame, output_path: Path) -> None:
    """对第二轮处理后的数据绘制各字段缺失数量的占比。"""
    missing_counts = df.isna().sum()
    missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=False)
    total_missing = int(missing_counts.sum())
    if total_missing == 0:
        print("当前数据没有缺失值，无需绘制饼图。")
        return

    labels: list[str] = []
    for column, count in missing_counts.items():
        percentage = count / total_missing * 100
        labels.append(f"{column}：{count}（{percentage:.1f}%）")

    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(12, 7))
        plt.pie(missing_counts, startangle=90, colors=plt.cm.tab20.colors,
                wedgeprops={"edgecolor": "white"})
        plt.title("各字段缺失值占比")
        plt.legend(labels, loc="center left",
                   bbox_to_anchor=(1, 0.5), fontsize=10)
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_missing_fill_counts(report: pd.DataFrame, output_path: Path) -> None:
    """用堆叠条形图展示每个字段的缺失值如何处理。"""
    report = report.sort_values("处理前缺失", ascending=False)
    country_counts = report["同国填补"]
    status_counts = report["同类国家填补"]
    removed_counts = report["随记录排除"]
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(12, 8))
        plt.barh(report["字段"], country_counts, color="#497f72", label="本国统计量填补")
        plt.barh(report["字段"], status_counts, left=country_counts,
                 color="#638cac", label="同类国家统计量填补")
        plt.barh(report["字段"], removed_counts, left=country_counts + status_counts,
                 color="#c87c53", label="随寿命缺失记录排除")
        for position, count in enumerate(report["处理前缺失"]):
            plt.text(count + 5, position, str(count), va="center")
        plt.gca().invert_yaxis()
        plt.title("各字段缺失值处理数量", pad=40)
        plt.xlabel("缺失单元格数量")
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=3, fontsize=9)
        plt.grid(axis="x", alpha=0.25)
        plt.gca().set_axisbelow(True)
        plt.xlim(0, report["处理前缺失"].max() * 1.12)
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_data_quality(
    df: pd.DataFrame, output_dir: str | Path | None = None
) -> tuple[list[Path], Path]:
    """保存三张分组箱线图及离群值数量堆叠图。"""
    output_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().with_name("figures")
    boxplot_dir = output_dir / "箱线图"
    boxplot_dir.mkdir(parents=True, exist_ok=True)
    boxplot_paths: list[Path] = []
    for title, columns in PlotConfig.BOX_GROUPS.items():
        path = boxplot_dir / f"{title}.svg"
        plot_boxplot_group(df, columns, path)
        boxplot_paths.append(path)
    outlier_path = output_dir / "离群值数量.svg"
    plot_outlier_counts(df, outlier_path)
    return boxplot_paths, outlier_path


if __name__ == "__main__":
    original_df = load_data()
    df, report = drop_problem_rows(original_df)
    print(f"原始行数：{len(original_df)}")
    print(f"删除行数：{len(original_df) - len(df)}")
    print(f"剩余行数：{len(df)}")
    print("各字段不合格行数：")
    for column, count in report.items():
        print(f"{column}：{count}")

    outlier_report = find_outliers_iqr(df)
    print("\n各字段离群值统计：")
    print(
        outlier_report.to_string(
            index=False, float_format="{:.2f}".format, na_rep="无数据"
        )
    )

    boxplot_paths, outlier_path = plot_data_quality(df)
    print("\n三张分组箱线图已保存：")
    for path in boxplot_paths:
        print(path)
    print(f"离群值数量图已保存：{outlier_path}")
