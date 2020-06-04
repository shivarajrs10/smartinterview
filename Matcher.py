import random
from collections import Counter
import Converter

# database libarary
import os
import re
import pandas as pd
import en_core_web_sm
from spacy.matcher import PhraseMatcher
import ssl
nlp = en_core_web_sm.load()


#   ***********    empty global declaration ******************
header_list = []                  # Its used to Store csv headers
pdf_names = []                    # used to track uploaded pdf_files
word_dic = pd.DataFrame()  # used to store read csv file
# header_list_words used to header name + words like :Data Science words
header_list_words = []
# spacy_words used to stores header values to spacy values
spacy_words = {}
# key_words used to header name + KEYWORDS like :MACHINE_LEARNING_KEYWORDS
key_words = []
# header_score used to header name + SCORE like :MACHINE_LEARNING_SCORE
header_score = []


# ###################  File Storage Handling ###############
# mypath = r'C:\Users\srs2\Documents\Python_Projects\show_times\storage'
# onlyfiles = [os.path.join(mypath, f) for f in os.listdir(
#     mypath) if os.path.isfile(os.path.join(mypath, f))]
# print(onlyfiles)


#################### CSV Handling ######################
def csv_handling(csv):
    csvfile = csv

    word_dict = pd.read_csv(csvfile)
    global word_dic
    word_dic = pd.DataFrame()
    word_dic = word_dic.append(word_dict)

    # print(word_dic)

    global header_list
    global header_list_words
    global key_words
    global header_score
    header_list = []
    header_list_words = []
    key_words = []
    header_score = []

    count = 0
    for col in word_dict.columns:
        header_list.append(col)
        header_list_words.append(header_list[count] + ' words')
        keyword_name = header_list[count].upper().replace(
            " ", "_") + "_KEYWORDS"
        key_words.append(keyword_name)
        score_name = header_list[count].upper().replace(
            " ", "_") + "_SCORE"
        header_score.append(score_name)
        count = count + 1

####################### PDF Handling ##################################


# def candidate_result(filenames):
#     i = 1
#     csv_handling()
#     while i < len(onlyfiles):
#         path = onlyfiles[i]
#         filename = filenames[i-1]

#         name, mail, result_dic = create_database(path, filename)
#         header_Cal(name, mail, result_dic)
#         i += 1
#     return name, mail, result_dic


######################### Docx handling ##################################

def docx_extract(file):
    import docx
    text = ''
    doc = docx.Document(file)
    for i in doc.paragraphs:
        text = text + i.text + ' '
    return text
######################## txt handling ################################


def txt_extract(file):
    text = ''
    with open(file, 'r') as f:
        for line in f:
            # print(f"txt \n {line}")
            text = text+line+' '
    return text


def create_database(file, name):

    cand_name = name
    # print(cand_name)
    cv = ''
    # print(word_dic)
    # print(header_list)
    if ".pdf" in file:
        cv = Converter.text_convert(file)
    elif ".docx" in file:
        cv = docx_extract(file)
    else:
        cv = txt_extract(file)
    # print("----- CV ------")
    # print(cv)
    cv = str(cv)
    cv = cv.replace("\\n", "")
    cv_text = cv.lower()
    # print(cv_text)
    match = re.search(r'[\w\.-]+@[\w\.-]+', cv_text)
    e_mail_ID = match.group(0)
    # print(cand_name+' '+e_mail_ID)

    global spacy_words
    for i in range(0, len(header_list)):
        spacy_words[header_list_words[i]] = [
            nlp(text) for text in word_dic[header_list[i]].dropna(axis=0)]
    # print(spacy_words)

    matcher = PhraseMatcher(nlp.vocab)
    for i in range(0, len(header_list)):
        matcher.add(key_words[i], None, *spacy_words[header_list_words[i]])

    doc = nlp(cv_text)

    d = []

    matches = matcher(doc)
    for match_id, start, end in matches:
        # get the unicode ID, i.e. 'COLOR'
        rule_id = nlp.vocab.strings[match_id]
        span = doc[start:end]  # get the matched slice of the doc

        d.append((rule_id, span.text))
        # print(rule_id, span.text)
        # print(d)

    # print('\n\n')

    #  Used to store results...

    result_dic = {}
    for i, j in Counter(d).items():
        result = []

        if i[0] in result_dic:
            result = result_dic[i[0]]
            # print(result)
            result.append(i[1])
            result_dic[i[0]] = result
        else:
            result.append(i[1])
            result_dic[i[0]] = result

    return cand_name, e_mail_ID, result_dic


def header_Cal(C_name, C_mail, match_keywords, test_name):

    # used to store the keyword score
    final_score_result = {}
    # count = 0
    # count_score = 0
    result = []
    Keys = {}
    header = []

    # print(match_keywords)
    # print(word_dic)

    C_name = C_name.split('.')
    C_name = C_name[0]
    # print(C_name)
    # print(C_mail)
    word_dic_size = 0
    match_key_len = 0
    print("================")
    for i in header_list:
        word_dic_size += len(word_dic[i].dropna(axis=0))
    # print(word_dic_size)
    for i in header_list:

        head = i.upper()
        key = head.replace(
            " ", "_") + "_KEYWORDS"

        if key in match_keywords.keys():

            values = match_keywords[key]

            match_key_len += len(values)

            score = (len(values) / len(word_dic[i].dropna(axis=0))) * 100
            header.append(head)
            Keys[key] = values
            result.append(round(score, 1))
            # count = count + 1
            # count_score = count_score+score
    # print(Keys)
    # print(result)
    # print(count_score / count)
    # print(round((match_key_len/word_dic_size)*100, 2))
    final_score_result["Name"] = C_name
    final_score_result["Email"] = C_mail
    final_score_result['Test_Name'] = test_name
    final_score_result["Password"] = C_name + str(random.randint(1000, 9999))
    final_score_result["Uid"] = random.randint(1000, 9999)
    # final_score_result["Header"] = header
    # final_score_result["Result"] = result
    final_score_result["Total"] = round((match_key_len/word_dic_size)*100, 1)
    final_score_result["Keys"] = Keys
    header_list_upper = [x.upper() for x in header_list]
    final_score_result["headerlist"] = header_list_upper
    # print(final_score_result)
    # print("\n\n")

    headerlistscore = [0]*len(header_list)
    for i in range(0, len(header)):

        if header[i] in header_list_upper:
            idxxx = header_list_upper.index(header[i])
            headerlistscore[idxxx] = result[i]

    final_score_result["headerlistscore"] = headerlistscore
    for i in range(0, len(header_list_upper)):

        final_score_result[header_list_upper[i]] = headerlistscore[i]
    print(final_score_result)
    return final_score_result
