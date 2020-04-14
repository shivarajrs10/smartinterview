from pymongo import MongoClient


############ **** monogo connection ******###############

#  client = MongoClient(
#     'mongodb+srv://mydb:mydb@cluster0-zzs7j.gcp.mongodb.net/test?retryWrites=true&w=majority')
client = MongoClient("mongodb://localhost:27017/")
db = client['Candidate-database']
collection = db['Candidate-collection']
Question_Db = db['Question_and_ans']
Admin_control_db = db['Admin_control_db']
Result_Db = db['Quiz_Result']


''' Data stored to mongodb'''


def collection_store(data):
    count = collection.count_documents({})
    if count > 0:
        x = collection.delete_many({})
        # print(x.deleted_count, " documents deleted.")
        collection.insert_many(data)

    else:
        collection.insert_many(data)


def questions_store(data):

    count = Question_Db.count_documents({})

    if count > 0:
        x = Question_Db.delete_many({})
        # print(x.deleted_count, " documents deleted.")
        db = Question_Db.insert_many(data)
    else:
        db = Question_Db.insert_many(data)


def request_Store(data):
    db = Admin_control_db.insert_many(data)


def result_Store(data):
    db = Result_Db.insert_many(data)


'''Data will return from the mongodb here'''


def collection_return(find_values, find_value):
    data = list(collection.find(
        {'Header': {'$all': find_values}}).sort(find_value, -1))
    return data


def FetchAll():
    data = list(collection.find().sort("Total", -1))
    return data


def Questions_All():
    data = list(Question_Db.find())
    return data


def Result_All():
    data = list(Result_Db.find().sort("Total", -1))
    return data


def request_All():
    data = list(Admin_control_db.find())
    return data


def signinVerify(mail):
    data = list(collection.find(
        {'Email': mail}))
    return data
