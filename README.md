# OCR_simple_binarize_function
Tesseract is unable to take this image and pull out the words, so you can help tesseract by cropping out certain pieces.

If you look back up at the image though, you'll see there is a small sign inside of the shop that also has the shop name on it.
In this tutorial we're able to recognize the text on that sign? Let's give it a try.
First, we need to determine a bounding box for that sign. OCR works better with higher resolution images, so increase the size of this image by using the pillow resize() function. 
*The Image.LANCZOS and Image.BICUBIC filters do a good job

<img src="storefront.png" alt="storefront" width="800"/>


#### How should we pick the best binarization to use? 
Well, there are some methods, We have an english word we are trying to detect, "FOSSIL".
If we tried all binarizations, from 0 through 255, and looked to see if there were any english words in that list, this might be one way.

#### This work was delivered by accomplishing "Python Project: pillow, tesseract, and opencv". 
#### This course is part of the "Python 3 Programming Specialization" by University of Michigan.
#### https://www.coursera.org/learn/python-project/home/welcome
