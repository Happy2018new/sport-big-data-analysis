from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from prepare import (
    ColumnConfig, PlotConfig, drop_problem_rows, load_data,
    plot_missing_pie, plot_missing_fill_counts,
)


class FillConfig:
    METHODS: dict[str, str] = {
        "alcohol": "median",
        "percentage_expenditure": "median",
        "hepatitis_b": "median",
        "polio": "median",
        "total_expenditure": "median",
        "diphtheria": "median",
        "thinness_1_19_years": "median",
        "thinness_5_9_years": "median",
        "income_composition_of_resources": "mean",
        "schooling": "mean",
    }


def clean_second_round(df: pd.DataFrame) -> pd.DataFrame:
    """删除三个不可靠字段，并将指定字段的零值替换为缺失值。"""
    cleaned_df = df.drop(columns=list(ColumnConfig.SECOND_ROUND_DROP_COLUMNS)).copy()
    for column in ColumnConfig.ZERO_AS_MISSING_COLUMNS:
        cleaned_df[column] = cleaned_df[column].replace(0, np.nan)
    return cleaned_df


def fill_missing_values(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """排除寿命缺失行，再按国家、status 的统计量补全分析数据。"""
    filled_df = df.dropna(subset=["life_expectancy"]).copy()
    report = df.isna().sum().to_frame("处理前缺失")
    report.index.name = "字段"
    report["随记录排除"] = report["处理前缺失"] - filled_df.isna().sum()
    report["同国填补"] = 0
    report["同类国家填补"] = 0

    for column, method in FillConfig.METHODS.items():
        missing = filled_df[column].isna()
        # 两种统计量都来自填补前的有效记录。
        country_values = filled_df.groupby("country")[column].transform(method)
        status_values = filled_df.groupby("status")[column].transform(method)
        filled_df[column] = filled_df[column].fillna(country_values)
        remaining = int(filled_df[column].isna().sum())
        report.loc[column, "同国填补"] = int(missing.sum()) - remaining
        filled_df[column] = filled_df[column].fillna(status_values)
        report.loc[column, "同类国家填补"] = remaining - int(filled_df[column].isna().sum())
        if column in ColumnConfig.INTEGER_COLUMNS:
            filled_df.loc[missing, column] = np.floor(filled_df.loc[missing, column] + 0.5)

    report["剩余缺失"] = filled_df.isna().sum()
    report = report[report["处理前缺失"] > 0].reset_index()
    return filled_df, report


def plot_bmi_lines(df: pd.DataFrame, output_path: Path) -> None:
    """用四个国家的年度折线展示 bmi 数值的异常变化。"""
    countries = {
        "United States of America": "美国",
        "Haiti": "海地",
        "Sierra Leone": "塞拉利昂",
        "Viet Nam": "越南",
    }
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(12, 8))
        for index, (country, name) in enumerate(countries.items(), start=1):
            country_data = df[df["country"] == country].sort_values("year")
            # 被剔除的年份留为空值，折线在这些位置自动断开。
            bmi = country_data.set_index("year")["bmi"].reindex(range(2000, 2016))
            plt.subplot(2, 2, index)
            plt.plot(bmi.index, bmi, marker="o")
            plt.title(name)
            plt.xlabel("年份")
            plt.ylabel("bmi")
            plt.xticks([2000, 2005, 2010, 2015])
            plt.xlim(1999.5, 2015.5)
            plt.grid(alpha=0.3)
        plt.suptitle("首轮清理后各国 bmi 年度记录")
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_zero_values(df: pd.DataFrame, output_path: Path) -> None:
    """用四张柱状子图展示零值疑似缺失的依据。"""
    examples = [
        ("income_composition_of_resources", "Grenada", "格林纳达", "2000至2010年均为0"),
        ("schooling", "Montenegro", "黑山", "2000至2003年均为0"),
    ]
    years = range(2000, 2016)
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(14, 9))
        for index, (column, country, name, note) in enumerate(examples, start=1):
            country_data = df[df["country"] == country].sort_values("year")
            values = country_data.set_index("year")[column].reindex(years)
            plt.subplot(2, 2, index)
            plt.bar(values.index, values, color="#497f72")
            plt.text(2000, values.max() * 0.08, note, fontsize=10)
            plt.title(f"{name}：{column}", fontsize=11)
            plt.xlabel("年份")
            plt.ylabel("记录值")
            plt.xticks([2000, 2005, 2010, 2015])
            plt.xlim(1999.5, 2015.5)
            plt.ylim(bottom=0)
            plt.grid(axis="y", alpha=0.3)
            plt.gca().set_axisbelow(True)

        zero_rates: list[float] = []
        gdp_missing_rates: list[float] = []
        expenditure_missing_rates: list[float] = []
        # 各年保留行数不同，使用比例比较，而不是直接比较数量。
        for year in years:
            year_data = df[df["year"] == year]
            zero_rates.append((year_data["percentage_expenditure"] == 0).sum() / len(year_data) * 100)
            gdp_missing_rates.append(year_data["gdp"].isna().sum() / len(year_data) * 100)
            expenditure_missing_rates.append(year_data["total_expenditure"].isna().sum() / len(year_data) * 100)
        plt.subplot(2, 2, 3)
        positions = np.arange(2000, 2016)
        plt.bar(positions - 0.25, zero_rates, width=0.25, color="#c87c53", label="percentage_expenditure 为零")
        plt.bar(positions, gdp_missing_rates, width=0.25, color="#638cac", label="gdp 缺失")
        plt.bar(positions + 0.25, expenditure_missing_rates, width=0.25, color="#779a70", label="total_expenditure 缺失")
        plt.title("各年零值与缺失值占比", fontsize=11)
        plt.xlabel("年份")
        plt.ylabel("占当年保留记录的比例（%）")
        plt.xticks([2000, 2003, 2006, 2009, 2012, 2015])
        plt.xlim(1999.5, 2015.5)
        plt.ylim(0, 105)
        plt.legend(loc="upper left", fontsize=9)
        plt.grid(axis="y", alpha=0.3)
        plt.gca().set_axisbelow(True)

        values_2015 = df.loc[df["year"] == 2015, "percentage_expenditure"].dropna()
        zero_count = int((values_2015 == 0).sum())
        nonzero_count = int((values_2015 != 0).sum())
        plt.subplot(2, 2, 4)
        counts = [zero_count, nonzero_count]
        plt.bar(["零值", "非零值"], counts, color=["#c87c53", "#497f72"], width=0.6)
        for position, count in enumerate(counts):
            plt.text(position, count + 2, str(count), ha="center")
        plt.title(f"2015年 percentage_expenditure（共{len(values_2015)}条非缺失记录）", fontsize=11)
        plt.ylabel("记录数量")
        plt.ylim(0, max(counts) * 1.12)
        plt.grid(axis="y", alpha=0.3)
        plt.gca().set_axisbelow(True)
        plt.suptitle("首轮清理后零值疑似缺失的证据")
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_magnitude_scatter(df: pd.DataFrame, output_path: Path) -> None:
    """用四张散点子图展示 gdp 和 population 的数量级突变。"""
    examples = [
        ("gdp", "Mauritius", "毛里求斯", "美元"),
        ("gdp", "Rwanda", "卢旺达", "美元"),
        ("population", "South Africa", "南非", "人"),
        ("population", "Hungary", "匈牙利", "人"),
    ]
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(12, 8))
        for index, (column, country, name, unit) in enumerate(examples, start=1):
            country_data = df[df["country"] == country].sort_values("year")
            plt.subplot(2, 2, index)
            plt.scatter(country_data["year"], country_data[column], color="#638cac", s=35)
            plt.yscale("log")
            plt.title(f"{name}：{column}")
            plt.xlabel("年份")
            plt.ylabel(f"{unit}（对数刻度）")
            plt.xticks([2000, 2005, 2010, 2015])
            plt.xlim(1999.5, 2015.5)
            plt.grid(alpha=0.3)
        plt.suptitle("首轮清理后 gdp 与 population 的年度记录")
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    df, _ = drop_problem_rows(load_data())
    output_dir = Path(__file__).resolve().parent / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_bmi_lines(df, output_dir / "bmi折线图.svg")
    plot_zero_values(df, output_dir / "零值疑似缺失.svg")
    plot_magnitude_scatter(df, output_dir / "数量级异常.svg")
    print(f"三张问题说明图已保存至：{output_dir}")

    df = clean_second_round(df)
    print("第二轮处理：已删除 gdp、population、bmi，指定字段的零值已替换为缺失值。")
    print(f"剩余行数：{len(df)}，剩余字段数：{len(df.columns)}")
    missing_path = output_dir / "缺失值占比.svg"
    plot_missing_pie(df, missing_path)
    print(f"缺失值占比饼图已保存：{missing_path}")

    filled_df, fill_report = fill_missing_values(df)
    print("\n缺失值处理统计：")
    print(fill_report.to_string(index=False))
    print(f"排除寿命缺失记录：{len(df) - len(filled_df)}行")
    print(f"补全后行数：{len(filled_df)}，剩余缺失值：{int(filled_df.isna().sum().sum())}")
    fill_path = output_dir / "缺失值处理数量.svg"
    plot_missing_fill_counts(fill_report, fill_path)
    print(f"缺失值处理数量图已保存：{fill_path}")
    data_path = Path(__file__).resolve().with_name("寿命数据_补全.csv")
    filled_df.to_csv(data_path, index=False, encoding="utf-8-sig")
    print(f"补全后的分析数据已保存：{data_path}")
