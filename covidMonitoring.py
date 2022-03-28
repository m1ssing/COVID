import arcpy
import datetime
arcpy.OverwriteOutput = True
covidLayer = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Owner.sde\\Horizon.DBO.EOC\\Horizon.DBO.COVIDselfMonitoring"
#Has to be in datetime due to starttime and endtime in COVIDMonitoring being a datetime field
currentDate= datetime.datetime.now()
fields = ["starttime", "Status", "endtime", "notes"]
with arcpy.da.UpdateCursor(covidLayer, fields) as Ucur:
    for Urow in Ucur:
        if "(REC)" in Urow[3]:
            Urow[1] = "Recovered"
            Ucur.updateRow(Urow)
        if "(CON)" in Urow[3]:
            if Urow[0] == None or Urow[2] == None:
                Urow[1] = "Active - Confirmed"
                Ucur.updateRow(Urow)
                #starttime <= currentTime and endtime >= currentTime
            elif Urow[0] <= currentDate and Urow[2] >= currentDate:
                Urow[1] = "Active - Confirmed"
                Ucur.updateRow(Urow)
            else:
                Urow[1] = "Active - Confirmed"
                Ucur.updateRow(Urow)
        if "(PUM)" in Urow[3]:
            if Urow[0] == None or Urow[2] == None:
                Urow[1] = "Active - Presumptive"
                Ucur.updateRow(Urow)
            elif Urow[0] <= currentDate and Urow[2] >= currentDate:
                Urow[1] = "Active - Presumptive"
                Ucur.updateRow(Urow)
            else:
                Urow[1] = "Inactive - Presumptive"
                Ucur.updateRow(Urow)
        if "(CFA)" in Urow[3]:
            if Urow[0] == None or Urow[2] == None:
                Urow[1] = "Fatality"
                Ucur.updateRow(Urow)
            elif Urow[0] <= currentDate and Urow[2] >= currentDate:
                Urow[1] = "Fatality"
                Ucur.updateRow(Urow)
            else:
                Urow[1] = "Fatality"
                Ucur.updateRow(Urow)
        if "(PROB)" in Urow[3]:
            if Urow[0] == None or Urow[2] == None:
                Urow[1] = "Probable"
                Ucur.updateRow(Urow)
del Ucur

COVID19_Cases = "\\\\gisapp\\Workspace\\Models\\Scripts\\Horizon_owner.sde\\EOC\\COVID19_Cases"
currentDay = "date " + "'" + str(datetime.date.today()) + "'"
currentDayfixed = currentDay.replace("date", "")
currentSQL = "Location IN ( 'Pearland' ) AND CountType = 'Cumulative Monitoring' AND Date >= " + currentDayfixed
StatusSQL = "Status LIKE 'Active%'"
Covid_cases_flds = ["Location", "Date", "CountType", "CaseCount"]

arcpy.MakeFeatureLayer_management(covidLayer, "Monitor_FL", StatusSQL)
NewCount = int(arcpy.GetCount_management("Monitor_FL").getOutput(0))
x = datetime.datetime.today().replace(microsecond=0)

cList = []
SC = arcpy.da.SearchCursor(COVID19_Cases, Covid_cases_flds, currentSQL)
for record in SC:
    cList.append(record[1])


if cList != []:
    with arcpy.da.UpdateCursor(COVID19_Cases, Covid_cases_flds, currentSQL) as UC:
        for row in UC:
            UC.updateRow(("Pearland", x, "Cumulative Monitoring", NewCount))
    del UC
else:
    with arcpy.da.InsertCursor(COVID19_Cases, Covid_cases_flds) as iCursor:
            iCursor.insertRow(("Pearland", x, "Cumulative Monitoring", NewCount))
    del iCursor




print("Monitoring Script Done.")


