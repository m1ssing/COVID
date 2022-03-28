import requests
import pandas as pd
import re
from selenium import webdriver
import time
import arcpy
import datetime
inFile = open("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\death_Rec.txt", "w")
def main():
    
    harris = harrisCounty()
    fb = fortbendCounty()
    braz = brazoriaCounty()
    #galv = galvestonCounty()
    texas = Texas()
    
    #harrisDeath = int(harris[1]) + int(houston[0])
    print("Harris: ", "Recovered: ", harris[0], "Deaths: ", harris[1])
    print("Fort Bend: ", "Recovered: ", fb[0], "Deaths: ", fb[1])
    print("Brazoria: ", "Recovered: ", braz[1], "Deaths: ", braz[0])
    #print("Galveston Death", galv[1], "Galveston Recovered", galv[0])

    currentDate = datetime.date.today()
    currentTime = currentDate.strftime("%m/%d/%Y")
    currentDateDelta = datetime.date.today() + datetime.timedelta(days = -1)
    currentTimeDelta = currentDateDelta.strftime("%m/%d/%Y")
    deathDict= { "Harris": harris[1], "Fort Bend": fb[1],  "Brazoria": braz[0],  "Texas": texas}
    #"Fort Bend": fb[1],
    #"Galveston": galv[1],
    #"Harris": int(harris[1]),
    recDict= { "Harris": harris[0], "Fort Bend": fb[0], "Brazoria": braz[1]}
    #"Fort Bend": fb[0],
    #"Harris": int(harris[0]),
    #"Galveston": galv[0]
    points = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Owner.sde\\Horizon.DBO.EOC\\Horizon.DBO.COVID19_Cases"
    fields = ["Location", "Date", "CountType", "CaseCount"]

    lst = []
    lst1 = []
    lst2 = []
    
    y = 0
    #Deaths
    with arcpy.da.UpdateCursor(points, fields)as Ucur:
        for row in Ucur:
            lst.append([row[0], row[1], row[2]])
            for key, value in deathDict.items():
                if row[0] == key and row[1].strftime("%m/%d/%Y") == currentTime and row[2] == "Cumulative Deaths":
                    Ucur.updateRow((key, currentTime, "Cumulative Deaths", value ))
    for x in lst:
        if x[1].strftime("%m/%d/%Y") == currentTime and x[2] == "Cumulative Deaths" and x[0] != "Pearland":
            lst1.append(x)
    print("DeathList", lst1)
    if len(lst1) == 0:
        for key, value in deathDict.items():
            with arcpy.da.InsertCursor(points, fields) as Icur:
                Icur.insertRow((key, currentTime, "Cumulative Deaths", value ))
    lst = []
    lst1 = []
    lst2 = []
    #Recoveries
    with arcpy.da.UpdateCursor(points, fields)as Ucur:
        for row in Ucur:
            lst.append([row[0], row[1], row[2]])
            for key, value in recDict.items():
                if row[0] == key and row[1].strftime("%m/%d/%Y") == currentTime and row[2] == "Cumulative Recovered" and x[0] != "Pearland":
                    Ucur.updateRow((key, currentTime, "Cumulative Recovered", value ))

    for x in lst:
        if x[1].strftime("%m/%d/%Y") == currentTime and x[2] == "Cumulative Recovered"and x[0] != "Pearland":
            lst1.append(x)
    print("RecList", lst1)
    if len(lst1) == 0:
        for key, value in recDict.items():
            with arcpy.da.InsertCursor(points, fields) as Icur:
                Icur.insertRow((key, currentTime, "Cumulative Recovered", value ))
       
def harrisCounty():
    inFile = open("\\\\GISAPP\\Workspace\\GIS STaff Workspace\\cschultz\\PythonFiles\\death_Rec.txt", "w")
    inFile.write("HAR")
    inFile.close()
    driver = webdriver.Firefox(executable_path=r"C:\Program Files\geckodriver.exe")
    lst = []
    page = driver.get('https://harriscounty.maps.arcgis.com/apps/opsdashboard/index.html#/c0de71f8ea484b85bb5efcb7c07c6914')
    time.sleep(10)
    buyers = driver.find_elements_by_xpath('//*')
    for node in buyers:
        if node.text in lst:
            pass
        else:
            lst.append(node.text)

    lst = lst[0].split("\n")
    print(lst)
    for x in lst:
        if x == "(Not including Houston)":
            lst.remove("(Not including Houston)")
    lst1 = []
    for x in lst:
        if x == "Recovered Cases" or x == "Deaths":
            name = lst.index(x)
            num = name + 2
            lst1.append(lst[name:num])
    print(lst1)
    print("Harris Done.")
    return(lst1[0][1], lst1[1][1])
    
#def Houston():
#    page = requests.get('https://houstonemergency.org/covid19')
#    tree = html.fromstring(page.content)
#    buyers = tree.xpath('//div[@class="fl-rich-text"]//h3/text()')
#    numList = [i.split(";\xa0", 1)[0:2] for i in buyers]
#    lst = []
#    for x in range(0,1):
#        lst.append(numList[0][x].split(": "))
#    print("Houston Done.")
#    return (lst[0][1])#, lst[1][1])
    

def fortbendCounty():
    inFile = open("\\\\GISAPP\\Workspace\\GIS STaff Workspace\\cschultz\\PythonFiles\\death_Rec.txt", "w")
    inFile.write("FB")
    inFile.close()
    driver = webdriver.Firefox(executable_path=r"C:\Program Files\geckodriver.exe")
    lst = []
    page = driver.get('https://fbcgis.maps.arcgis.com/apps/opsdashboard/index.html#/b7dc7f0c14d5494eb82b888cc705b7c8')
    #https://www.arcgis.com/apps/opsdashboard/index.html#/75133e049f584ae8b51dc6cba740009a
    time.sleep(10)
    buyers = driver.find_elements_by_xpath('//*')
    for node in buyers:
        if node.text in lst:
            pass
        else:
            lst.append(node.text)
    print(lst)
    lst = lst[0].split("\n")  
    lst1 = [lst[i:i+2] for i in range(0,12,2)]
    lst2 = []
    print(lst)
    for x in lst:
        if x == "Recovered" or x == "Deaths":
            name = lst.index(x)
            num = name + 2
            lst2.append(lst[name:num])
    print(lst2)
    print("Fort Bend Done.")
    return(lst2[0][1], lst2[1][1])

def galvestonCounty():
    inFile = open("\\\\GISAPP\\Workspace\\GIS STaff Workspace\\cschultz\\PythonFiles\\death_Rec.txt", "w")
    inFile.write("GALV")
    inFile.close()
    driver = webdriver.Firefox(executable_path=r"C:\Program Files\geckodriver.exe")
    lst = []
    page = driver.get('https://galvcountymaps.maps.arcgis.com/apps/opsdashboard/index.html#/cb485269e11f42508e6ed1e969e4ef75')
    time.sleep(10)
    buyers = driver.find_elements_by_xpath('//*')
    for node in buyers:
        if node.text in lst:
            pass
        else:
            lst.append(node.text)
    lst = lst[0].split("\n")
    lst1 = []
    lst2 = []
    print(lst)
    for x in lst:
        if x in ["Recovered", "Deceased"] :
            name = lst.index(x)
            stuff = name + 2
            lst1.append(lst[name:stuff])
    print(lst1)
    print("Galveston Done.")
    return(lst1[0][1], lst1[1][1])

def brazoriaCounty():
    inFile = open("\\\\GISAPP\\Workspace\\GIS STaff Workspace\\cschultz\\PythonFiles\\death_Rec.txt", "w")
    inFile.write("BRAZ")
    inFile.close()
    driver = webdriver.Firefox(executable_path=r"C:\Program Files\geckodriver.exe")
    lst = []
    page = driver.get('https://app.powerbigov.us/view?r=eyJrIjoiYTk3ZTllZTQtMzIwNi00OGY3LThhMTktYTg2OWRiMzk4ZWYwIiwidCI6IjY0NjAwMjA1LTFlZjctNDgwOC05NzljLWEyNjc2ZDJhMTQzOCJ9')
    time.sleep(10)
    buyers = driver.find_elements_by_xpath('//div[@class = "cardItemContainer"]')
    for node in buyers:
        if node.text in lst:
            pass
        else:
            lst.append(node.text)
    lst1= [x.replace('\n', "  ") for x in lst]
    lst2=[x.split("  ") for x in lst1]
    print(lst2)
    lst3 = []
    for x in lst2:
        if x[1] == "Recovered" or x[1] == "Deceased":
            lst3.append(x)
    print("Brazoria Done.")
    print(lst3)
    return (lst3[1][0], lst3[0][0])


def Texas():
    jh = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/0"
    path = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb"
    name="covidJHDataDeaths"
    points = path + "\\" + name
    arcpy.Delete_management(points)
    arcpy.FeatureClassToFeatureClass_conversion(jh, path, name)
    globalTotalDeaths = 0
    usTotalDeaths = 0
    texTotalDeaths = 0

    fields = ["Deaths","Country_Region", "Province_State"]
    with arcpy.da.SearchCursor(points, fields) as Scur:
        for row in Scur:
            if row[2] == "Texas":
                texTotalDeaths += row[0]
   
    return(texTotalDeaths)



main()
print(".")
inFile.close()

