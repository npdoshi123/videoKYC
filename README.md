# VideoKYC.

## Process flow
The purpose of this software is to demonstrate the OCR using tesseract. Please note the card identification and localization is not in the scope of this demonstration. However, card identification is done for better OCR results. Template matching technique is used for card identification in the software is not recommended for video KYC in its current form. 

The process flow is as below:

•	Image is open using OpenCV 

•	Card identification is done using template matching algorithm. 

•	Then the image is pass to OCR engine for character recognition.

Programmatically two separate models are created for processing of PAN card and Adhar card. Each model uses the structural information for extracting the text information from the card. Finally, the OCR results are printed in console.


## Requirements:
Python 3.X

OpenCV 4.X

Pytesseract

## Files
main.py - This is the entry point to the software. All the OCR code is put in this file
Imageset - This folder contains the ID card and its templates. The ID card number is changed for security reason.

## main.py
Line number 128 in main.py is changed to select the image (img = cv.imread('Imageset/img_p.jpg' or img = cv.imread('Imageset/img_a.jpg'))

## Results
Adhar Card:

![AdharCard](https://user-images.githubusercontent.com/5662535/118500194-37b27200-b745-11eb-9a85-62e1c5da7241.PNG)

PAN Card:

![pan](https://user-images.githubusercontent.com/5662535/118500263-47ca5180-b745-11eb-9f1e-3234551d5989.PNG)




