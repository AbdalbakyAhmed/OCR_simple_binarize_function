from PIL import Image
import pytesseract
from IPython.display import display
# def display(image_to_show):
#     image_to_show.show()


# Lets read in the storefront image I've loaded into the course and display it
image=Image.open('storefront.jpg')
display(image)

bounding_box=(315, 170, 700, 270)
title_image=image.crop(bounding_box)
# Now lets display it and pull out the text
display(title_image)
print(pytesseract.image_to_string(title_image))

# If you look back up at the image though, you'll see there is a small sign inside of the
# shop that also has the shop name on it. I wonder if we're able to recognize the text on 
# that sign? Let's give it a try.
bounding_box=(900, 420, 940, 445)
# Now, lets crop the image
little_sign=image.crop((900, 420, 940, 445))
display(little_sign)

# All right, that is a little sign! OCR works better with higher resolution images, so
# lets increase the size of this image by using the pillow resize() function
new_size=(little_sign.width*10,little_sign.height*10)
options=[Image.NEAREST, Image.BOX, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS]
for option in options:
    # lets print the option name
    print(option)
    # lets display what this option looks like on our little sign
    display(little_sign.resize( new_size, option))
# From this we can notice two things. First, when we print out one of the resampling
# values it actually just prints an integer! This is really common: that the
# API developer writes a property, such as Image.BICUBIC, and then assigns it to an
# integer value to pass it around. 

# First lets resize to the larger size
bigger_sign=little_sign.resize(new_size, Image.BICUBIC)
# Lets print out the text
pytesseract.image_to_string(bigger_sign)
# Well, no text there. Lets try and binarize this. First, let me just bring in the
# binarization code we did earlier
def binarize(image_to_transform, threshold):
    output_image=image_to_transform.convert("L")
    for x in range(output_image.width):
        for y in range(output_image.height):
            if output_image.getpixel((x,y))< threshold:
                output_image.putpixel( (x,y), 0 )
            else:
                output_image.putpixel( (x,y), 255 )
    return output_image
eng_dict=[]
with open ("words_alpha.txt", "r") as f:
    data=f.read()
    eng_dict=data.split("\n")

for i in range(150,170):
    strng=pytesseract.image_to_string(binarize(bigger_sign,i))
    strng=strng.lower()
    # then lets import the string package - it has a nice list of lower case letters
    import string
    
    comparison=''
    for character in strng:
        if character in string.ascii_lowercase:
            comparison=comparison+character
    if comparison in eng_dict:
        # and print it if we find it
        print(comparison)
