from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc

TEMPLATE_WIDTH = 15

def MakePyramid(image, minsize):
    pyramid = [image]
    x,y = image.size
    while x > minsize:
        x *=0.75
        y *=0.75
        pyramid.append(im.resize((int(x),int(y)), Image.BICUBIC))
        
    return pyramid

def ShowPyramid(pryamid):
    width = []
    height = pyramid[0].size[1]
    for im in pyramid:
        width.append(im.size[0])
    combined_pyramid = Image.new("L", (sum(width), height))
    combined_pyramid.paste(pryamid[0],(0,0))
    for i in range(1 ,len(pyramid)):
        combined_pyramid.paste(pryamid[i],(sum(width[0:i]),0))
    combined_pyramid.show()

def drawRect(x,y, halfwidth, halfheight, im):
    draw = ImageDraw.Draw(im)
   
    draw.line((x-halfwidth,y+halfheight,x-halfwidth,y-halfheight),fill=200,width=2)
    draw.line((x+halfwidth,y+halfheight,x+halfwidth,y-halfheight),fill=200,width=2)
    draw.line((x-halfwidth,y+halfheight,x-halfwidth,y+halfheight),fill=200,width=2)
    draw.line((x-halfwidth,y-halfheight,x+halfwidth,y-halfheight),fill=200,width=2)
    del draw


def FindTemplate(pyramid, template, threshold):

    x,y = template.size
    xyratio = float(y)/float(x)
    normtemplate = template.resize((TEMPLATE_WIDTH,int(float(TEMPLATE_WIDTH)*(xyratio))), Image.BICUBIC)
    corr = []
    highvals = []
    for i in range(0,len(pyramid)):
        corr.append(ncc.normxcorr2D(pyramid[i], normtemplate))     
        for x in range(0, corr[i].shape[0]):
            for y in range(0, corr[i].shape[1]):
                denormal = corr[i][x][y]
                if corr[i][x][y] > float(threshold):          
                    scalefactor = 1.0/pow(.75,i)            
                    highvals.append((int(float(x)*scalefactor),int(float(y)*scalefactor), i))

    for i in range(0,len(highvals)):
        scalefactor = 1.0/pow(.75,highvals[i][2])
        drawRect(highvals[i][1],highvals[i][0], int((float(TEMPLATE_WIDTH)*scalefactor)/2.0), int((float(TEMPLATE_WIDTH)*(xyratio)*scalefactor)/2.0),pyramid[0])
    pyramid[0].show()

img_path = "faces/judybats.jpg"
im = Image.open(img_path)
pyramid = MakePyramid(im, 25)
ShowPyramid(pyramid)

template = Image.open("faces/template.jpg")
FindTemplate(pyramid, template, 0.6)
