import arcpy 
import datetime
arcpy.OverwriteOutput = True

#Creating Local fgdb layers due to lack of GeoAnalystics server
covidLayer = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\ImageTrendCases"
hexagonLayer = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\ImageTrendCases_hex"

#Need to delete layers for Feature to Feature and Aggregate Points
arcpy.Delete_management(covidLayer)
arcpy.Delete_management(hexagonLayer)

#Horizon point Layer that gets updated through GeoMAX
covidLayerSDE = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Owner.sde\\Horizon.DBO.EOC\\Horizon.DBO.ImageTrendCases"

#Horizon polygon Layer that will get updated
covidLayerHEX = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Owner.sde\\Horizon.DBO.EOC\\Horizon.DBO.SymptomaticCases"

#Split Path and Name of covidLayer for use in FeatureClasstoFeatureClass_conversion
pathFTF = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb"
nameFTF = "ImageTrendCases"

#Need Current time for query ultimatley used in FCtoFC
currentDatetime = datetime.datetime.now()
query = "Incident_Unit_Notified_By_Dispa >= '3-1-2020 00:00:00' and Incident_Unit_Notified_By_Dispa <= '{}' ".format(currentDatetime)
arcpy.FeatureClassToFeatureClass_conversion(covidLayerSDE, pathFTF, nameFTF, query)

#Aggregate Points makes the Hexagon Layer based on covidLayerSDE points (Even if numbers stay the same hexagons will move daily, we have no control over this)
arcpy.gapro.AggregatePoints(covidLayer, hexagonLayer, "BIN", None, "Hexagon", "1500 feet")

#AlterField to make append work properly (Moving from FGDB to Horizon caused COUNT to become COUNT_ due to COUNT being reserved)
arcpy.AlterField_management(hexagonLayer, "COUNT", "COUNT_")

#Truncate and Append Layer due to hexagons being live in a map service
arcpy.TruncateTable_management(covidLayerHEX)
arcpy.Append_management(hexagonLayer, covidLayerHEX)
print("done")