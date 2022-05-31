

from cv2 import sqrt
from numpy import square
import cv2

#birden fazla tekrar eden verileri sıralama algoritması
#goruntu icinde su an kullanılmıyor !
def SetIsleme(tanimliArr):
    bulunan = []
    for arrA in range(len(tanimliArr)):
        for arrB in tanimliArr:
            if(tanimliArr[arrA]==arrB and (arrA != tanimliArr.index(arrB)) and (arrB not in bulunan)):
                bulunan.append(arrB)
                break   
    bulunan.sort()
    print(bulunan)


#konrinat verilerini txt'ye kayıt içi oluşturuldu 
#goruntu icinde su an kullanılmıyor !
def kayitTxt(kordinatArr):
    dosya = open("kordinat.txt","w")
    for arr in kordinatArr:
        dosya.write(str(arr)+"\n")
    dosya.close()

#test su an kullanılmıyor
def Takip(test,sapma_degeri):
    ciz = True
    if(test[0][1]+sapma_degeri>=test[1][1] or test[0][1]<=test[1][1]+sapma_degeri):
        ciz = False
    return ciz



#px*cm mesafe hesaplama
def mesafeHesapla(merkezArr):
    b = abs(merkezArr[0][0] - merkezArr[1][0])
    a = abs(merkezArr[0][1] - merkezArr[1][1])
    c = ((a**2)+(b**2))
    return (round(c)**0.5)*0.026458333
    



def goruntuKayitArac(frame,x,y,w,h):
        kyt ="imagesOto/"+(str(x)+str(y))+".png"
        img = cv2.getRectSubPix(frame,(w+50,h+50),(x,y))
        cv2.imwrite(kyt,img)

def goruntuKayitInsan(frame,x,y,w,h):
        kyt ="imagesFace/"+(str(x)+str(y))+".png"
        img = cv2.getRectSubPix(frame,(w+50,h+50),(x,y))
        cv2.imwrite(kyt,img)       





