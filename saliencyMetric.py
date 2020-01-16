import cv2
import pySaliencyMap
import numpy as np
from skimage import util, color
import math



def low_res(inFile, outFile):

    image = cv2.imread(inFile)

    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliencyLowResMap) = saliency.computeSaliency(image)

    saliencyLowResMap = saliencyLowResMap * 255
    cv2.imwrite( outFile, saliencyLowResMap )

    #(thresh, saliencyLoResMap) = cv2.threshold(saliencyLowResMap, 63, 255, cv2.THRESH_BINARY)

    total = saliencyLowResMap.shape[0] * saliencyLowResMap.shape[1] # Total number of pixels
    number_salient = np.count_nonzero( saliencyLowResMap ) # Number of salient pixels

    saliency_density = float(number_salient ) / float( total ) # Ratio

    return saliency_density

def hi_res(inFile, outFile):



    image = cv2.imread(inFile)

    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyHiResMap) = saliency.computeSaliency(image)

    #saliencyHiResMap = saliencyHiResMap
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

#
# AALTO version of feature congestion.
#

def create_border(img, borders, y, x):
    r1 = int(img[y][x][0])
    g1 = int(img[y][x][1])
    b1 = int(img[y][x][2])

    points_2 = [
        [y, x + 1],
        [y, x - 1],
        [y + 1, x],
        [y - 1, x]
    ]

    ret = 0
    for n in range(4):
        x2 = points_2[n][1]
        y2 = points_2[n][0]

        r2 = int(img[y2][x2][0])
        g2 = int(img[y2][x2][1])
        b2 = int(img[y2][x2][2])

        dst_r = math.fabs(r2 - r1)
        dst_g = math.fabs(g2 - g1)
        dst_b = math.fabs(b2 - b1)

        if (dst_r > 50 or dst_b > 50 or dst_g > 50) and borders[y2][x2] == 0:
            ret = 255
            break

    return ret

#
# Notes for this implementation of the algortihm from Minuikovich and De Angeli:
# https://www.researchgate.net/publication/266657991_Quantification_of_interface_visual_complexity
#
# We operationalized edge congestion and figure-ground contrast. 
# Edge congestion relies on the notion of critical spacing – minimal distance between objects at which the user starts 
# having difficulties differentiating the objects. We tried out 8-, 12- and 20pixel thresholds, which all gave similar results. 
# Hence, we chose the 20-pixel threshold. 
# ##
# ## NB The Aalto implementation here by Thomas Langerak in 2017 uses 4 as the congestion threshold, arguing more than 4 pixels is too far.
# ## BUT we feel this depends on screen size and viewing distance and should really be expressed in terms of visual angle.
# ##
# The algorithm consisted of two main steps: detecting edges and detecting edges in close proximity. 
# Any edge detection algorithm without pre-detection smoothing could be used (e.g., the Sobel or Prewitt algorithms); 
# we used simple value difference of more than 50 between adjacent pixels across all three (red, green and blue) color components. 
# The edges by different color components were combined using disjunction. 
# In the second step, if at least two pixels of two different edges occurred in the same 20-pixel vicinity, they were marked as congested. 
# The marking was done in both horizontal and vertical directions. 
# Finally, we took the ratio of ‘congested’ pixels (pc) to all edge pixels (pa) as the metric of edge congestion: !"#$= !!/!!. 
# Edge congestion does not require chance normalization as the symmetry metric above, despite they both leverage edge detection. 
# Whatever the reason is two edges are too close, they still impede user perception fluency. 
#
# Rosenholtz's 2007 feature congestion metric is less well correlated with RT than edge congestion
#
def edgeCongestion(inFile, outFile):
    # Initialize
    print( "Running contour congestion" )
    img = cv2.imread(inFile)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    height, width, depth = img.shape
    borders = np.zeros((img.shape[0], img.shape[1]), dtype=np.int)

    # Do edge detection. create_border return 0 or 255 depending on the difference with neigboring pixels
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            borders[y][x] = create_border(img, borders, y, x)

    count_edge = 0
    count_uncongested = 0
    threshold = 4 # Paper says 20, this is insane. The amount of pixels a person needs to differentiate between two elements

    # Create numpy array from list
    borders = np.array(borders)

    # Assumme screen border is always a border
    for x in range(threshold, width - threshold):
        for y in range(threshold, height - threshold):
            if borders[y][x] == 255:
                count_edge += 1

                # Sum left, right, up, down for number of pixels in threshold
                arr_right = borders[y, x + 1:x + threshold]
                sum_right = sum(arr_right)
                arr_left = borders[y, x - threshold:x - 1]
                sum_left = sum(arr_left)
                arr_up = borders[y + 1:y + threshold, x]
                sum_up = sum(arr_up)
                arr_down = borders[y - threshold:y - 1, x]
                sum_down = sum(arr_down)

                # If the sum is zero, it means there are no other pixels nearby. It needs to be in all directions non-0
                # for a pixel to be congested
                if sum_right == 0 or sum_left == 0 or sum_up == 0 or sum_down == 0:
                    count_uncongested += 1

    try:
        count_congested = count_edge - count_uncongested
        result = float(count_congested) / float(count_edge)
    except ZeroDivisionError:
        result = 0

    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    cv2.imwrite( outFile, borders )

    return( result )
