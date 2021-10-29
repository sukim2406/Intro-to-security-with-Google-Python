from json_logic import jsonLogic
from statistics import mean
from enum import Enum, IntEnum
import random
import pandas as pd
import matplotlib.pyplot as plt

class Const(str, Enum):
    PASS = "Y"
    FAIL = "N"


class LearningConfig(IntEnum):
    RULE_CURRENT_SCORE = 70
    RULE_MEAN = 50
    RULE_FREE_PASS_SCORE = 90


def check_exam_list(score_list):
    rule = {"or":
                [{"and":
                    [{">=": [{"var": "current_score"},
                        LearningConfig.RULE_CURRENT_SCORE]},
                    {">=": [{"var": "mean"},
                        LearningConfig.RULE_MEAN]}]},
                {">=": [{"var": "current_score"},
                    LearningConfig.RULE_FREE_PASS_SCORE]}]
    }

    exam_dict = {}
    exam_dict["current_score"] = score_list[1]
    exam_dict["mean"] = score_list[2]

    rule_result = jsonLogic(rule,exam_dict)

    if rule_result:
        return Const.PASS.value
    else:
        return Const.FAIL.value

def make_random_numbers(previous_min, previous_max, current_min, current_max, sample_number):
    my_set = set()

    while 1:
        previous_score = random.randint(previous_min, previous_max)
        current_score = random.randint(current_min, current_max)
        score_mean = mean([previous_score, current_score])
        my_set.add(tuple([previous_score, current_score, score_mean]))

        if len(my_set) == sample_number:
            break
    
    random_list = [list(x) for x in my_set]

    for index, item in enumerate(random_list):
        result = check_exam_list(item)
        item.insert(0, result)

    return random_list


random_set = make_random_numbers(0, 100, 0, 100, 5000)
sample_dataframe = pd.DataFrame.from_records(random_set)

sample_dataframe.loc[sample_dataframe[0]=="N", 0] = "red"
sample_dataframe.loc[sample_dataframe[0]=="Y", 0] = "yellow"

sample_dataframe.columns = ["result", "previous_score", "current_score", "mean"]

print(sample_dataframe.head(3))

ax1 = sample_dataframe.plot.scatter(x="previous_score", y="current_score", c="result", colormap="viridis")
ax1.set_title("Rule based")
plt.show()