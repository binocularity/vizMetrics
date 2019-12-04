import cv2
import pySaliencyMap
import numpy as np
from skimage import util, color
import math



def low_res(inFile, outFile):

    image = cv2.imread(inFile)

    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliencyLoResMap) = saliency.computeSaliency(image)

    saliencyLoResMap = saliencyLoResMap * 255
    cv2.imwrite( outFile, saliencyLoResMap )

    (thresh, saliencyLoResMap) = cv2.threshold(saliencyLoResMap, 63, 255, cv2.THRESH_BINARY)

    total = saliencyLoResMap.shape[0] * saliencyLoResMap.shape[1] # Total number of pixels
    number_salient = np.count_nonzero( saliencyLoResMap ) # Number of salient pixels

    saliency_density = float(number_salient ) / float( total ) # Ratio

    return saliency_density

def hi_res(inFile, outFile):



    image = cv2.imread(inFile)

    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyHiResMap) = saliency.computeSaliency(image)

    saliencyHiResMap = saliencyHiResMap * 255
    #saliencyHiResMap = cv2.threshold(saliencyHiResMap.astype("uint8"), 64, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    cv2.imwrite( outFile, saliencyHiResMap )

    #(thresh, saliencyHiResMap) = cv2.threshold(saliencyHiResMap, 64, 255, cv2.THRESH_BINARY)

    total = saliencyHiResMap.shape[0] * saliencyHiResMap.shape[1] # Total number of pixels
    number_salient = np.count_nonzero( saliencyHiResMap ) # Number of salient pixels

    saliency_density = float(number_salient ) / float( total ) # Ratio
    return saliency_density

def aalto(inFile, outFile):

    print("***")
    print(inFile, ":::",outFile)
    print("***")

    # Initialize
    img = cv2.imread(inFile)

    imgsize = img.shape
    img_width = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    saliency_map = sm.SMGetSM(img)
    saliency_map = saliency_map * 255

    cv2.imwrite( outFile, saliency_map )

    (thresh, saliency_map) = cv2.threshold(saliency_map, 63, 255, cv2.THRESH_BINARY)

    total = saliency_map.shape[0] * saliency_map.shape[1] # Total number of pixels
    number_salient = np.count_nonzero( saliency_map ) # Number of salient pixels

    saliency_density = float(number_salient ) / float( total ) # Ratio
    return saliency_density


