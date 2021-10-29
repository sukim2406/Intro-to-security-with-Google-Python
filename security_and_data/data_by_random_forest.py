from json_logic import jsonLogic
from statistics import mean
from enum import Enum, IntEnum
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class Const(str, Enum):
    PASS = "Y"
    FAIL = "N"
    TRAINING_BY_ALL = "TA"
    TRAINING_BY_LOW_SAMPLE = "TL"
    TRAINING_BY_PREVIOUS_AND_MEAN = "TPM"
    TRAINING_BY_CURRENT = "TC"
    TRAINING_BY_PREVIOUS = "TP"
    TRAINING_BY_MISSING_DATA = "TM" 


class LearningConfig(IntEnum):
    RULE_CURRENT_SCORE = 70
    RULE_MEAN = 50
    RULE_FREE_PASS_SCORE = 90
    LOW_SAMPLE = 10
    ENOUGH_SAMPLE = 5000


test_mode = Const.TRAINING_BY_LOW_SAMPLE.value

def check_exam_list(score_list):
    rule = {"or":
                [{"and" : 
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

if test_mode == Const.TRAINING_BY_LOW_SAMPLE:
    random_set = make_random_numbers(0, 100, 0, 100, LearningConfig.LOW_SAMPLE)
else:
    random_set = make_random_numbers(0, 100, 0, 100, LearningConfig.ENOUGH_SAMPLE)

ml_df = pd.DataFrame.from_records(random_set)

ml_df.loc[ml_df[0] == "N", 0] = "red"
ml_df.loc[ml_df[0] == "Y", 0] = "yellow"

ml_df.columns = ["result", "previous_score", "current_score", "mean"]
print(ml_df.head(3))

data = ml_df.iloc[:, 1:]
label = ml_df.iloc[:, 0]

data_train, data_test, label_train, label_test = train_test_split(data, label)

data_test_original = data_test.copy()

if test_mode == Const.TRAINING_BY_PREVIOUS_AND_MEAN:
    data_test = data_test.iloc[:, [0, 2]]
    data_train = data_train.iloc[:, [0, 2]]
elif test_mode == Const.TRAINING_BY_CURRENT:
    data_test = data_test.iloc[:, [1]]
    data_train = data_train.iloc[:, [1]]
elif test_mode == Const.TRAINING_BY_PREVIOUS:
    data_test = data_test.iloc[:, [0]]
    data_train = data_train.iloc[:, [0]]

model = RandomForestClassifier()

if test_mode == Const.TRAINING_BY_MISSING_DATA:
    ml_missing_df = ml_df.query('previous_score < 90 and current_score < 90')
    print(ml_missing_df.head(3))

    data_missing = ml_missing_df.iloc[:, 1:]
    label_missing = ml_missing_df.iloc[:, 0]

    data_missing_train, data_missing_test, label_missing_train, label_missing_test = train_test_split(data_missing, label_missing)

    model.fit(data_missing_train, label_missing_train)
else:
    model.fit(data_train, label_train)

predict = model.predict(data_test)
print("predict:" + str(predict))

accuracy_score = metrics.accuracy_score(label_test, predict)
classification_report = metrics.classification_report(label_test, predict)

print("Accuracy: ", accuracy_score)
print("Statistic: \n", classification_report)

axis1 = ml_df.plot.scatter(x="previous_score", y="current_score", c="result", colormap="viridis")
axis1.set_title("Rule based")
axis2 = data_test_original.plot.scatter(x="previous_score", y="current_score", c=predict, colormap="viridis")
axis2.set_title("Random Forest")

plt.show()