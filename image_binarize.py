from PIL import Image
import pytesseract
from IPython.display import display
# def display(image_to_show):
#     image_to_show.show()


# Lets read in the storefront image I've loaded into the course and display it
image=Image.open('storefront.jpg')
display(image)
# Finally, lets try and run tesseract on that image and see what the results are
print(pytesseract.image_to_string(image))
    
# OUTPUT: ''

# We see at the very bottom there is just an empty string. Tesseract is unable to take
# this image and pull out the name.  
#W'll will help Tesseract to crop the images in the
# First, lets set the bounding box. In this image the store name is in a box
bounding_box=(315, 170, 700, 270)
# Now lets crop the image
title_image=image.crop(bounding_box)
# Now lets display it and pull out the text
display(title_image)
print(pytesseract.image_to_string(title_image))

# OUTPUT: FOSSIL

# Great, we see how with a bit of a problem reduction we can make that work. So now we have
# been able to take an image, preprocess it where we expect to see text, and turn that text
# into a string that python can understand.
#
# If you look back up at the image though, you'll see there is a small sign inside of the
# shop that also has the shop name on it. I wonder if we're able to recognize the text on 
# that sign? Let's give it a try.
#
# First, we need to determine a bounding box for that sign. 
bounding_box=(900, 420, 940, 445)
# Now, lets crop the image

little_sign=image.crop((900, 420, 940, 445))
display(little_sign)

# All right, that is a little sign! OCR works better with higher resolution images, so
# lets increase the size of this image by using the pillow resize() function
new_size=(little_sign.width*10,little_sign.height*10)

# We can see that there are a number of different filters for resizing the image. The
# default is Image.NEAREST. Lets see what that looks like
# I think we should be able to find something better. I can read it, but it looks
# really pixelated. Lets see what all the different resize options look like
options=[Image.NEAREST, Image.BOX, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS]
for option in options:
    # lets print the option name
    print(option)
    # lets display what this option looks like on our little sign
    display(little_sign.resize( new_size, option))

# From this we can notice two things. First, when we print out one of the resampling
# values it actually just prints an integer! This is really common: that the
# API developer writes a property, such as Image.BICUBIC, and then assigns it to an
# integer value to pass it around. Some languages use enumerations of values, which is
# common in say, Java, but in python this is a pretty normal way of doing things.
# The second thing we learned is that there are a number of different algorithms for
# image resampling. In this case, the Image.LANCZOS and Image.BICUBIC filters do a good
# job. Lets see if we are able to recognize the text off of this resized image

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

# Ok, that text is pretty useless. How should we pick the best binarization
# to use? Well, there are some methods, but lets just try something very simple to
# show how well this can work. We have an english word we are trying to detect, "FOSSIL".
# If we tried all binarizations, from 0 through 255, and looked to see if there were
# any english words in that list, this might be one way. So lets see if we can
# write a routine to do this.
#
# First, lets load a list of english words into a list.
eng_dict=[]
with open ("words_alpha.txt", "r") as f:
    data=f.read()
    # now we want to split this into a list based on the new line characters
    eng_dict=data.split("\n")

for i in range(150,170):
    # lets binarize and convert this to s tring values
    strng=pytesseract.image_to_string(binarize(bigger_sign,i))
    # We want to remove non alphabetical characters, like ([%$]) from the text, here's
    # a short method to do that
    # first, lets convert our string to lower case only
    strng=strng.lower()
    # then lets import the string package - it has a nice list of lower case letters
    import string
    # now lets iterate over our string looking at it character by character, putting it in
    # the comaprison text
    comparison=''
    for character in strng:
        if character in string.ascii_lowercase:
            comparison=comparison+character
    # finally, lets search for comparison in the dictionary file
    if comparison in eng_dict:
        # and print it if we find it
        print(comparison)
