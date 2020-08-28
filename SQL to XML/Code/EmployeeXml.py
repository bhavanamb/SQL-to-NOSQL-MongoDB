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

sql = "SELECT emp_fname,emp_lname,dname,concat('[',group_concat('" + '{"Pname":"' + "',pname,'" + '","Pnumber":"' + "',pnumber,'" + '","Hours":' + "',hours,'}'),']') as proj_list FROM Company.EmployeeDoc group by emp_fname,emp_lname, dname;"
cursor.execute(sql)

project_results = cursor.fetchall()

root = ET.Element("Employees")
for each_emp in project_results:
    print(each_emp)
    emp_root = ET.Element("Employee")
    root.append(emp_root)
    emp_fname = ET.SubElement(emp_root,"FName")
    emp_fname.text = str(each_emp[0])
    emp_lname = ET.SubElement(emp_root,"LName")
    emp_lname.text = str(each_emp[1])
    DName = ET.SubElement(emp_root,"Dname")
    DName.text = str(each_emp[2])   
    if each_emp[3] is not None:
        y = re.findall('(\{.*?\})+',each_emp[3])
        for each_proj in y:
            proj_record = json.loads(each_proj)
            proj_subroot = ET.Element("Project")
            emp_root.append(proj_subroot)
            proj_name = ET.SubElement(proj_subroot,"PName")
            proj_name.text = proj_record['Pname']
            proj_number = ET.SubElement(proj_subroot,"PNumber")
            proj_number.text = proj_record['Pnumber']
            hours = ET.SubElement(proj_subroot,'Hours')
            hours.text = str(proj_record['Hours'])
xmltree = ET.ElementTree(root)
print(xmltree)
with open("/Users/bhavana/Documents/summer/db2/project2/xml_files/Employee.xml",'wb') as files : 
        xmltree.write(files) 
