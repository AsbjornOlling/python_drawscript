#!/usr/bin/env python

from PIL import Image, ImageDraw
import random
import math

debug = False
saveframes = True
iterations = 100000
inputfile = "./fjong2.png"
outputfile = "./output.png"


# draw a random square
def drawRandomSquare():

    # init drawer class
    draw = ImageDraw.Draw(drawImg)

    width, height = drawImg.size

    global size
    size = random.randint(1,5)

    p1 = (random.randint(0,width),random.randint(0,height))
    # p2 is "just outside" rectangle
    p2 = (p1[0]+size,p1[1]+size) 
   
    ## bounds to be used by comarison function
    global bounds
    bounds = (p1[0],p1[1],p2[0],p2[1]) 

    # handle bounds outside box
    if bounds[2] > width or bounds[3] > height:
        bounds = (p1[0],p1[1],width,height) 
        if debug == True:
            print("Changing bounds")

    # get jandom color
    global srcColors
    color = srcColors[random.randint( 0, len(srcColors)-1 )]

    # actually draw
    draw.rectangle([p1,p2],fill=color)

    if debug == True:
        # save image after draw
        drawImg.save(outputfile)
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
    imgCrop = img.copy()
    srcCrop = srcImg.copy()
    imgCrop = imgCrop.crop( bounds )
    srcCrop = srcCrop.crop( bounds )

    # make list of pixels in image
    imgCropList = list(imgCrop.getdata())
    srcCropList = list(srcCrop.getdata())

    if debug == True:
        # print size and crop size
        global size
        print("Size: "+str(size)+" ImgCrop: "+str(imgCrop.size)+" SrcCrop: "+str(srcCrop.size)+"Bounds: "+str(bounds) )
        # sanity check for size
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
        # sanity check list length
        if ( len(imgCropList) != len(srcCropList)):
            print("Pixel list lengths not equal.")
        # save crops every time
        #imgCrop.save("imgCrop.png")
        #srcCrop.save("srcCrop.png")

    # init diff
    diff = 0

    # loop though list, calculate manhattan color distance
    for i in range( 0, len(imgCropList) ):
        diffR = abs(imgCropList[i][0] - srcCropList[i][0])
        diffG = abs(imgCropList[i][1] - srcCropList[i][1])
        diffB = abs(imgCropList[i][2] - srcCropList[i][2])
        diff += diffR + diffG + diffB

    return diff

# number and save output image in folder
def saveFrame(i):
    if i > 9999:
        zeroes = ""
    elif i > 999:
        zeroes = "0"
    elif i > 99:
        zeroes = "00"
    elif i > 9:
        zeroes = "000"
    else:
        zeroes = "0000"
    framefile = "image_"+zeroes+str(i)
    drawImg.save("./out/"+framefile+".png")

# load source image
srcImg = Image.open(inputfile)
analyzeSource()

# make new blank image and a copy of it, don't save shit
compImg = Image.new("RGB",srcImg.size,"white")
drawImg = compImg.copy()

    ####
    # GO GO GO

# declare the counter vars
accept = 0
reject = 0
identical = 0
framecount = 0
for i in range(0,iterations):

    # MAIN STATS LINE
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
        compImg = drawImg.copy()
        accept += 1
        if saveframes == True and accept % 100 == 0:
            saveFrame(framecount)
            framecount += 1

    # if new image is worse
    elif ( drawImgDiff > compImgDiff ):
        # reset
        drawImg = compImg.copy()
        reject += 1

    else:
        print("Neither is closer - wat?")
        identical += 1

    # make new file every tenth iteration
    if (accept % 100 == 0 and saveframes != True) or debug == True:
            drawImg.save(outputfile)

#save when finished
drawImg.save(outputfile)
