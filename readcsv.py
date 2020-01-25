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


output_dir = 'C:/work/csvtest/hinan.tif'

csvlayer = QgsVectorLayer(uri, "hinan", "delimitedtext")


#    CSV レイヤのオープン成功
if csvlayer.isValid():
         canvas = QgsMapCanvas()
         
         canvas.setCanvasColor(Qt.white)
# enable this for smooth rendering
         canvas.enableAntiAliasing(True)

         print("Layer load OK")

         
         canvas.setExtent(csvlayer.extent())
         
         canvas.setLayers([csvlayer])
         
         canvas.refresh()
             

         # rendering my map canvas to tif image
         settings = canvas.mapSettings()
         settings.setLayers([csvlayer])
         job = QgsMapRendererParallelJob(settings)
         job.start()
         job.waitForFinished()
         image = job.renderedImage()
         image.save(output_dir)


         
         #QgsProject.instance().addMapLayer(csvlayer)
         #features = csvlayer.getFeatures()

         #for feature in features:
         #      attrs = feature.attributes()
         #      print(attrs)
               
               

#   csv レイヤオープン失敗
else:
     print("csv Layer failed to load!")
     
     
     
# Write your code here to load some layers, use processing
# algorithms, etc.

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()