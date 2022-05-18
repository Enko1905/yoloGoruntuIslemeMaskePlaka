from ast import Global
from logging import exception
from os import listdir
import pytesseract, cv2, imutils as imt, datetime
import os
# plt degisken
plt =""
def readplate(gelenFrame):

    #pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    try:    
        DTNo = datetime.datetime.now()
        DTNow = str(datetime.datetime.ctime(DTNo))
        Plakalar = []
        contour_with_license_plate = None
        license_plate = None
        x = None
        y = None
        w = None
        h = None
        image = gelenFrame
        image = imt.resize(image, width=500, inter=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filter = cv2.bilateralFilter(gray_image, 11, 17, 17)
        canny_edge = cv2.Canny(filter, 100, 200)
        contours, new = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:
                contour_with_license_plate = approx
                x, y, w, h = cv2.boundingRect(contour)
                license_plate = gray_image[y:y + h, x:x + w]
                break

        (thresh, blackAndWhiteImage) = cv2.threshold(license_plate, 100, 255, cv2.THRESH_BINARY)
        texto = pytesseract.image_to_string(blackAndWhiteImage, config='--psm 6')
        global plt 
        plt = texto
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        image = cv2.putText(image, texto.upper(), (x + 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,cv2.LINE_AA)
        with open("Plates.txt", "a") as dosya:
            if texto not in Plakalar:
                Plakalar.append(texto)
                for i in Plakalar:
                    dosya.write(f' \n {i} arac su {DTNow} vakitte geldi.')
            return str("Araç Giriş Tarih: "+DTNow+" PL: "+plt)

    except Exception as e:
        print("Tanımlanamıyan Plaka --> "+str(e))

def resimKonrol(adress):
    resim = cv2.imread(adress)
    readplate(resim)
    return plt 
