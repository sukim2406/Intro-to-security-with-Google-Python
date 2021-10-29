from sys import _current_frames
from json_logic import jsonLogic
from statistics import mean
from enum import Enum, IntEnum
import random
import pandas as pd
from sklearn.cluster import KMeans
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

    rule_result = jsonLogic(rule, exam_dict)

    if rule_result:
        return Const.PASS.value
    else:
        return Const.FAIL.value
    
def make_random_numbers(min, max, sample_number):
    my_set = set()

    while 1:
        previous_score = random.randint(min, max)
        current_score = random.randint(min, max)
        score_mean = mean([previous_score, current_score])
        my_set.add(tuple([previous_score, current_score, score_mean]))

        if len(my_set) == sample_number:
            break
    
    random_list = [list(x) for x in my_set]

    for index, item in enumerate(random_list):
        result = check_exam_list(item)
        item.insert(0, result)

    return random_list

random_set1 = make_random_numbers(0, 100, 5000)
random_set2 = make_random_numbers(200, 300, 100)
random_set = random_set1 + random_set2

ml_df = pd.DataFrame.from_records(random_set)

ml_df.loc[ml_df[0] == "N", 0] = "red"
ml_df.loc[ml_df[0] == "Y", 0] = "yellow"
ml_df.columns = ["result", "previous_score", "current_score", "mean"]
ml_df.drop(["result", "mean"], axis=1, inplace=True)

print(ml_df.head(3))

model = KMeans(n_clusters=2, algorithm='auto')
model.fit(ml_df)

predict = pd.DataFrame(model.predict(ml_df))
predict.columns = ["predict"]

final_df = pd.concat([ml_df, predict], axis=1)

ax1=final_df.plot.scatter(x="previous_score", y="current_score", c="predict", colormap="viridis")
ax1.set_title("KMean")

plt.show()