#!/usr/bin/env python

from PIL import Image, ImageDraw
import random
import math
from copy import deepcopy

debug = True


# makes a blank imagefile with the same size a source image
def initImg(filename):
    newImg = Image.new("RGB",srcImg.size,"white")
    newImg.save(filename)
    return newImg


# draw a random square
def drawRandomSquare():
    width, height = drawImg.size

    global size
    size = 2

    p1 = (random.randint(0,width),random.randint(0,width))
    # p2 is "just outside" rectangle
    p2 = (p1[0]+size,p1[1]+size) 
   
    ## bounds to be used by comarison function
    global bounds
    bounds = (p1[0],p1[1],p2[0],p2[1]) 

    # get random color
    global srcColors
    color = srcColors[random.randint( 0, len(srcColors)-1 )]

    # actually draw
    draw.rectangle([p1,p2],fill=color)

    if debug == True:
        # save image
        drawImg.save("img_finale.png")
        input()


# make list of colors
def analyzeSource():
    ## disturb user if non-rgb
    if srcImg.mode != "RGB":
        print("Not RGB  trying convert")
        input()
        srcImg.convert("RGB")

    # image to list of pixel tuples
    srcPixelList = list(srcImg.getdata())
   
    print("Loaded image. Starting color analysis.")
    # list of individual colors
    global srcColors
    srcColors = []
    # identify unique colors
    for pixel in srcPixelList:
        if pixel not in srcColors:
            srcColors.append(pixel)
    print("Finsihed finding "+str(len(srcColors))+" colors.")


# use manhattan distance
# maybe compare smaller sections of image for faster processing
def compareWithSrc(img):
    # announce method call
    if (debug == True):
        print(" - - comparewithSrc() called. - - ")

    # get bounds tuple from square method
    global bounds

    # crop images
    imgCrop = deepcopy(img)
    srcCrop = deepcopy(srcImg)
    imgCrop = imgCrop.crop( bounds )
    srcCrop = srcCrop.crop( bounds )

    # sanity check for size
    if (debug == True):
        global size
        imgW, imgH = imgCrop.size
        if (imgW != size or imgH != size):
            print("Size problem with img")
            print("Width: "+str(imgW)+" Height: "+str(imgH))
            print("Size is set to: "+str(size))
        srcW, srcH = imgCrop.size
        if (srcW != size or srcH != size):
            print("Size problem with src")
            print("Width: "+str(srcW)+" Height: "+str(srcH))
            print("Size is set to: "+str(size))

    # make list of pixels in image
    imgCropList = list(imgCrop.getdata())
    srcCropList = list(srcCrop.getdata())
    
    if (debug == True):
        # sanity check list length
        if ( len(imgCropList) != len(srcCropList)):
            print("Pixel list lengths not equal.")
        imgCrop.save("imgCrop.png")
        srcCrop.save("srcCrop.png")

    # init diff
    diff = 0

    # loop though list 
    for i in range( 0, len(imgCropList) ):
        # calculate manhattan color distance
        diffR = abs(imgCropList[i][0] - srcCropList[i][0])
        diffG = abs(imgCropList[i][1] - srcCropList[i][1])
        diffB = abs(imgCropList[i][2] - srcCropList[i][2])
        diff += diffR + diffG + diffB

    if diff == 0:
        print("Nulldiff.")

    return diff


# load source image
filename = "./tux.png"
srcImg = Image.open(filename)
analyzeSource()

# make new blank image and a copy of it
compImg = initImg("new_img.png")
drawImg = deepcopy(compImg)

# init drawer class
draw = ImageDraw.Draw(drawImg)

####
# GO GO GO

# declare the counter vars
accept = 0
reject = 0
identical = 0
for i in range(0,1000000):

    #STATS
    print("Drawing square no: "+str(i)+" (Accepted: "+str(accept)+" Rejected: "+str(reject)+" Identical: "+str(identical)+")")

    # draw another one
    drawRandomSquare()

    # calculate diff on new image
    ## this calculates doubly - unnecessary
    drawImgDiff = compareWithSrc(drawImg)
    compImgDiff = compareWithSrc(compImg)

    # announce diff results
    if debug == True:
        print("Both diffs found: "+str(drawImgDiff)+" "+str(compImgDiff))

    # if new image is better:
    if ( drawImgDiff < compImgDiff ):
        # make new comp, and transfer diff value
        compImg = deepcopy(drawImg)
        accept += 1

    # if new image is worse
    elif ( drawImgDiff > compImgDiff ):
        # reset
        drawImg = deepcopy(compImg)
        reject += 1

    else:
        print("Neither is closer - wat?")
        identical += 1

    # make new file every tenth iteration
    if (accept % 10 == 0 or debug == True):
        drawImg.save("img_finale.png")

# save when finished
drawImg.save("img_finale.png")
