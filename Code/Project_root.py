import mysql.connector
import json
from pymongo import MongoClient

#MongoDb connection
client = MongoClient('localhost',27017)

#mysql database connection
mydb = mysql.connector.connect(
    host='127.0.0.1',
    user = 'root',
    password = '5^@vD4VJtvOT$1n@Q$',
    database="Company"
)

cursor = mydb.cursor()


#query to select details from database
sql = "SELECT pname,pnumber,dname,concat('[',group_concat('" + '{"FName":"' + "',emp_fname,'" + '","LName":"' + "',emp_lname,'" + '","Hours":' + "',hours,'}'),']') as emp_list FROM Company.ProjectDoc group by pname,pnumber,dname;"
cursor.execute(sql)

project_results = cursor.fetchall()

project_dict = {}
emp_arr = []

project_json = open("project_doc.json",'w')
i = 1
project_json.write("[\n")

#generating nested document and writing to json file
for each_project in project_results:
    out_string = '{"Pname":"' + str(each_project[0]) + '","Pnumber":' + str(each_project[1]) + ',"Dname":"' + str(each_project[2]) + '","Employees":' + str(each_project[3]) + '}'
    #out = str(project_dict).replace("'",'"')
    project_json.write(out_string)
    if i != len(project_results):
        project_json.write(",\n")
    else:
        project_json.write("\n")
    i += 1

project_json.write("]")
project_json.close()


#mongodb database
myMongodb = client["CompanyData"]

#mongodb collection
projectCol = myMongodb["projectData"]

#print(myMongodb.list_collection_names())

projectData= open("project_doc.json",'r')


#Insert json to mongodb
data = projectCol.insert_many(json.load(projectData))

#print(data.inserted_ids)