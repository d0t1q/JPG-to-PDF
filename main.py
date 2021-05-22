from fpdf import FPDF
from PIL import Image
import os
import sys

pdf = FPDF()
imagelist = []                                                 # Contains the list of all images to be converted to PDF.

try:
    folder = sys.argv[1]                                                    # Folder containing all the images
    name = sys.argv[2]                                                     # Name of the output PDF file.
except IndexError:
    folder = "./"
    name = "out.pdf"

ext = [".jpg", ".png"]
for dirpath, dirnames, filenames in os.walk(folder):
    for filename in [f for f in filenames if f.endswith(tuple(ext))]:
        full_path = os.path.join(dirpath, filename)
        imagelist.append(full_path)


imagelist.sort()                                               # Sort the images by name.
for i in range(0, len(imagelist)):
    print(imagelist[i])
    
#de-interlace png files  https://stackoverflow.com/questions/7583564/how-do-i-deinterlace-an-image-in-python
for i in range(0, len(imagelist)):
    img=Image.open(imagelist[i])
    size=list(img.size)
    size[0] /= 2
    size[1] /= 2
    downsized=img.resize(size, Image.NEAREST) 
    downsized.save(imagelist[i])
    
    
    

# --------------- ROTATE ANY LANDSCAPE MODE IMAGE IF PRESENT ----------------- #

for i in range(0, len(imagelist)):
    im1 = Image.open(imagelist[i])                             # Open the image.
    width, height = im1.size                                   # Get the width and height of that image.
    if width > height:
        im2 = im1.transpose(Image.ROTATE_270)                  # If width > height, rotate the image.
        os.remove(imagelist[i])                                # Delete the previous image.
        im2.save(imagelist[i])                                 # Save the rotated image.
        # im.save

print("\nFound " + str(len(imagelist)) + " image files. Converting to PDF....\n")


# -------------- CONVERT TO PDF ------------ #

for image in imagelist:
    pdf.add_page()
    pdf.image(image, 0, 0, 210, 297)                           # 210 and 297 are the dimensions of an A4 size sheet.

pdf.output(folder + name, "F")                                 # Save the PDF.

print("PDF generated successfully!")
