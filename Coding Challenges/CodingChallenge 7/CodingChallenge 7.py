import csv
import arcpy
import math
import os

#set project parameters
spRef = arcpy.SpatialReference(4326)
arcpy.env.outputCoordinateSystem = spRef
arcpy.env.overwriteOutput = True

#this workspace will have your species CSV and your script
baseWorkspace = r'C:\Users\johnt801\PycharmProjects\Lab 7 Remixed'
arcpy.env.workspace = baseWorkspace
input_directory = arcpy.env.workspace
inCSV = r'SpeciesCSV.csv'
speciesList = []


#set up project folders

#temp files will have the separated species csvs, point shapefiles, and base fishnets
if not os.path.exists(os.path.join(input_directory, "temporary_files")):
    os.mkdir(os.path.join(input_directory, "temporary_files"))

#outputs will only have the final joined fishnets
if not os.path.exists(os.path.join(input_directory, "outputs")):
    os.mkdir(os.path.join(input_directory, "outputs"))


points = open(os.path.join(arcpy.env.workspace, inCSV),newline='')
pointsreader = csv.reader(points, delimiter=',')
lineCount = 0
for row in pointsreader:
    if row[5] not in speciesList:
        speciesList.append(row[5])

points.seek(0) #reset reader

#delete column name
speciesList.pop(0)

print("Species List: ")
for i in speciesList:
    print("- " + i)

#reset workspace to point to temporary files
arcpy.env.workspace = os.path.join(baseWorkspace,'temporary_files')

for species in speciesList:
    print("Making csv table for: " + species)
    with open('%s-output.csv' % species,mode = 'w', newline='') as csv2:
        csv_writer = csv.writer(csv2)

        #add column names
        csv_writer.writerow(['X','Y','Species'])

        for row in pointsreader:
            if row[5] == species:
                csv_writer.writerow([row[4],row[3],row[5]])
    points.seek(0) #reset reader


print("Making shapefile layers...")
for species in speciesList:

    #define tool parameters
    inTable = '%s-output.csv' % species
    x_coords = 'X'
    y_coords = 'Y'
    z_coords = ''
    out_Layer = '%s' % species
    saved_Layer = '%s-saved.shp' % species

    lyr = arcpy.MakeXYEventLayer_management(inTable,x_coords,y_coords,out_Layer,spRef,z_coords)
    arcpy.CopyFeatures_management(lyr,saved_Layer)


print("Making fishnets...")
for species in speciesList:

    # define fishnet parameters
    desc = arcpy.Describe('%s-saved.shp' % species)
    origin = str(desc.extent.XMin) + ' ' + str(desc.extent.YMin)
    y_coord = str(desc.extent.XMin) + ' ' + str(desc.extent.XMin + 10)

    distance = math.sqrt(math.pow(desc.extent.XMax-desc.extent.XMin,2) + math.pow(desc.extent.YMax-desc.extent.YMin,2))
    cellX = 0
    cellY = 0

    if distance < 5:
        cellX = '1'
        cellY = '1'
    else:
        cellX = "2.5"
        cellY = "2.5"

    opposite_corner = str(desc.extent.XMax) + ' ' + str(desc.extent.YMax)

    out_Fishnet = '%s-fishnet.shp' % species

    fish = arcpy.CreateFishnet_management(out_Fishnet,origin,y_coord,cellX,cellY,'','',opposite_corner,geometry_type="POLYGON",labels=None)


#spatial join operation
print("Joining layers...")

for species in speciesList:
    arcpy.SpatialJoin_analysis("%s-fishnet.shp" % species, "%s-saved.shp" % species, os.path.join(baseWorkspace,'outputs',"%s-joinedFishnet.shp" % species))

points.close()