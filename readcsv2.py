import os
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import QAction, QMainWindow
from qgis.PyQt.QtCore import Qt

#import processing

# Supply the path to the qgis install location
#
#      QGIS インストール位置を環境変数 QGIS_PREFIX_PATH から取得
qgis_installed=os.environ['QGIS_PREFIX_PATH']




#              QGIS インストールパス指定
QgsApplication.setPrefixPath(qgis_installed, True)


# Create a reference to the QgsApplication.
# Setting the second argument to True enables the GUI.  We need
# this since this is a custom application.

qgs = QgsApplication([], True)

# load providers
qgs.initQgis()

uri='file:///C:/work/csvtest/hinan.csv?delimiter=,&encoding=UTF-8&xField=x&yField=y'


uri_shp='C:/work/csvtest/shp/pref.shp'


output_dir = 'C:/work/csvtest/hinan2.tif'


canvas = QgsMapCanvas()
canvas.setCanvasColor(Qt.white)
# enable this for smooth rendering
canvas.enableAntiAliasing(True)

layerArray = []


csvlayer = QgsVectorLayer(uri, "hinan", "delimitedtext")
#    CSV レイヤのオープン成功
if csvlayer.isValid():

         layerArray.append( csvlayer )
         

         print("CSV Layer load OK")
         
         canvas.setExtent(csvlayer.extent())

#   csv レイヤオープン失敗
else:
     print("csv Layer failed to load!")
     
     
shp_layer  = QgsVectorLayer(uri_shp, "JPmap", "ogr")
#    SHP レイヤのオープン成功
if shp_layer.isValid():
     print("SHP  Layer load OK")
     
     layerArray.append( shp_layer )
     
#   SHP レイヤオープン失敗
else:
     print("SHP Layer failed to load!")
     

  
canvas.setLayers(layerArray)
         
canvas.refresh()
             

         # rendering my map canvas to tif image
settings = canvas.mapSettings()
settings.setLayers(layerArray)
job = QgsMapRendererParallelJob(settings)
job.start()
job.waitForFinished()
image = job.renderedImage()
image.save(output_dir)

   
     
# Write your code here to load some layers, use processing
# algorithms, etc.

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()