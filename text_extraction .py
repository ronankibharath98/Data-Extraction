#import required libraries
import os
import re
import io
import datetime
import pytesseract
import pandas as pd
import numpy as np
from PIL import Image
from google.cloud import vision 
from matplotlib import pyplot as plt 
from matplotlib import patches as pch 

#set path for the OCR API(google vision)
'''you need to create an Google vision API
to run this code which is available in google.
without the API you can not run this code.'''

credential_path = "C:/Users/Nani/Downloads/image-058318726b3f.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
client = vision.ImageAnnotatorClient() 

#set path for the input data

path1 = 'C:/Users/Nani/Downloads/Receipts/'
dirList=os.listdir(path1)
im=[]

#append the input data to the list 

for fname in dirList:
    im.append(fname)
print(im)
totalImages = len(im)
v=[]
dates = []
names = []
extractedImages = 0
count = 0

#text extraction for each image

for i in im:
    with open(path1+i, 'rb') as image:
        content = image.read()
        image = vision.types.Image(content = content)
        response = client.text_detection(image=image)  
        df = pd.DataFrame(columns=['locale', 'description'])
        texts = response.text_annotations
        #append the extracted data to a dataframe
        for text in texts:
            df = df.append(
                    dict(
                            locale=text.locale,
                            description=text.description
                            ),
                            ignore_index=True
                            )
    x=[(df['description'][0])]
    #creating a regular expression to extract dates of different formats
    date_reg_exp2 = re.compile(r"(\d{2}|\d{1})([-/.])(\d{2}|\d{1}|[a-zA-Z]{3})\2(\d{4}|\d{2})|\w{3}\s(\d{1}|\d{2})[,.']\s(\d{4}|\d{2})|\w{3}(\d{1}|\d{2})[',](\d{2}|\d{4})|\d{2}\w{3}[']\d{2}")

    matches_list = [x.group() for x in date_reg_exp2.finditer(str(x))]
    print(matches_list)
    if len(matches_list)==0:
        name = np.repeat(i, 1, axis=0)
        matches_list = ["No Date Found"]
    else:
        name = np.repeat(i, len(matches_list), axis=0)
        matches_list = matches_list
        extractedImages = extractedImages + 1
    dates.append(matches_list)
    names.append(name)
  
print(dates)
print(names)

from itertools import chain
dates = list(chain(*dates))
names = list(chain(*names))
#creating a dataframe to convert the output into .CSV format
data = pd.DataFrame({"Names":names, "Dates":dates})
print(data)
data.to_csv(r'C:/Users/Nani/Downloads/data.csv')
#calculating the accuracy 
print("total number of images are : ",totalImages)
print("total number of images from which date is extracted : ",extractedImages)
accuracy = (extractedImages/totalImages)*100
print("ACCURACY : ", accuracy)
