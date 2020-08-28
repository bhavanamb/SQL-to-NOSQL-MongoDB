import  xml.etree.ElementTree as ET
import mysql.connector
import re
import json

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user = 'root',
    password = '5^@vD4VJtvOT$1n@Q$',
    database="Company"
) 

cursor = mydb.cursor()

#sql = "SELECT pname,pnumber,dname,concat(group_concat('{\"FName\":\"',emp_fname,'\",\"LName\":\"',emp_lname,'\",\"Hours\":',hours,'}')) as emp_list FROM Company.ProjectDoc group by pname,pnumber,dname;"

sql = "SELECT pname,pnumber,dname,concat('[',group_concat('" + '{"FName":"' + "',emp_fname,'" + '","LName":"' + "',emp_lname,'" + '","Hours":' + "',hours,'}'),']') as emp_list FROM Company.ProjectDoc group by pname,pnumber,dname;"
cursor.execute(sql)

project_results = cursor.fetchall()



root = ET.Element("Projects")
for each_project in project_results:
    proj = ET.Element("Project")
    root.append(proj)
    Proj_name = ET.SubElement(proj,"PName")
    Proj_name.text = str(each_project[0])
    Proj_number = ET.SubElement(proj,"PNumber")
    Proj_number.text = str(each_project[1])
    DName = ET.SubElement(proj,"Dname")
    DName.text = str(each_project[2])
    if each_project is not None:
        y = re.findall('(\{.*?\})+',each_project[3])
        for each_emp in y:
            emp_record = json.loads(each_emp)
            Emp = ET.Element("Employee")
            proj.append(Emp)
            emp_fname = ET.SubElement(Emp,"Fname")
            emp_fname.text = emp_record['FName']
            emp_lname = ET.SubElement(Emp,"Lname")
            emp_lname.text = emp_record['LName']
            hours = ET.SubElement(Emp,'Hours')
            hours.text = str(emp_record['Hours'])
xmltree = ET.ElementTree(root)
print(xmltree)
with open("/Users/bhavana/Documents/summer/db2/project2/xml_files/Project.xml",'wb') as files : 
        xmltree.write(files) 
