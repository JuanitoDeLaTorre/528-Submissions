import csv
import arcpy
import math

#set project parameters
spRef = arcpy.SpatialReference(4326)
arcpy.env.outputCoordinateSystem = spRef
arcpy.env.overwriteOutput = True

arcpy.env.workspace = r'C:\Users\johnt801\Downloads\Test'
speciesList = []


points = open(str(arcpy.env.workspace + r'\SpeciesCSV.csv'),newline='')
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



print("Making fishnet...")
for species in speciesList:

    desc = arcpy.Describe('%s-saved.shp' % species)


    # define fishnet parameters
    distance = math.sqrt(math.pow(desc.extent.XMax-desc.extent.XMin,2) + math.pow(desc.extent.YMax-desc.extent.YMin,2))
    cellX = 0
    cellY = 0

    if distance < 5:
        cellX = '0.5'
        cellY = '0.5'
    else:
        cellX = "2.5"
        cellY = "2.5"

    origin = str(desc.extent.XMin - float(cellX)) + ' ' + str(desc.extent.YMin - float(cellY))
    y_coord = str(desc.extent.XMin - float(cellX)) + ' ' + str(desc.extent.YMin + 10 - float(cellX))
    opposite_corner = str(desc.extent.XMax + float(cellX)) + ' ' + str(desc.extent.YMax + float(cellX))

    out_Fishnet = '%s-fishnet.shp' % species

    fish = arcpy.CreateFishnet_management(out_Fishnet,origin,y_coord,cellX,cellY,'','',opposite_corner,geometry_type="POLYGON",labels="NO_LABELS")


#spatial join operation
print("Joining layers...")

for species in speciesList:
    arcpy.SpatialJoin_analysis("%s-fishnet.shp" % species, "%s-saved.shp" % species, "%s-joinedFishnet.shp" % species)

#delete supporting shapefiles
for species in speciesList:
    arcpy.Delete_management("%s-saved.shp" % species)
    arcpy.Delete_management("%s-output.shp" % species)
    arcpy.Delete_management("%s-fishnet.shp" % species)

points.close()