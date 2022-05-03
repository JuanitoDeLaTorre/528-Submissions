import arcpy,os

#make output directory (base folder where data/script is)
basePath = r'C:\Users\johnt801\Downloads\ALL_FILES\Step_2_Data'
arcpy.env.workspace = basePath
arcpy.env.overwriteOutput = True

#create output NDVI folder
outPath = os.path.join(arcpy.env.workspace,'outputNDVI')
if not os.path.exists(outPath):
    os.makedirs(outPath)

#get list of image folders
print("Getting image folders...")
imageFolders = []

#assume eighth character in image folder is numeric (year)
[imageFolders.append(x) for x in os.listdir(arcpy.env.workspace) if x[8].isnumeric()]

#loop through folders and create NDVI based on provided band rasters
for folder in imageFolders:

    #reassign workspace to current year
    arcpy.env.workspace = os.path.join(basePath,folder)
    listRaster = arcpy.ListRasters('*','TIF')
    prefix = listRaster[0][0:42]

    band5 = prefix + '5.tif'
    band4 = prefix + '4.tif'

    print("Creating NDVI for folder %s...\n" % folder)

    outNDVI = arcpy.sa.RasterCalculator([band5,band4],['NIR','Red'],'(NIR-Red)/(NIR+Red)','FirstOf')
    outNDVI.save(outPath + "\\NDVI_%s" % folder[7:])

print("All NDVIs created successfully!")
