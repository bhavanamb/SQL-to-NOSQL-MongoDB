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
sql = "SELECT emp_fname,emp_lname,dname,concat('[',group_concat('" + '{"Pname":"' + "',pname,'" + '","Pnumber":' + "',pnumber,'" + ',"Hours":' + "',hours,'}'),']') as emp_list FROM Company.EmployeeDoc group by emp_fname,emp_lname, dname;"
cursor.execute(sql)


employess_result = cursor.fetchall()

employee_dict ={}

employee_json = open("Employee_doc.json",'w')


i = 1
employee_json.write("[\n")

#generating nested document and writing to json file
for each_emp in  employess_result:
    emp_list = each_emp[3]
    if each_emp[3] is  None:
        emp_list = []
    out_string = '{"Emp_Fname":"' + str(each_emp[0]) + '","Emp_Lname":"' + str(each_emp[1]) + '","Emp_dname":"' + str(each_emp[2]) + '","Projects":' + str(emp_list) + '}'
    employee_json.write(out_string)
    if i != len(employess_result):
        employee_json.write(",\n")
    else:
        employee_json.write("\n")
    i += 1

employee_json.write("]")
employee_json.close()

#mongodb database
myMongodb = client["CompanyData"]

#mongodb collection
empCol = myMongodb["employeeData"]

#print(myMongodb.list_collection_names())

employeeData= open("Employee_doc.json",'r')


#Insert json to mongodb
data = empCol.insert_many(json.load(employeeData))

#print(data.inserted_ids)