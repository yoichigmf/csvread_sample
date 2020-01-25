## QGIS ライブラリを利用してCSVファイルを画像にプロットするサンプル

csv_read.bat    Pythonプログラムを起動する bat ファイル

readcsv.py    csv read と画像プロットのサンプル

hinan.csv    CSVファイルサンプル  国土数値情報の岡山県避難施設

hinan.tif    プロットされた画像


## 実行方法

QGIS3.x (OSGeo4wでも可)がインストールされている端末に上記ファイルをコピー
csv_read.bat   readcsv.py  の各種パラメータを調整

QGIS の Python3 が起動できるコマンドプロンプトの起動  
(stand alone install の場合はインストールディレクトリにある OSGeo4W.bat    C:\Program Files\QGIS 3.4\OSGeo4W.bat
OSGeo4w install の場合は OSGeo4w インストールディレクトリにある OSGeo4W.bat    C:\OSGeo4W64\OSGeo4W.bat ) を起動


コマンドプロンプト内でバッチコマンド  csv_read.bat  を実行


## 設定パラメータ解説

### csv_read.bat

<pre>
	@echo off 
	
	set OSGEO4W_ROOT=C:\OSGeo4W64
	
	call "%OSGEO4W_ROOT%\bin\o4w_env.bat" 
	call "%OSGEO4W_ROOT%\bin\qt5_env.bat" 
	call "%OSGEO4W_ROOT%\bin\py3_env.bat" 
 	
	set PATH=%OSGEO4W_ROOT%\bin;%OSGEO4W_ROOT%\apps\qgis-ltr\bin;C:\OSGeo4W64\apps\Qt5\bin;%PATH%
	set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%PYTHONPATH%
	set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr
	set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins
	python3 readcsv.py
	
	echo end
</pre>

- OSGEO4W_ROOT  QGIS またはOSGeo4W インストールディレクトリ
- PATH  プログラム実行パス
- PYTHONPATH  python  実行パス
- QGIS_PREFIX_PATH   QGISのインストールパス
- QT_QPA_PLATFORM_PLUGIN_PATH  Qt5プラグインインストールパス


### readcsv.py

<pre>
import os
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import QAction, QMainWindow
from qgis.PyQt.QtCore import Qt
	
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

</pre>


- uri='file:///C:/work/csvtest/hinan.csv?delimiter=,&encoding=UTF-8&xField=x&yField=y'  CSVファイルの記述
  https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/loadlayer.html#id1
- output_dir = 'C:/work/csvtest/hinan.tif'   出力イメージファイル名