import arcpy,os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BufferFolder,CompositeFolders,ClipAllToSA]

class BufferFolder(object):
    def __init__(self):

        self.label = "BufferFolders"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []
        input_points = arcpy.Parameter(name="input_points",
                                       displayName="Input Points",
                                       datatype="DEFolder",
                                       parameterType="Required",
                                       direction="Input",
                                       )
        input_points.value = r'C:\Users\johnt801\Documents\TestPointsNEW'
        params.append(input_points)
        buffer_dist = arcpy.Parameter(name="buffer_dist",
                                      displayName="Buffer Distance (m)",
                                      datatype="Double",
                                      parameterType="Required",
                                      direction="Input",
                                      )
        buffer_dist.value = 50
        params.append(buffer_dist)
        output_buffer = arcpy.Parameter(name="output_buffer",
                                        displayName="Output folder for buffered points",
                                        datatype="DEFolder",
                                        parameterType="Required",
                                        direction="Output",
                                        )
        output_buffer.value = r'C:\Users\johnt801\Documents\TestBuffer'
        params.append(output_buffer)

        return params

    def execute(self, parameters, messages):
        import arcpy,os

        # define shapefile object location
        inputPoints = parameters[0].valueAsText

        arcpy.env.workspace = inputPoints
        arcpy.env.overwriteOutput = True
        points = arcpy.ListFeatureClasses()


        # define parameters
        buffer = parameters[1].valueAsText

        bufferDist = str(buffer) + ' Meters'

        for layer in points:
            arcpy.AddMessage("Buffering %s by " % layer + buffer + " meters..." )
            outputBuffer = os.path.join(parameters[2].valueAsText,
                                        str(layer).split('.')[0] + '_%smBuffer.shp' % str(buffer))

            # perform buffer
            arcpy.Buffer_analysis(layer, outputBuffer, bufferDist, dissolve_option='NONE')

        arcpy.AddMessage("Buffer completed succesfully!")

        return



class CompositeFolders(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CompositeFolders"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []
        inputFolder = arcpy.Parameter(name="inputFolder",
                                 displayName="Input Master Folder of Rasters",
                                 datatype="Folder",
                                 parameterType="Required",
                                 direction="Input",
                                 )
        inputFolder.value = r"E:\testRasters"
        params.append(inputFolder)
        outputFolder = arcpy.Parameter(name="outputFolder",
                                 displayName="Output folder of composites",
                                 datatype="Folder",
                                 parameterType="Required",
                                 direction="Output",
                                 )
        outputFolder.value = r"E:\outputComposites(TIF)"
        params.append(outputFolder)

        return params

    def execute(self, parameters, messages):
        import arcpy, os

        basePth = parameters[0].valueAsText
        arcpy.env.workspace = basePth
        arcpy.env.overwriteOutput = True

        outPath = parameters[1].valueAsText
        if not os.path.exists(outPath):
            os.makedirs(outPath)

        folders = []
        for i in os.listdir(arcpy.env.workspace):
            if i.isnumeric():
                folders.append(i)
        print(folders)

        for raster in folders:
            arcpy.env.workspace = os.path.join(basePth, raster)
            tifs = []
            for i in arcpy.ListRasters('*', 'TIF'):
                if i[42].isnumeric():
                    tifs.append(i)
            tifs.sort()

            # move B10 and B11 to back of the list to order correctly
            tifs.append(tifs.pop(1))
            tifs.append(tifs.pop(1))

            # do dumb string concatenation thing to get the bands ready for input
            bandInput = ''
            for i in tifs:
                bandInput = bandInput + os.path.join(basePth, raster, i) + ';'

            print("Making composite of raster: " + str(raster))
            arcpy.management.CompositeBands(bandInput, os.path.join(outPath, 'Comp%s.tif' % raster))
            print("Done with raster: " + str(raster))
        return

class ClipAllToSA(object):
    def __init__(self):

        self.label = "ClipAllToSA"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []
        input_shapes = arcpy.Parameter(name="input_shapes",
                                       displayName="Master folder of shapefiles to be clipped",
                                       datatype="DEFolder",
                                       parameterType="Required",
                                       direction="Input",
                                       )
        input_shapes.value = r'E:\TestShapefiles'
        params.append(input_shapes)
        inputSA = arcpy.Parameter(name="inputSA",
                                      displayName="Input Study Area",
                                      datatype="GPFeatureLayer",
                                      parameterType="Required",
                                      direction="Input",
                                      )
        inputSA.value = r'E:\CampusSA\CampusSA.shp'
        params.append(inputSA)
        output_folder = arcpy.Parameter(name="output_folder",
                                        displayName="Output folder for clipped layers",
                                        datatype="DEFolder",
                                        parameterType="Required",
                                        direction="Output",
                                        )
        output_folder.value = r'E:\testOutputs'
        params.append(output_folder)

        return params

    def execute(self, parameters, messages):
        import arcpy, os

        inputShapes = parameters[0].valueAsText
        inputSA = parameters[1].valueAsText
        outputFolder = parameters[2].valueAsText

        arcpy.env.workspace = inputShapes
        arcpy.env.overwriteOutput = True

        for shape in arcpy.ListFeatureClasses('*'):
            arcpy.AddMessage('Clipping %s...' % shape)
            outShape = os.path.join(outputFolder, '%s_Clipped.shp' % shape.split('.')[0])
            arcpy.analysis.Clip(shape, inputSA, outShape)

        return

# This code block allows you to run your code in a test-mode within PyCharm, i.e. you do not have to open the tool in
# ArcMap. This works best for a "single tool" within the Toolbox.
def main():
   tool = BufferFolder()
   tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
   main()
