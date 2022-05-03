# OVERALL COMMENT ABOUT YOUR SCRIPT
# Jonathan Thomas - March 2022

import arcpy
from arcpy import env

#allow overwrite
env.overwriteOutput = True

#define shapefile object location
vegetation = r"C:\Data\Students_2022\Thomas\Coding_Challenge_4\AD-Run\Submerged_Aquatic_Vegetation__SAV__in_RI_Coastal_Waters.shp"

#define parameters
buffer = input("Choose a buffer distance (m): ")
bufferDist = str(buffer) + ' Meters'
outputBuffer = r'C:\Data\Students_2022\Thomas\Coding_Challenge_4\AD-Run\SubmergedBuffer_' + str(buffer) + 'm.shp'

#perform buffer
arcpy.Buffer_analysis(vegetation,outputBuffer,bufferDist,dissolve_option='ALL')

arcpy.AddMessage("Buffer completed succesfully!")