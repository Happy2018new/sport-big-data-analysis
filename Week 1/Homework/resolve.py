import numpy as np
import pandas as pd
from dataclasses import dataclass
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

CONST_GROUP_DATA = {
    "专家组": ["祁中海", "蹇子欣", "苏艳", "员阳"],
    "学生组": ["革政君", "吾宇旗义轩", "迮静怡", "邴中海"],
    "家长组": ["陈依诺", "出英", "介义轩", "裴丽芳"],
}


@dataclass
class AnovaResult:
    f_value: float
    p_value: float
    df_between: int
    df_within: int

    def __repr__(self) -> str:
        result = ""

        result += f"检验 F 值\t{self.f_value}\n"
        result += f"检验 P 值\t{self.p_value}\n"
        result += f"组间自由度\t{self.df_between}\n"
        result += f"组内自由度\t{self.df_within}\n"

        if self.p_value < 0.05:
            result += "检验结论\t至少存在一组之间具有显著差异"
        else:
            result += "检验结论\t各组之间不存在显著差异"

        return result


def resolve_problem_one(
    data: pd.DataFrame, group: dict[str, list[str]]
) -> tuple[pd.Series, pd.Series]:
    mean_for_each_person = pd.Series()
    mean_for_each_group = pd.Series()
    std_for_each_group = pd.Series()

    for _, value in group.items():
        for i in value:
            mean_for_each_person[i] = np.mean(
                data[i].eq(data["真实结果"]),
            )
    for index, value in group.items():
        mean_for_each_group[index] = mean_for_each_person[value].mean()
        std_for_each_group[index] = mean_for_each_person[value].std()

    return mean_for_each_group, std_for_each_group


def resolve_problem_two(
    data: pd.DataFrame, group: dict[str, list[str]]
) -> tuple[pd.DataFrame, AnovaResult]:
    df = pd.DataFrame(columns=["人员", "组别", "图片", "判断准确率"])

    for index, value in group.items():
        for i in value:
            temp = data[i].eq(data["真实结果"])
            mean = temp.groupby(data["图片"]).mean()
            for image_id, accuracy in mean.items():
                df.loc[len(df)] = [
                    i,
                    index,
                    image_id,
                    accuracy,
                ]

    sub1 = df.loc[df["组别"] == "专家组", "判断准确率"]
    sub2 = df.loc[df["组别"] == "学生组", "判断准确率"]
    sub3 = df.loc[df["组别"] == "家长组", "判断准确率"]
    f_value, p_value = f_oneway(sub1, sub2, sub3)

    return df, AnovaResult(
        f_value=f_value,
        p_value=p_value,
        df_between=len(group) - 1,
        df_within=len(df) - len(group),
    )


path = input("请输入 作业1.csv 文件路径: ")
try:
    data = pd.read_csv(path)
    print()
except FileNotFoundError:
    print("文件未找到，请检查路径是否正确。")
    exit()

mean_for_each_group, std_for_each_group = resolve_problem_one(data, CONST_GROUP_DATA)
print("—————————— 每组均值 ——————————")
print(mean_for_each_group)
print()
print("—————————— 每组标准差 ——————————")
print(std_for_each_group)
print()

df, result = resolve_problem_two(data, CONST_GROUP_DATA)
print("—————————— 单因素分析结果 ——————————")
print(result)
print()

if result.p_value < 0.05:
    print("—————————— 多重比较结果 ——————————")
    print(
        pairwise_tukeyhsd(
            endog=df["判断准确率"],
            groups=df["组别"],
            alpha=0.05,
        )
    )
