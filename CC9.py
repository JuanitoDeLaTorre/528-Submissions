import arcpy
import csv
import pandas
import glob

points = r"C:\Users\johnt801\PycharmProjects\CC9\RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp"
arcpy.env.workspace = r'C:\Users\johnt801\PycharmProjects\CC9'
arcpy.env.overwriteOutput = True

descPoints = arcpy.Describe(points)
spRef = descPoints.spatialReference
fieldNames = []
uniqueSpecies = []

for field in descPoints.fields:
     fieldNames.append(field.name)

print(fieldNames)

overallCount = 0
photoCount = 0
photoIndices = []
photoCoords = []
nonphotoIndices=[]
nonphotoCoords = []

fields = ['OBJECTID','photo','SHAPE@X','SHAPE@Y']

print("Filtering photo/non photo data points...")
with arcpy.da.SearchCursor(points,fields) as curs:
    for i in curs:
        overallCount += 1

        if 'y' in i[1]:
            photoCount += 1
            photoIndices.append(i[0])
            photoCoords.append([i[2],i[3]])
        else:
            nonphotoIndices.append(i[0])
            nonphotoCoords.append([i[2], i[3]])

#getting count of unique species
with arcpy.da.SearchCursor(points,'Species') as species:
    for i in species:
        if i not in uniqueSpecies:
            uniqueSpecies.append(i)

print("Data summary:\n")
print("Overall count: " + str(overallCount))
print("Points with photos: " + str(photoCount))
print("Points without photos: " + str(overallCount - photoCount))

#subtract 3 for blank values, unknown values, and 'other' values
print("Unique species: " + str(len(uniqueSpecies) - 3) + '\n')

print('Creating CSVs...\n')
with open("Photo_Data.csv",'w+',newline='') as csvOK:
    csvRiter = csv.writer(csvOK)
    csvRiter.writerow(fieldNames)

    with arcpy.da.SearchCursor(points,'*') as curs2:
        for i in curs2:
            for j in photoIndices:
                if i[2] == j:
                    csvRiter.writerow(i)

with open("NonPhoto_Data.csv",'w+',newline='') as csvOK2:
    csvRiter = csv.writer(csvOK2)
    csvRiter.writerow(fieldNames)

    with arcpy.da.SearchCursor(points,'*') as curs2:
        for i in curs2:
            for j in nonphotoIndices:
                if i[2] == j:
                    csvRiter.writerow(i)

df = pandas.read_csv(r'C:\Users\johnt801\PycharmProjects\CC9\Photo_Data.csv')

# updating the column value/data
df['X'] = '0.0'
df['Y'] = '0.0'

for i in range(len(photoCoords)):
    df.loc[i,'X'] = photoCoords[i][0]
    df.loc[i,'Y'] = photoCoords[i][1]

# writing into the file
df.to_csv("Photo_Data.csv", index=False)

df2 = pandas.read_csv(r'C:\Users\johnt801\PycharmProjects\CC9\NonPhoto_Data.csv')

df2['X'] = '0.0'
df2['Y'] = '0.0'

for i in range(len(nonphotoCoords)):
    df2.loc[i, 'X'] = nonphotoCoords[i][0]
    df2.loc[i, 'Y'] = nonphotoCoords[i][1]

# writing into the file
df2.to_csv("NonPhoto_Data.csv", index=False)

print("Making layers from photo points / non photo points...\n")
inTable = r'C:\Users\johnt801\PycharmProjects\CC9\Photo_Data.csv'
x_coords = 'X'
y_coords = 'Y'
out_Layer = 'PhotoPoints'
saved_Layer = 'PhotoPoints'
z_coords = ''

lyr = arcpy.MakeXYEventLayer_management(inTable,x_coords,y_coords,out_Layer,spRef,z_coords)
arcpy.CopyFeatures_management(lyr,saved_Layer)

inTable = r'C:\Users\johnt801\PycharmProjects\CC9\NonPhoto_Data.csv'

x_coords = 'X'
y_coords = 'Y'
out_Layer = 'NonPhotoPoints'
saved_Layer = 'NonPhotoPoints'
z_coords = ''

lyr = arcpy.MakeXYEventLayer_management(inTable,x_coords,y_coords,out_Layer,spRef,z_coords)
arcpy.CopyFeatures_management(lyr,saved_Layer)

print("Layer creation done! Shapefiles located at: " + str(arcpy.env.workspace))



