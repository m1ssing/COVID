import arcpy
import datetime
arcpy.env.OverwriteOutput = True
pearlandRow = 0
brazoriaRow = 0
fbRow = 0
harrisRow = 0
houstonRow = 0
texasRow = 0
galvRow = 0

def main():
    cumulativeConfirmed()
    cumulativeRecovered()
    cumulativeDeaths()
    #dailyConfirmed()

def cumulativeConfirmed():


    def DatasetUpdate():
        lst = ["Location", "Date", "CountType", "CaseCount"]
        points = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.EOC\\Horizon.DBO.COVID19_Cases"
        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
        lstDaily = ["Date", "CityofPearland", "BrazoriaCounty", "FortBendCounty", "HarrisCounty", "CityofHouston", "StateofTexas", "GalvestonCounty"]

        arcpy.DeleteRows_management("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset")

        def DailyUpdate():

            mdate = str(datetime.date.today())
            rdate = str(datetime.date(2020, 3, 4))
            mdate1 = datetime.datetime.strptime(mdate, "%Y-%m-%d").date()
            rdate1 = datetime.datetime.strptime(rdate, "%Y-%m-%d").date()
            delta =  (mdate1 - rdate1).days
            dateList = list(range(0, delta+1))
            dateList.reverse()

            for x in dateList:
                pearlandRow = 0
                brazoriaRow = 0
                fbRow = 0
                harrisRow = 0
                houstonRow = 0
                texasRow = 0
                galvRow = 0
                currentDate = datetime.date.today() - datetime.timedelta(days = x)
                currentTime = currentDate.strftime("%m/%d/%Y")
                with arcpy.da.SearchCursor(points, lst) as Scur:
                        for row in Scur:
                            if row[1].strftime("%m/%d/%Y") == currentTime:
                                timeRow = row[1].strftime("%m/%d/%Y")
                                if row[2] == "Cumulative Confirmed":
                                    if row[0] == "Pearland":
                                        pearlandRow = row[3]
                                    if row[0] == "Brazoria":
                                        brazoriaRow = row[3]
                                    if row[0] == "Fort Bend":
                                        fbRow = row[3]
                                    if row[0] == "Harris":
                                        harrisRow = row[3]
                                    if row[0] == "Houston":
                                        houstonRow = row[3]
                                    if row[0] == "Texas":
                                        texasRow = row[3]
                                    if row[0] == "Galveston":
                                        galvRow = row[3]
        
                        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
                        lstDaily = ["Date", "CityofPearland", "BrazoriaCounty", "FortBendCounty", "HarrisCounty", "CityofHouston", "StateofTexas", "GalvestonCounty"]
                        lstCumulative = ["Date", "CityofPearlandTOTAL", "BrazoriaTOTAL", "FortBendTOTAL", "HarrisTOTAL", "HoustonTOTAL", "TexasTOTAL", "GalvestonTOTAL"]
                        lstValue = [timeRow, pearlandRow, brazoriaRow, fbRow, harrisRow, houstonRow, texasRow, galvRow]
                        with arcpy.da.InsertCursor(pointsDaily, lstCumulative) as Icur:
                            Icur.insertRow(lstValue)

        DailyUpdate()

    def RunningTotal():
        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
        lstDaily = ["CityofPearlandTOTAL", "BrazoriaTOTAL", "FortBendTOTAL", "HarrisTOTAL", "HoustonTOTAL","TexasTOTAL", "GalvestonTOTAL"]

        for z in [0, 1, 2, 3, 4, 5, 6]:
            with arcpy.da.SearchCursor(pointsDaily, lstDaily)as Scur:
                lst = []
                for row in Scur:
                    lst.append(row[z])  
                cumulative = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
                totalList = ["CityofPearland", "BrazoriaCounty", "FortBendCounty", "HarrisCounty", "CityofHouston", "StateofTexas", "GalvestonCounty"]
                with arcpy.da.UpdateCursor(cumulative, totalList) as Ucur:
                    x = 0
                    for row in Ucur:
                        if x == 0:
                            lst1 = lst[x]
                        else:
                            lst1 = lst[x] - lst[x-1]
                        row[z] = lst1
                        Ucur.updateRow(row)
                        x += 1

    def SurroundingTotal():
        currentTime = str(datetime.datetime.today().strftime("%m_%d_%Y"))
        cumulative = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
        totalList = ["BrazoriaTOTAL", "FortBendTOTAL", "HarrisTOTAL", "HoustonTOTAL", "GalvestonTOTAL", "SurroundingAreaTOTAL"]
        TotalNum = len(totalList) - 1

        with arcpy.da.UpdateCursor(cumulative, totalList) as Ucur:
            for x in totalList:
                y = 0
                for row in Ucur:
                    z = 0
                    for num in row[0:TotalNum]:
                        if num == None:
                            num = 0
                        z += num
                        row[TotalNum] = z
                        Ucur.updateRow(row)
    DatasetUpdate()
    RunningTotal()
    SurroundingTotal()

def cumulativeRecovered():


    def DatasetUpdate():
        lst = ["Location", "Date", "CountType", "CaseCount"]
        points = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.EOC\\Horizon.DBO.COVID19_Cases"
        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
        lstDaily = ["Date", "CityofPearland", "BrazoriaCounty", "FortBendCounty", "HarrisCounty", "CityofHouston", "StateofTexas", "GalvestonCounty"]

        arcpy.DeleteRows_management("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Recovery")

        def DailyUpdate():

            mdate = str(datetime.date.today())
            rdate = str(datetime.date(2020, 3, 19))
            mdate1 = datetime.datetime.strptime(mdate, "%Y-%m-%d").date()
            rdate1 = datetime.datetime.strptime(rdate, "%Y-%m-%d").date()
            delta =  (mdate1 - rdate1).days
            dateList = list(range(0, delta+1))
            dateList.reverse()

            for x in dateList:
                pearlandRow = 0
                brazoriaRow = 0
                fbRow = 0
                harrisRow = 0
                houstonRow = 0
                texasRow = 0
                galvRow = 0
                currentDate = datetime.date.today() - datetime.timedelta(days = x)
                currentTime = currentDate.strftime("%m/%d/%Y")
                with arcpy.da.SearchCursor(points, lst) as Scur:
                        for row in Scur:
                            if row[1].strftime("%m/%d/%Y") == currentTime:
                                timeRow = row[1].strftime("%m/%d/%Y")
                                if row[2] == "Cumulative Recovered":
                                    if row[0] == "Pearland":
                                        pearlandRow = row[3]
                                    if row[0] == "Brazoria":
                                        brazoriaRow = row[3]
                                    if row[0] == "Fort Bend":
                                        fbRow = row[3]
                                    if row[0] == "Harris":
                                        harrisRow = row[3]
                                    if row[0] == "Houston":
                                        houstonRow = row[3]
                                    if row[0] == "Texas":
                                        texasRow = row[3]
                                    if row[0] == "Galveston":
                                        galvRow = row[3]
        
                        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Recovery"
                        lstCumulative = ['CoPTOTAL', 'BrazTOTAL', 'HarrisTOTAL', 'FBTOTAL', 'Date','GalvTOTAL' ]
                        lstValue = [pearlandRow, brazoriaRow, harrisRow, fbRow, timeRow, galvRow]
                        with arcpy.da.InsertCursor(pointsDaily, lstCumulative) as Icur:
                            Icur.insertRow(lstValue)

        DailyUpdate()

    def RunningTotal():
        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Recovery"
        lstDaily = ['CoPTOTAL', 'BrazTOTAL', 'HarrisTOTAL', 'FBTOTAL', "GalvTOTAL"]

        for z in [0, 1, 2, 3, 4]:
            with arcpy.da.SearchCursor(pointsDaily, lstDaily)as Scur:
                lst = []
                for row in Scur:
                    lst.append(row[z])  
                cumulative = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Recovery"
                totalList = ['CoP_REC', 'Braz_REC', 'Harris_REC', 'FB_REC', 'Galv_REC']
                with arcpy.da.UpdateCursor(cumulative, totalList) as Ucur:
                    x = 0
                    for row in Ucur:
                        if x == 0:
                            lst1 = lst[x]
                        else:
                            lst1 = lst[x] - lst[x-1]
                        row[z] = lst1
                        Ucur.updateRow(row)
                        x += 1

    def SurroundingTotal():
        currentTime = str(datetime.datetime.today().strftime("%m_%d_%Y"))
        cumulative = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Recovery"
        totalList = ['CoPTOTAL', 'BrazTOTAL', 'HarrisTOTAL', 'FBTOTAL', "GalvTOTAL", "SurroundingAreaTOTAL"]
        TotalNum = len(totalList) - 1

        with arcpy.da.UpdateCursor(cumulative, totalList) as Ucur:
            for x in totalList:
                y = 0
                for row in Ucur:
                    z = 0
                    for num in row[0:TotalNum]:
                        if num == None:
                            num = 0
                        z += num
                        row[TotalNum] = z
                        Ucur.updateRow(row)
    DatasetUpdate()
    RunningTotal()
    SurroundingTotal()

def cumulativeDeaths():


    def DatasetUpdate():
        lst = ["Location", "Date", "CountType", "CaseCount"]
        points = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.EOC\\Horizon.DBO.COVID19_Cases"
        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVIDDataset"
        lstDaily = ["Date", "CityofPearland", "BrazoriaCounty", "FortBendCounty", "HarrisCounty", "CityofHouston", "StateofTexas", "GalvestonCounty"]

        arcpy.DeleteRows_management("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Death")

        def DailyUpdate():

            mdate = str(datetime.date.today())
            rdate = str(datetime.date(2020, 3, 25))
            mdate1 = datetime.datetime.strptime(mdate, "%Y-%m-%d").date()
            rdate1 = datetime.datetime.strptime(rdate, "%Y-%m-%d").date()
            delta =  (mdate1 - rdate1).days
            dateList = list(range(0, delta+1))
            dateList.reverse()

            for x in dateList:
                pearlandRow = 0
                brazoriaRow = 0
                fbRow = 0
                harrisRow = 0
                houstonRow = 0
                texasRow = 0
                galvRow = 0
                currentDate = datetime.date.today() - datetime.timedelta(days = x)
                currentTime = currentDate.strftime("%m/%d/%Y")
                with arcpy.da.SearchCursor(points, lst) as Scur:
                        for row in Scur:
                            if row[1].strftime("%m/%d/%Y") == currentTime:
                                timeRow = row[1].strftime("%m/%d/%Y")
                                if row[2] == "Cumulative Deaths":
                                    if row[0] == "Pearland":
                                        pearlandRow = row[3]
                                    if row[0] == "Brazoria":
                                        brazoriaRow = row[3]
                                    if row[0] == "Fort Bend":
                                        fbRow = row[3]
                                    if row[0] == "Harris":
                                        harrisRow = row[3]
                                    if row[0] == "Houston":
                                        houstonRow = row[3]
                                    if row[0] == "Texas":
                                        texasRow = row[3]
                                    if row[0] == "Galveston":
                                        galvRow = row[3]
        
                        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Death"
                        lstCumulative = [ 'BrazTOTAL', 'HarrisTOTAL', 'FBTOTAL', 'Date','TexasTOTAL', 'CopTOTAL','GalvTOTAL' ]
                        lstValue = [brazoriaRow, harrisRow, fbRow, timeRow, texasRow, pearlandRow, galvRow]
                        with arcpy.da.InsertCursor(pointsDaily, lstCumulative) as Icur:
                            Icur.insertRow(lstValue)

        DailyUpdate()

    def RunningTotal():
        pointsDaily = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Death"
        lstDaily = [ 'BrazTOTAL', 'HarrisTOTAL', 'FBTOTAL', 'TexasTOTAL', 'CopTOTAL','GalvTOTAL' ]

        for z in [0, 1, 2, 3, 4, 5]:
            with arcpy.da.SearchCursor(pointsDaily, lstDaily)as Scur:
                lst = []
                for row in Scur:
                    lst.append(row[z])  
                cumulative = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Death"
                totalList = ['Braz_DEATH', 'Harris_DEATH', 'FB_DEATH', 'Texas_DEATH', 'CoP_DEATH', 'Galv_DEATH']
                with arcpy.da.UpdateCursor(cumulative, totalList) as Ucur:
                    x = 0
                    for row in Ucur:
                        if x == 0:
                            lst1 = lst[x]
                        else:
                            lst1 = lst[x] - lst[x-1]
                        row[z] = lst1
                        Ucur.updateRow(row)
                        x += 1

    def SurroundingTotal():
        currentTime = str(datetime.datetime.today().strftime("%m_%d_%Y"))
        cumulative = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\COVID_Death"
        totalList = ['BrazTOTAL', 'HarrisTOTAL', 'FBTOTAL', 'CoPTOTAL','GalvTOTAL', "SurroundingAreaTOTAL"]
        TotalNum = len(totalList) - 1
        print("yes")
        with arcpy.da.UpdateCursor(cumulative, totalList) as Ucur:
            for x in totalList:
                y = 0
                for row in Ucur:
                    z = 0
                    for num in row[0:TotalNum]:
                        if num == None:
                            num = 0
                        z += num
                        row[TotalNum] = z
                        Ucur.updateRow(row)
    DatasetUpdate()
    RunningTotal()
    SurroundingTotal()

def dailyConfirmed():
    currentDate = datetime.date.today()
    currentTime = currentDate.strftime("%m/%d/%Y")
    points = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\scratch.gdb\\COVID19_Cases"
    fields = ["Location", "Date", "CountType", "CaseCount"]
    dailyDict= {"Harris": 0, "Fort Bend": 0, "Brazoria": 0, "Texas": 0, "Pearland": 0}
    lst = []
    lst1 = []
    with arcpy.da.UpdateCursor(points, fields)as Ucur:
        for row in Ucur:
            lst.append([row[0], row[1], row[2]])
            for key, value in dailyDict.items():
                dailyDict[key] = row[3]
                print(dailyDict)
    #            if row[0] == key and row[1].strftime("%m/%d/%Y") == currentTime and row[2] == "Daily Confirmed":
    #                Ucur.updateRow((key, currentTime, "Daily Confirmed", value ))
    #for x in lst:
    #    if x[1].strftime("%m/%d/%Y") == currentTime and x[2] == "Daily Confirmed":
    #        lst1.append(x)

    #if len(lst1) == 0:
    #    for key, value in dailyDict.items():
    #        with arcpy.da.InsertCursor(points, fields) as Icur:
    #            Icur.insertRow((key, currentTime, "Daily Confirmed", value ))
main()
print(".")