import csv
import math, random, os
import arcpy

############################################
#   This program models three proxy distributions in RI of user-defined size,
#   makes point layers, buffers them, and summarizes their "habitat" based on
#   a 2011 land cover shapefile by outputting a table with cover type area (acres)
#   and the percentage of the "habitat" that the cover type represents

#   The only two things the user needs to change is the path where the shapefile
#   is and the working GDB

#   John Thomas, 2022
#############################################

##########CHANGE THIS
dataPth = r"C:\Users\johnt801\Downloads\Data"
LandCoverFC = dataPth + r"\Land_Use_and_Land_Cover_(2011).shp"


if not os.path.exists(dataPth + '\Outputs'):
    os.makedirs(dataPth + '\Outputs')

outputFolder = dataPth + '\Outputs'
arcpy.env.workspace = outputFolder

###########CHANGE THIS
homeGDB = r'C:\Users\johnt801\Documents\ArcGIS\Projects\Test\Test.gdb'

spRef = arcpy.SpatialReference(4326)
arcpy.env.outputCoordinateSystem = spRef
arcpy.env.overwriteOutput = True

def randCoords(numObservations,Xhigh,Xlow,Yhigh,Ylow):
    X = []
    Y = []
    XY = []
    for i in range(numObservations):
        X.append(round(random.uniform(Xhigh,Xlow),4))
        Y.append(round(random.uniform(Yhigh,Ylow),4))
    for i in range(len(X)):
        XY.append(str(X[i]) + ' ' + str(Y[i]))
    return XY

#top left (X: -71.79,-71.64 Y: 42,41.83)

#central (X: -71.78,-71.62 Y: 41.85,41.79)

#around campus/N Kingstown (X: -71.71,-71.49 Y: 41.58,41.49)

numObs = int(input("Enter the amount of species you want for each distribution: "))
buffDist = input("Choose buffer distance (m): ")
speciesList = [randCoords(numObs,-71.69,-71.49,41.58,41.49),randCoords(numObs,-71.73,-71.64, 41.70,41.62),randCoords(numObs,-71.73,-71.62, 41.85,41.79)]

csvList = []

#make csv files based on user defined species
for i in speciesList:

    speciesName = input("Enter species name: ")

    with open("%s_coordinates.csv" % speciesName, 'w', newline='') as points:
        csvWriter = csv.writer(points)
        csvWriter.writerow(['X', 'Y', 'SpeciesName'])

        #split combined coordinates and write CSV rows
        for j in range(len(i)):
            csvWriter.writerow([float(i[j].split(' ')[0]),float(i[j].split(' ')[1]),str(speciesName)])
    csvList.append("%s_coordinates.csv" % speciesName)

#making species point shapefiles
for csv in csvList:

    #define tool parameters
    inTable = str(csv)
    x_coords = 'X'
    y_coords = 'Y'
    z_coords = ''
    speciesName = csv.split('_')[0]
    saved_PointsLayer = '%s-saved.shp' % speciesName

    print("Creating random distribution for: %s. . ." % speciesName)
    lyr = arcpy.MakeXYEventLayer_management(inTable,x_coords,y_coords,speciesName,spRef,z_coords)
    arcpy.CopyFeatures_management(lyr,saved_PointsLayer)

    print("Buffering distribution for: %s. . ." % speciesName)
    bufferLyr = arcpy.Buffer_analysis(saved_PointsLayer,'%s_bufferedPoints.shp' % csv.split('_')[0], "%s Meters" % buffDist,dissolve_option = "NONE")

    print("Summarizing habitat composition for: %s. . ." % speciesName)
    summary = arcpy.analysis.SummarizeWithin(bufferLyr,LandCoverFC, homeGDB + "\%s_bufferedPoints_SummarizeWithin" % speciesName, "KEEP_ALL", None, "ADD_SHAPE_SUM", "ACRES", "Descr_2011", "NO_MIN_MAJ","ADD_PERCENT", homeGDB + "\%s_Summary" % speciesName)
    arcpy.Delete_management(homeGDB + "\%s_bufferedPoints_SummarizeWithin" % speciesName)