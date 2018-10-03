from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc

TEMPLATE_WIDTH = 15

# Create a image pyramid
# input: image: image to make a pyramid
# input: minsize: min size of an image in pyramid
# output: image pyramid in the form of an array of PIL images
def MakePyramid(image, minsize):
    pyramid = [image]
    x,y = image.size
    while x > minsize:
        x *=0.75
        y *=0.75
        pyramid.append(im.resize((int(x),int(y)), Image.BICUBIC))
        
    return pyramid

# display the pyramid for testng purposes
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

# Create an array of coordinates where each coordinate is the location matching the template
# input: pyramid: a pyramid of images
# input: template: the image to be matched 
# input: threshold: the min value for a template to match
# output: an array or tupes matching templates
def GetMatchedTemplateCoordinates(pyramid, template, threshold):
    x,y = template.size
    xyratio = float(y)/float(x)
    normtemplate = template.resize((TEMPLATE_WIDTH,int(float(TEMPLATE_WIDTH)*(xyratio))), Image.BICUBIC)
    # an array of normalized correlations for each image in the pyramid
    correlatedarray = []
    # an array of tuples (x,y,index) where index is the index in the pyramid 
    # this is in order to kow how much to scale the template later
    matchingvalues = []
    for i in range(0,len(pyramid)):
        # get correlation result from template and an image in the pryamid
        correlatedarray.append(ncc.normxcorr2D(pyramid[i], normtemplate))     
        for x in range(0, correlatedarray[i].shape[0]):
            for y in range(0, correlatedarray[i].shape[1]):
                denormal = correlatedarray[i][x][y]
                # if we have value above the threshold, we add that coorinate to the array for later
                if correlatedarray[i][x][y] > float(threshold):          
                    scalefactor = 1.0/pow(.75,i)            
                    matchingvalues.append((int(float(x)*scalefactor),int(float(y)*scalefactor), i))
    return matchingvalues


# Given a pyramid, template and threshold, display where the template matches
# input: pyramid: a pyramid of images
# input: template: the image to be matched 
# input: threshold: the min value for a template to match
def FindTemplate(pyramid, template, threshold):  
    x,y = template.size
    xyratio = float(y)/float(x)
    highvals = GetMatchedTemplateCoordinates(pyramid, template, threshold)
    #draw boxes around faces
    for i in range(0,len(highvals)):
        scalefactor = 1.0/pow(.75,highvals[i][2])
        drawRect(highvals[i][1],highvals[i][0], int((float(TEMPLATE_WIDTH)*scalefactor)/2.0), int((float(TEMPLATE_WIDTH)*(xyratio)*scalefactor)/2.0),pyramid[0])
    #display the image
    pyramid[0].show()

img_path = "faces/judybats.jpg"
im = Image.open(img_path)
pyramid = MakePyramid(im, 25)
ShowPyramid(pyramid)

template = Image.open("faces/template.jpg")
FindTemplate(pyramid, template, 0.6)
