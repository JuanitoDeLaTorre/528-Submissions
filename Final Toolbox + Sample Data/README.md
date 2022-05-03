## Toolbox Description

This toolbox is designed to speed up the workflow of common vector and raster operations by allowing large amounts of data to be processed at once.

### Tool 1: Buffer Folder

Takes in a folder of point shapefiles, buffers them all by a defined distance, and then outputs the resulting polygons to a defined output folder.

Inputs:
- Folder of any number of point shapefiles
- Double representing desired buffer distance in meters
- Output folder path

Sample Data:
- Three point shapefiles in a single folder

### Tool 2: Clip All to SA

Often in the early stages of projects, the clipping of multiple shapefiles to a study area is needed. It can be tedious to do one at a time, so this tool clips 
all shapefiles in a folder to a defined study area shapefile and then outputs the clipped shapefiles to a defined folder.

Inputs:
- Folder of any number of polygon shapefiles
- Study area shapefile
- Output folder path

Sample Data:
- Sample study area (campus) and three shapefiles to be clipped (roads, buildings, and RI forest habitat)

### Tool3: Composite Folder

The Composite Bands tool in ArcGIS is sometimes frustrating to use because each band's TIF must be selected individually. This tool takes a folder of Landsat band folders, 
sorts the bands, composites the bands, and outputs the composite TIFs in a defined folder. Because of character limits in the Composite Bands tool, the entire raster name could
not be output, so only the date is used (e.g. if a raster is named LC08_L1TP_012031_20150201_20170301_01_T1_B1, only the folder name (201502) will be used)

Inputs:
- Master folder of any number of Landsat 11-band TIF folders
- Output folder for composite rasters

Sample Data:
- Folder of five Landsat 11-band TIF folders