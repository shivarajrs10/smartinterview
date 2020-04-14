
import os
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
import mongoDb
import matplotlib
import pandas as pd
matplotlib.use('Agg')


"""
FLot for all data

"""
mypath = os.getcwd()
mypath = mypath+'/storage/'

# ALL results plot


def All_data():
    Db = mongoDb.FetchAll()
    print("mongodb-----------")

    header = []
    results = []
    names = []
    # print(Db)
    header = Db[0]['headerlist']
    for i in range(0, len(Db)):
        names.append(Db[i]['Name'])

        results.append(Db[i]['headerlistscore'])

    Total_dic = {}

    Total_dic['Names'] = names
    for i in range(0, len(results[0])):
        values = []
        for j in range(0, len(Db)):

            values.append(results[j][i])

        Total_dic[header[i]] = values
    # print(Total_dic)

    df = pd.DataFrame(Total_dic)
    # df = df.set_index('Names', drop=True)
    # df = df.iloc[:, 0:5]
    # print(df)
    plt.figure(figsize=(60, 20))

    df_last = df.iloc[:, -1]

    df_ref = df[df.columns[1:]]
    df.plot(x='Names', kind='barh', stacked=True,
            title='Total', mark_right=True)

    for n in df_ref:
        for i, (cs, ab, pc, tot) in enumerate(zip(df.iloc[:, 1:].cumsum(1)[n], df[n], df_ref[n], df_last)):
            # print(ab)
            if ab == 0.0:
                continue
            # if tot == 0.0:
            #     plt.text(cs - ab/2, i, str(np.round(pc, 1)) +
            #              '%', va='center', ha='center')
            if tot == 33.3:
                plt.text(cs - ab/2, i, str(np.round(pc, 1)) +
                         '%', va='center', ha='center')
            else:
                # plt.text(tot, i, str(tot), va='center')
                plt.text(cs - ab/2, i, str(np.round(pc, 1)) +
                         '%', va='center', ha='center')

    img_name = "Totals" + ".png"

    image_file = mypath
    plt.savefig(os.path.join(image_file, img_name), dpi=100)

    # plt.show()


# Individiual header plot

def Ind_header(database, header_text):
    data = header_text.upper()
    print(database)
    if ',' in data:
        data = header_text.upper().split(",")
        data = data[0]
    ind_header_name = "individual.png"

    names = []
    results = []
    ind_dict = {}
    # print(database)

    for i in range(0, len(database)):
        if data in database[i]:
            names.append(database[i]['Name'])
            results.append(database[i][data])

    # print(names)
    # print(results)

    ind_dict["Names"] = names
    ind_dict["Results"] = results

    df_ind = pd.DataFrame(ind_dict)
    # print(df_ind)

    # plt.figure(figsize=(10, 8))

    df_ind = df_ind.sort_values(
        by=['Results'], ascending=True)
    print(type(df_ind))
    df_ind.plot(x='Names',
                kind='barh', subplots=True, figsize=(10, 10))
    # print(df_ind)

    # plt.barh(range(len(names)), results)
    # plt.yticks(range(len(names)), names)
    plt.title(data)

    # plt.show()
    image_file = mypath
    plt.savefig(os.path.join(image_file, ind_header_name))


############### Data fetch ########################


def fetch(data):
    data = data.upper().split(",")

    Db = mongoDb.collection_return(data, data[0])
    return Db

############## ploat creation ###################


def graphs(no, db, text_all):

    pdf_files = []
    img_files = []
    headerlist = db[0]['headerlist']

    for i in range(0, no):
        head = db[i]['Header']
        res = db[i]['Result']

        name = db[i]['Name']
        # print(name)
        # print(type(name))

        Z = i+1
        img_name = str(Z) + name + '.png'
        pdf_name = str(Z) + name + '.pdf'  # used to store file name

        headL = []
        headM = []
        headH = []
        resL = []
        resM = []
        resH = []
        for i in range(0, len(res)):
            if 0 < res[i] < 35:
                resL.append(res[i])
                headL.append(head[i])
            elif 35 < res[i] < 75:
                resM.append(res[i])
                headM.append(head[i])
            else:
                resH.append(res[i])
                headH.append(head[i])

        plt.figure(figsize=(10, 8))
        plt.bar(headL, resL, color='r')
        plt.bar(headM, resM, color='b')
        plt.bar(headH, resH, color='g')
        plt.title(name)
        # plt.show()

        image_file = mypath
        plt.savefig(os.path.join(image_file, img_name))

        file = image_file + "/" + img_name  # used to image input for pdf
        pdf_file = mypath + "/" + pdf_name  # used to output pdf file path
        ind_img = mypath + "/individual.png"
        tot_img = mypath+"/Totals.png"
        print("before")
        if text_all == 'ALL':
            add_image(file, pdf_file, tot_img, name)
        else:
            add_image_All(file, pdf_file, ind_img, tot_img, name)

        pdf_files.append(pdf_name)
        img_files.append(img_name)

    return pdf_files, headerlist


#### pdf creation #####################


def add_image(image_path, output_path, tot_Imag, name):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.ln(85)  # move 85 down
    pdf.cell(200, 10, name, ln=1)

    pdf.image(image_path, x=8, y=10, w=200)

    pdf.add_page()
    pdf.ln(85)  # move 85 down
    pdf.cell(200, 10, 'Total', ln=1)
    pdf.image(tot_Imag, x=8, y=10, w=200)

    pdf.output(output_path)


def add_image_All(image_path, output_path, Ind_Img, tot_Imag, name):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.ln(85)  # move 85 down
    pdf.cell(200, 10, name, ln=1)
    pdf.image(image_path, x=10, y=12, w=200)
    pdf.add_page()
    pdf.ln(85)  # move 85 down
    pdf.cell(200, 10, 'Individiual', ln=1)
    pdf.image(Ind_Img, x=10, y=12, w=200)

    pdf.add_page()
    pdf.ln(85)  # move 85 down
    pdf.cell(200, 10, 'Total', ln=1)
    pdf.image(tot_Imag, x=10, y=12, w=200)

    pdf.output(output_path)
