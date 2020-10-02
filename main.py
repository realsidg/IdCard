"""
Created by Siddharth Garg 
Registration number:18BCB0038

This is a python3 script reads the data of the members from a csv file and images saved as name of the respective members.
Output is saved in output/ with png at output/png/ and pdf at output/pdf/

-->I have included placeholder profile pictures (of lego faces, obviously) at dataset/images/ as the name of the respective members<--

Python Modules required:
1.img2pdf
2.PIL (Pillow)
#import more files
"""

import csv
import os
import img2pdf
from PIL import Image, ImageOps, ImageFont, ImageDraw

csvFile=open('dataset/data.csv', 'r')
reader = csv.reader(csvFile)
for row in reader:

    name,pos,q=row

    f_name,l_name=name.split()

    #splits quote with line breaks
    quote='"'+(q if len(q)<46 else q[:47]+'\n-'+q[47:])+'"'

    #opening image
    img = Image.open("plain.png")
    draw = ImageDraw.Draw(img)

    #opening font files
    font_name = ImageFont.truetype("fonts/Lato-Black.ttf", 130)
    font_pos = ImageFont.truetype("fonts/Lato-Regular.ttf", 64)
    font_quote = ImageFont.truetype("fonts/Lato-Light.ttf", 44)

    #Writing text at specific positions and specific color.
    draw.text((74, 1060),f_name,(0,148,255),font=font_name)
    draw.text((74, 1170),l_name,(0,0,0),font=font_name)
    draw.text((71, 1310),pos,(0,0,0),font=font_pos)
    draw.text((71, 1500),quote,(0,0,0),font=font_quote)

    #A transparent circular image of required size is created for ID-card picture
    size = (770, 770)
    mask = Image.new('L', size, 0)
    dp = ImageDraw.Draw(mask) 
    dp.ellipse((0, 0) + size, fill=255)
    im = Image.open('dataset/images/'+name+'.jpg')
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    #Profile image is superimposed on the ID-card image with itself as a filter
    img.paste(output,(180,230),output)

    #Image is resized (with respect to 92dpi) and saved to output/png/
    img = img.resize((322,482), Image.ANTIALIAS)
    img.save('output/png/'+name+'.png')

    #To convert to pdf the image is temporarily stored as jpeg
    rgb_img=img.convert('RGB')
    rgb_img.save("temp.jpg")
    temp=Image.open("temp.jpg")

    #The jpeg file is converted to pdf.
    pdf_bytes = img2pdf.convert("temp.jpg")  
    file = open("output/pdf/"+name+".pdf", "wb") 
    file.write(pdf_bytes) 

os.remove("temp.jpg")
csvFile.close()
