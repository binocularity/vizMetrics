#
#
# vizMetrics - an interactive toolset for calculating visualization metrics
#
#
#

import os

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout 
from kivy.properties import StringProperty

from saliencyMetric import low_res, hi_res, aalto

pathForImages = "C:/Users/nickh/OneDrive/Newcastle/Research/MetricsOfVisualization/vizMetrics/Images/"
generatedImages = "C:/Users/nickh/OneDrive/Newcastle/Research/MetricsOfVisualization/vizMetrics/_Images/"
currentFile = "default.png"


class aaltoSaliencyButton(Button):
    # Create a property to allow saliency image file name to be set.
    aaltoSaliencyImage = StringProperty('blank.png')

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)

    def saliency_aalto(self):
        global pathForImages
        global generatedImages
        global currentFile
        
        fName, fExt = os.path.splitext(currentFile)
        
        self.aaltoSaliencyImage = fName+'_aalto_saliency'+fExt

        inputFile = pathForImages + currentFile
        saliencyFile = generatedImages + self.aaltoSaliencyImage

        saliencyDensityVal = aalto(inputFile,saliencyFile)
        print( saliencyDensityVal )


class highSaliencyButton(Button):
    # Create a property to allow saliency image file name to be set.
    highSaliencyImage = StringProperty('blank.png')

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)

    def saliency_high(self):
        global pathForImages
        global generatedImages
        global currentFile
        
        fName, fExt = os.path.splitext(currentFile)
        
        self.highSaliencyImage = fName+'_high_saliency'+fExt

        inputFile = pathForImages + currentFile
        saliencyFile = generatedImages + self.highSaliencyImage

        saliencyDensityVal = hi_res(inputFile,saliencyFile)
        print( saliencyDensityVal )


class vizMetrics(TabbedPanel):

    def select(self, *args):
        global currentFile
        try: 
            file =  args[1][0]
            currentFile = os.path.basename(file)
            self.label.text = os.path.basename(file)
        except: pass

    pass

class vizMetricsApp(App):

    global pathForImages
    global generatedImages

    pathToImages = pathForImages
    pathToGenerated = generatedImages

    print( "vizMetrics I : starting interface " )

    def build(self):
        return vizMetrics()

#
# Defaults for screen size and app startup
#
from kivy.config import Config
Config.set('graphics', 'width', '1422')
Config.set('graphics', 'height', '774')

if __name__ == '__main__':
    vizMetricsApp().run()