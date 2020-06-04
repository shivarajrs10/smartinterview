import pandas as pd
import os
import random
# mypath = os.getcwd()
# file = mypath+'/storage/Questions.csv'


def headers(file):
    df = pd.read_csv(file)
    header_list = []
    for col in df.columns:
        header_list.append(col)
    return header_list


def question_extract(path, test_name):
    header_list = headers(path)
    df = pd.read_csv(path)
    count = 7
    database = {}
    database["Header"] = header_list
    all_que = []

    for j in range(0, len(header_list)):

        sr = df[header_list[j]]
        Que = ''
        options = []
        ans = ''
        for i in range(0, len(sr)):

            if i == count-1:
                list_que = dict()
                # ans = sr.get(i)
                level = sr.get(i).lower()

                Qid = header_list[j] + str(random.randint(1000, 9999))

                list_que["Qid"] = Qid
                list_que['Question'] = Que
                list_que['Options'] = options
                list_que['Anshwer'] = ans
                list_que['Level'] = level
                all_que.append(list_que)
                count = count + 7
                options = []

                Que = ''

                ans = ''

            elif i == count - 2:
                ans = sr.get(i)

            elif i == count - 7:
                Que = sr.get(i)

            elif i < count-2:

                options.append(sr.get(i))

            else:
                break
        database[header_list[j].upper()] = all_que
        database["TestName"] = test_name
        all_que = []
        count = 7

    return database


# print(question_extract())
