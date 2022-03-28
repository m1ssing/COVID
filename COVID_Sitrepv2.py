import xlsxwriter
import arcpy
import openpyxl
from lxml import html
import requests
import pandas as pd
from lxml import etree
import re
from selenium import webdriver
import time
import arcpy
import datetime
from win32com import client
import win32com

arcpy.env.OverwriteOutput = True

def main():
    gCon = globalusConfirmed()
    gDeath = globalusDeaths()
    pearland = Pearland()
    bc = brazoriaCounty()
    fbc = fortbendCounty()
    hc = harrisCounty()
    xlsx(gCon, gDeath, pearland, bc, fbc, hc)

def xlsx(gCon, gDeath, pearland, bc, fbc, hc):
    workbook = xlsxwriter.Workbook("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\test_xlsx1.xlsx")
    worksheet = workbook.add_worksheet()
    column_format = workbook.add_format({'bold': True, 'font_size': 14, 'text_wrap': True, "align": "center", "bg_color": "#aeaaaa"})
    row_format = workbook.add_format({'bold': True, 'font_size': 12})
    number_format = workbook.add_format({"num_format": "#,##0"})
    worksheet.set_column("A1:A1",  17.14)
    worksheet.set_column("D1:D1",  9.43)
    worksheet.set_column("E1:E1",  11)
    worksheet.set_column("G1:G1",  9.43)
    columnDict = {"A1": "Location", "B1": "Cases", "C1": "Cases Since Last Report","D1": "Cases Percent Change", "E1": "Reported Deaths",
                  "F1": "Deaths Since Last Report", "G1": "Deaths Percent Change"}
    for key, value in columnDict.items():
        worksheet.write_string(key, value, column_format)

    rowDict = {"A2": "Global", "A3": "US", "A4": "Texas", "A5": "Fort Bend County", "A6": "Harris County", "A7": "Brazoria County", "A8": "City of Pearland"}
    for key, value in rowDict.items():
        worksheet.write_string(key, value, row_format)
    #Texas, FB, Harris, Brazoria Confirmed
    casesDict = {"B2": gCon[0], "B3": gCon[1], "B4": gCon[2], "B5": int(fbc[1]), "B6": int(hc[0]), "B7": int(bc[1]), "B8": pearland[0]}
    for key, value in casesDict.items():
        worksheet.write_number(key, value, number_format)
    #Texas Fatality
    deathDict = {"E2": gDeath[0], "E3": gDeath[1], "E4": gDeath[2], "E5": int(fbc[0]), "E6": int(hc[1]), "E7": int(bc[0]), "E8": pearland[1]}
    for key, value in deathDict.items():
        worksheet.write_number(key, value, number_format)
    points = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_SitRep"
    fields = ['Global_C', 'US_C', 'Texas_C', 'FB_C', 'Harris_C', 'Braz_C', 'Pearland_C', 'Global_D', 'US_D', 'Texas_D', 'FB_D', 'Harris_D', 'Braz_D', 'Pearland_D', "Date"]
    with arcpy.da.SearchCursor(points, fields) as Scur:
        for row in Scur:
            row1 = row
    prevCasesDict = {"C2": row1[0], "C3": row1[1], "C4": row1[2], "C5": row1[3], "C6": row1[4], "C7": row1[5], "C8": row1[6]}
    #Cases Since Last Report
    worksheet.write_formula("C2", "=SUM(B2-{})".format(row1[0]))
    worksheet.write_formula("C3", "=SUM(B3-{})".format(row1[1]))
    worksheet.write_formula("C4", "=SUM(B4-{})".format(row1[2]))
    worksheet.write_formula("C5", "=SUM(B5-{})".format(row1[3]))
    worksheet.write_formula("C6", "=SUM(B6-{})".format(row1[4]))
    worksheet.write_formula("C7", "=SUM(B7-{})".format(row1[5]))
    worksheet.write_formula("C8", "=SUM(B8-{})".format(row1[6]))

    #Deaths Since Last Report
    worksheet.write_formula("F2", "=SUM(E2-{})".format(row1[7]))
    worksheet.write_formula("F3", "=SUM(E3-{})".format(row1[8]))
    worksheet.write_formula("F4", "=SUM(E4-{})".format(row1[9]))
    worksheet.write_formula("F5", "=SUM(E5-{})".format(row1[10]))
    worksheet.write_formula("F6", "=SUM(E6-{})".format(row1[11]))
    worksheet.write_formula("F7", "=SUM(E7-{})".format(row1[12]))
    worksheet.write_formula("F8", "=SUM(E8-{})".format(row1[13]))

    percent_fmt = workbook.add_format({'num_format': '0%'})
    #Percent Difference Cases
    worksheet.write_formula("D2", "=SUM(C2/B2)", percent_fmt)
    worksheet.write_formula("D3", "=SUM(C3/B3)", percent_fmt)
    worksheet.write_formula("D4", "=SUM(C4/B4)", percent_fmt)
    worksheet.write_formula("D5", "=SUM(C5/B5)", percent_fmt)
    worksheet.write_formula("D6", "=SUM(C6/B6)", percent_fmt)
    worksheet.write_formula("D7", "=SUM(C7/B7)", percent_fmt)
    worksheet.write_formula("D8", "=SUM(C8/B8)", percent_fmt)

    #Percent Difference Deaths
    worksheet.write_formula("G2", "=SUM(F2/E2)", percent_fmt)
    worksheet.write_formula("G3", "=SUM(F3/E3)", percent_fmt)
    worksheet.write_formula("G4", "=SUM(F4/E4)", percent_fmt)
    worksheet.write_formula("G5", "=SUM(F5/E5)", percent_fmt)
    worksheet.write_formula("G6", "=SUM(F6/E6)", percent_fmt)
    worksheet.write_formula("G7", "=SUM(F7/E7)", percent_fmt)
    worksheet.write_formula("G8", "=SUM(F8/E8)", percent_fmt)
    
    workbook.close()
    date = datetime.date.today()
    o = win32com.client.Dispatch("Excel.Application")
    o.Visible = False
    wb_path = r"\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\test_xlsx.xlsx"
    wb = o.Workbooks.Open(wb_path)
    ws_index_list = [1]
    path_to_pdf = r"\\\\GISAPP\\Workspace\\GIS Staff Workspace\mmasters\\COVID_Update{}.pdf".format(date)
    wb.WorkSheets(ws_index_list).Select()
    wb.ActiveSheet.ExportAsFixedFormat(0, path_to_pdf)


def globalusConfirmed():
    jh = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/1"
    path = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb"
    name="covidJHData"
    points = path + "\\" + name
    arcpy.Delete_management(points)
    arcpy.FeatureClassToFeatureClass_conversion(jh, path, name)
    globalTotal = 0
    usTotal = 0
    texTotal = 0

    fields = ["Confirmed","Country_Region", "Province_State"]
    with arcpy.da.SearchCursor(points, fields) as Scur:
        for row in Scur:
            globalTotal += row[0]
            if row[1] == "US":
                usTotal += row[0]
                if row[2] == "Texas":
                    texTotal += row[0]
    return(globalTotal, usTotal, texTotal)



def globalusDeaths():

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
            globalTotalDeaths += row[0]
            if row[1] == "US":
                usTotalDeaths += row[0]
                if row[2] == "Texas":
                    texTotalDeaths += row[0]
    print(texTotalDeaths)
    return(globalTotalDeaths, usTotalDeaths, texTotalDeaths)


def Pearland():
    # Pearland Recovered / Fatalities
    covidLayer = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Owner.sde\\Horizon.DBO.EOC\\Horizon.DBO.COVIDselfMonitoring"
    fields = ["Status"]
    PearlandConfirmed = 0
    PearlandDeaths = 0
    PearlandRecovered = 0 
    with arcpy.da.SearchCursor(covidLayer, fields) as Scur:
        for row in Scur:
            if row[0] in ["Active - Confirmed", "Fatality", "Recovered"]:
                PearlandConfirmed += 1
            if row[0] == "Fatality":
                PearlandDeaths += 1
    return(PearlandConfirmed, PearlandDeaths)


def harrisCounty():

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
        if x == "Confirmed Cases" or x == "Deaths":
            name = lst.index(x)
            num = name + 2
            lst1.append(lst[name:num])
    
    HarrisConfirmed = lst1[0][1].replace(",", "")
    print(lst1)
    print("Harris Done.")
    return(HarrisConfirmed, lst1[1][1])

def fortbendCounty():

    driver = webdriver.Firefox(executable_path=r"C:\Program Files\geckodriver.exe")
    lst = []
    page = driver.get('https://www.arcgis.com/apps/opsdashboard/index.html#/75133e049f584ae8b51dc6cba740009a')
    time.sleep(10)
    buyers = driver.find_elements_by_xpath('//*')
    for node in buyers:
        if node.text in lst:
            pass
        else:
            lst.append(node.text)
    lst = lst[0].split("\n")
    lst2 = []
    lst1 = []
    for x in lst:
        if x == "Confirmed Cases" or x == "Deaths":
            name = lst.index(x)
            num = name + 2
            lst1.append(lst[name:num])
    FortBendConfirmed = lst1[1][1].replace(",", "")
    print("Fort Bend Done.")
    return(lst1[0][1], FortBendConfirmed)

def brazoriaCounty():

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
        if x[1] == "Total Reported" or x[1] == "Deceased":
            lst3.append(x)
    print("Brazoria Done.")
    print(lst3)
    BrazoriaConfirmed = int(lst2[0][0]) + int(lst2[1][0]) + int(lst2[2][0])
    return (lst3[0][0], BrazoriaConfirmed)



main()
print(".")
