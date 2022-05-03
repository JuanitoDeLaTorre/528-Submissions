import csv
import arcpy
import os

##############################################
# This script makes multiple CSVs from a combined
# CSV and asks the user which shapefile(s) they want
# created and if they want a buffer applied. The
# user can specify any sized buffer they want.
##############################################


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

def ShapefileMakr(species,bufferDist):

    # define tool parameters
    inTable = '%s-output.csv' % species
    x_coords = 'X'
    y_coords = 'Y'
    z_coords = ''
    out_Layer = '%s' % species
    saved_Layer = '%s-saved.shp' % species

    lyr = arcpy.MakeXYEventLayer_management(inTable, x_coords, y_coords, out_Layer, spRef, z_coords)
    arcpy.CopyFeatures_management(lyr, saved_Layer)

    #if bufferDist is non zero number, make a buffered shapefile based on that number
    if int(bufferDist) > 0:
        shapefile = os.path.join(arcpy.env.workspace,'%s-saved.shp' % species)
        outputShapefile = '%s-Buffered(%sm).shp' % (species,bufferDist)
        distanceField = "%s Meters" % bufferDist

        arcpy.Buffer_analysis(shapefile, outputShapefile, distanceField)


while(True):

    while(True):
        print("Which species would you like to make a shapefile for? ")
        for i in speciesList:
            print("- " + i)
        speciesSelect = input()
        if speciesSelect not in speciesList:
            print("Sorry, %s isn't in your species list. Try again.\n" % speciesSelect)
        else:
            break


    buff = input("Would you like to buffer the shapefile? (Y/N)")


    if "Y" in buff:
        buffDistance = input("What would you like your buffer distance (m) to be for the %s shapefile?" % speciesSelect)

        ShapefileMakr(speciesSelect,buffDistance)
    else:
        ShapefileMakr(speciesSelect,0)

    cont = input("\nWould you like to make another shapefile? (Y/N)")
    if "N" in cont:
        break


print("Thank you for using the shapefile creator!")
points.close()