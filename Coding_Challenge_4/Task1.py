import arcpy
from arcpy import env

#allow overwrite
env.overwriteOutput = True

#define shapefile object location
vegetation = r"C:\Users\johnt801\Downloads\Submerged_Aquatic_Vegetation_(SAV)_in_RI_Coastal_Waters_(2006)\AquaticVegetationReproject.shp"

#define parameters
buffer = input("Choose a buffer distance (m): ")
bufferDist = str(buffer) + ' Meters'
outputBuffer = r'C:\Users\johnt801\Downloads\OutputFiles\SubmergedBuffer ' + str(buffer) + 'm.shp'

#perform buffer
arcpy.Buffer_analysis(vegetation,outputBuffer,bufferDist,dissolve_option='ALL')

arcpy.AddMessage("Buffer completed succesfully!")