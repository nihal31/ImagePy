from __future__ import division
from imutils import paths
import os
import argparse
import cv2
import shutil as sh
import numpy as np

def meancalc(hist):
        #print sum([hist[x][0] for x in range(30)])
	m = sum([x*hist[x][0] for x in range(30)])/6210000
	v = sum([(x**2)*hist[x][0] for x in range(30)])/6210000 - (m**2)
        return m,v
	


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=-1.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

path = os.getcwd()

mask = np.zeros((2700,5400), np.uint8)
mask[1000:2150 , :] = 255



if not os.path.exists(path + os.sep + "obright") :
	os.mkdir(path + os.sep + "obright")
if not os.path.exists(path + os.sep + "oclean") :
	os.mkdir(path + os.sep + "oclean")
if not os.path.exists(path + os.sep + "odark") :
	os.mkdir(path + os.sep + "odark")

if args["threshold"] > -1.0 :
	if not os.path.exists(path + os.sep + "notblur") :
		os.mkdir(path + os.sep +"notblur")
	if not os.path.exists(path + os.sep +"blurred") :
		os.mkdir(path + os.sep + "blurred")

f1 = open("blur.txt","w")
f2 = open("exp.txt","w")
i = 0
for imagepath in paths.list_images(args["images"]):
	# load the image, convert it to grayscale, and compute the
	# focus measure of the image using the Variance of Laplacian
	# method
	image = cv2.imread(imagepath)
	grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	hist = cv2.calcHist([grey],[0],mask,[30],[0,256])

	if args["threshold"] > -1 :
		vofl = variance_of_laplacian(image)
				
		if vofl < args["threshold"] :
			f1.write(imagepath + " : blurred\n")
			sh.copy(imagepath, path + os.sep + "blurred")
		else : 
			f1.write(imagepath + " : not blurred\n	")
			sh.copy(imagepath, path + os.sep + "notblur")
			
		
	avg,variance = meancalc(hist)
	print avg,variance,i	
	if avg > 18.0 :
		f2.write(imagepath + " : brite %f %f\n" %(avg,variance))
		sh.copy(imagepath, path + os.sep +"obright")
	elif avg < 9.0 :
		f2.write(imagepath + " : darky %f %f\n" %(avg,variance))
		sh.copy(imagepath, path + os.sep + "odark")
	else : 
		f2.write(imagepath + " : clean %f %f\n" %(avg,variance))
		sh.copy(imagepath, path + os.sep + "oclean")
	i+=1
	

f1.close()
f2.close()	
