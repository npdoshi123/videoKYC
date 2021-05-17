import cv2 as cv
import numpy as np
import pytesseract


# Identify the card type
def CardDetector(templatesList, imgSource):
    for templateFile in templatesList:
        templateImage = cv.imread(templateFile)
        [x, y, width, height] = TemplateMatch(imgSource, templateImage)
        if width > 0:
            print('Card found!')
            return [x, y, width, height, templateFile]

    # If match is not found the return empty data
    print('Card not found!')
    return [0, 0, 0, 0, '']


# Template matching and identifying best match
def TemplateMatch(sourceImage, templateImage):
    w, h, c = templateImage.shape
    res = cv.matchTemplate(sourceImage, templateImage, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if max_val > 0.75:
        return [max_loc[0], max_loc[1], w, h]
    else:
        return [0, 0, 0, 0]


# Processing PAN card information
def ProcessPAN(imageSource, x, y, width, height):

    # Selecting ROI on gray scale image based on the template match location
    imgW, imgH, imgC = imageSource.shape
    imageSource = cv.cvtColor(imageSource, cv.COLOR_BGR2GRAY)
    imgSourceROI = imageSource[y+width:, x:]

    # Colour based image thresholding to binarised image
    lowerRange = [(0)]
    higherRange = [(75)]
    mask = cv.inRange(imgSourceROI, np.array(lowerRange), np.array(higherRange))
    result = pytesseract.image_to_data(mask)
    PrintPAN(result)


# Print PAN card information
def PrintPAN(ocrResult):

    # Fields to extract
    dataProperty = ['name', 'fatherName', 'DOB', 'PAN']

    # Result dictionary
    resultData = {"name": "", "fatherName": "", "DOB": "", "PAN": ""}

    # Loop over list of strings to extract the relevant data
    currentRow = 0
    currentline = 0
    currentIndex = -1
    for x, data in enumerate(ocrResult.splitlines()):
        if x != 0:
            dataRow = data.split()
            if len(dataRow) > 11 and int(dataRow[10]) > 70:
                row = int(dataRow[2])
                line = int(dataRow[4])
                if row != currentRow or currentline != line:
                    currentRow = row
                    currentline = line
                    currentIndex += 1
                    resultData[dataProperty[currentIndex]] += dataRow[11]
                else:
                    resultData[dataProperty[currentIndex]] += (" " + dataRow[11])
    print(resultData)


# Processing Adhar card information
def ProcessAdhar(imageSource, x, y, width, height):
    # Selecting ROI on gray scale image based on the template match location
    imgW, imgH, imgC = imageSource.shape
    imageSource = cv.cvtColor(imageSource, cv.COLOR_BGR2GRAY)
    imgSourceROI = imageSource[y + width:, x:]

    # Colour based image thresholding to binarised image
    lowerRange = [(0)]
    higherRange = [(100)]
    mask = cv.inRange(imgSourceROI, np.array(lowerRange), np.array(higherRange))
    result = pytesseract.image_to_data(mask)
    PrintAdhar(result)


# Print Adhar
def PrintAdhar(ocrResult):

    # Fields to extract
    dataProperty = ['name', 'number']

    # Result dictionary
    resultData = {"name": "", "number": ""}

    # Loop over list of strings to extract the relevant data
    currentRow = 0
    currentIndex = -1
    for x, data in enumerate(ocrResult.splitlines()):
        if x != 0:
            dataRow = data.split()
            if len(dataRow) > 11 and int(dataRow[10]) > 70:
                row = int(dataRow[2])
                if row != currentRow:
                    currentRow = row
                    currentIndex += 1
                    resultData[dataProperty[currentIndex]] += dataRow[11]
                else:
                    resultData[dataProperty[currentIndex]] += (" " + dataRow[11])
    print(resultData)


# Main function - entry point for software
if __name__ == '__main__':
    print('OCR detection algorithm started...')

    # Set up pytessract
    pytesseract.pytesseract.tesseract_cmd = 'D:\\Software Installed\\TesseractOCR\\tesseract.exe'

    # Template/training images
    templates = ['Imageset/template_a.jpg', 'Imageset/template_p.jpg']

    # Load test image and resize to 1024 X 768
    img = cv.imread('Imageset/img_p.jpg')
    img = cv.resize(img, (1024, 768), interpolation=cv.INTER_NEAREST )

    # Identify image type
    [x, y, width, height, template] = CardDetector(templates, img)
    if width > 0 and  template == 'Imageset/template_a.jpg':
        print('Adhar card identified. Extracting information...')
        ProcessAdhar(img, x, y, width, height)
    elif width > 0 and  template == 'Imageset/template_p.jpg':
        print('PAN card identified. Extracting information...')
        ProcessPAN(img, x, y, width, height)

    cv.waitKey(0)








