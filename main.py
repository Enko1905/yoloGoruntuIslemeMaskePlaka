from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget,QFileDialog
from PyQt5.QtWidgets import QApplication, QSizePolicy, QGridLayout
from PyQt5.QtCore import QTimer, QRect, Qt
from PyQt5.QtGui import QPixmap, QImage
import sys
import cv2
import analizSet as az
from arayuz import Ui_MainWindow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import datetime
import numpy as np
import plakaAnaliz as pltAnaliz
import vt


kr = [0,0]
class islem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.kameraAdress=0
        self.tanimliNesneler = []
        self.araclarArasiKordinat = []
        self.aracSinifi = ["araba","kamyon","motosiklet"]
        self.maskeTanima = False
        self.maskeTanimliInsanSec =False
        self.maskeCevreAnalizetSec =True

        self.ayiriciMesafe = False
        self.girisCikis = False
        self.plakaAnaliz = False
        self.aracResimKaydet = False
        #self.tanimlananNesneFotografi = False

        self.sapmaDegeri = 10
        self.ui.btnBaslat.clicked.connect(self.baslatVideo)
        self.ui.btnKapat.clicked.connect(app.exit)
        self.ui.btnGoruntuKaydet.clicked.connect(self.ekranKayit)
        self.ui.btnPlakaResimKontrol.clicked.connect(self.plakaResimKontrol)
        self.ui.btnSec.clicked.connect(self.dosyaYoluSec)

        self.ui.checkAraba.stateChanged.connect(self.TanimliNesneEkle)
        self.ui.checkKamyon.stateChanged.connect(self.TanimliNesneEkle)
        self.ui.checkInsan.stateChanged.connect(self.TanimliNesneEkle)
        self.ui.checkMotosiklet.stateChanged.connect(self.TanimliNesneEkle)

        self.ui.checkTanimlananArac.stateChanged.connect(self.ozellikAktiflik)
        self.ui.checkMesafe.stateChanged.connect(self.ozellikAktiflik)
        self.ui.checkGirisCikis.stateChanged.connect(self.ozellikAktiflik)
        self.ui.checkMaske.stateChanged.connect(self.ozellikAktiflik)
        self.ui.checkPlakaAnaliz.stateChanged.connect(self.ozellikAktiflik)
        self.ui.checAracResimKayit.stateChanged.connect(self.ozellikAktiflik)


        self.ui.lblHataGoster.setText("")
        self.ui.radioKamera.toggled.connect(self.kameraAktifKonum)
        self.ui.radioVideo.toggled.connect(self.videoAktifKonum)

        self.ui.radioMaskeTanimliInsan.toggled.connect(self.MaskeTanimliInsan)
        self.ui.radioMaskeCevreAnalizEt.toggled.connect(self.MaskeCevreAnalizet)
        self.ui.sldSapmaDegeri.valueChanged[int].connect(self.changeValue)

        self.ui.btnDurdur.clicked.connect(self.durdur)

        self.data = vt.AnalizIslem()

    def baslatVideo(self):
        try:
            self.startVideo()
        except Exception as hata:
            self.ui.lblHataGoster.setText("GÖRÜNTÜ OYNATILAMADI !")
        self.videoAktifKonum(1)
    def changeValue(self, value):
        self.sapmaDegeri = value
    def ekranKayit(self):
        gr,kayit = self.cap.read()
        if not gr:
            cv2.imwrite(f'ekranGoruntu/ekranGoruntu{self.data.tarih.time()}.jpg',kayit)
    def kameraAktifKonum(self,selected):
        if(selected):
            if(self.ui.txtKameraAdress.text() == ""):
                self.kameraAdress = 0
            else:
                self.kameraAdress=int(self.ui.txtKameraAdress.text())
    def MaskeTanimliInsan(self,selected):
        if(selected):
            self.maskeTanimliInsanSec =True
            self.maskeCevreAnalizetSec =False
    def MaskeCevreAnalizet(self,selected):
         if(selected):
            self.maskeCevreAnalizetSec =True
            self.maskeTanimliInsanSec =False

    def dosyaYoluSec(self):

        file , path = QFileDialog.getOpenFileName(self, 'Video Aç', '/home','video dosyası(*.*)')
        self.ui.txtVideoAdress.setText(file)

    def videoAktifKonum(self,selected):
        if(selected):
            if(self.ui.txtVideoAdress.text() == ""):
                self.kameraAdress = 0
            else:
                self.kameraAdress=str(self.ui.txtVideoAdress.text())
    def plakaResimKontrol(self):
        try:
            plaka= pltAnaliz.resimKonrol(self.ui.txtPlakaResimAdresi.text())
            self.ui.lblPlakaBilgileri.setText("PLAKA NO :"+plaka)
            self.data.plakaKayitEt(plaka)

        except Exception as hata:
            self.ui.listMessage.addItem("Plaka Adresi Okunamadı ! ")

    def ozellikAktiflik(self):
        self.ayiriciMesafe = False
        self.girisCikis = False
        self.maskeTanima =False
        self.plakaAnaliz = False
        self.aracResimKaydet =False
        self.tanimlananNesneFotografi=False
        if(self.ui.checkMesafe.isChecked()):
            self.ayiriciMesafe = True
        if(self.ui.checkGirisCikis.isChecked()):
            self.girisCikis = True
        if(self.ui.checkMaske.isChecked()):
            self.maskeTanima = True
        if(self.ui.checkPlakaAnaliz.isChecked()):
            self.plakaAnaliz = True
        if(self.ui.checkTanimlananArac.isChecked()):
            self.tanimlananNesneFotografi = True
        if(self.ui.checAracResimKayit.isChecked()):
            self.aracResimKaydet =True



    def TanimliNesneEkle(self):
        self.tanimliNesneler = []
        if(self.ui.checkAraba.isChecked()):
            self.tanimliNesneler.append("araba")
        if(self.ui.checkKamyon.isChecked()):
            self.tanimliNesneler.append("kamyon")
        if(self.ui.checkInsan.isChecked()):
            self.tanimliNesneler.append("insan")
        if(self.ui.checkMotosiklet.isChecked()):
            self.tanimliNesneler.append("motosiklet")

    def ozelliklerYaz(self):

        self.ui.lblHeight.setText(str(round(self.cap.get(3))))
        self.ui.lblWidth.setText(str(round(self.cap.get(4))))
        self.ui.lblFbs.setText(str(round(self.cap.get(5))))

    def durdur(self):
        self.ui.listMessage.addItem("KAMERA GÖRÜNTÜSÜ KAPATILDI")

        self.cap.release()

    def startVideo(self):
        self.ui.lblHataGoster.setText("")
        try:
            self.cap = cv2.VideoCapture(self.kameraAdress)
            kr[0]=0
            kr[1]=0
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.timer = QTimer()
            millisecs = int(1000.0 / fps)
            self.timer.setTimerType(Qt.PreciseTimer)
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(millisecs)

        except Exception as hata:
            print("GÖRÜNTÜ OYNATILAMADI -->",hata)
            self.ui.lblHataGoster.setText("GÖRÜNTÜ OYNATILAMADI !")
    def nextFrameSlot(self):
        self.ozelliklerYaz()
        net = cv2.dnn.readNet("yolo_tiny/yolov4-tiny.weights", "yolo_tiny/yolov4-tiny.cfg")
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(512, 512), scale=1/255)
        if(self.maskeTanima):
            self.face_cascade=cv2.CascadeClassifier('maskeModul/haarcascade_frontalface_default.xml')
            self.mymodel=load_model('maskeModul/model.h5')


        classes = []
        with open("yolo_tiny/classesTr.txt", "r") as file_object:
            for class_name in file_object.readlines():
                #print(class_name)
                class_name = class_name.strip()  # satır arası boşluklar için
                classes.append(class_name)

        ret, self.frame = self.cap.read()

        if ret == True:
            (class_ids, scores, kordinatlar) = model.detect(self.frame, confThreshold=0.5, nmsThreshold=.4)
            for class_id, score, kordinat in zip(class_ids, scores, kordinatlar):

                (self.x, self.y, self.w, self.h) = kordinat
                class_name = classes[class_id]
                if(class_name in self.tanimliNesneler):
                    cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255,20,20), 3)
                    cv2.rectangle(self.frame,(self.x,self.y-5),(self.x+140,self.y-30),(255,100,100),-1)
                    cv2.putText(self.frame, class_name+" "+str(round(score,1)), (self.x, self.y - 7), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2)
                    if(self.girisCikis):
                        self.sayNesne(class_name)
                    if(self.ayiriciMesafe):
                        self.ayiriciCiz()
                    if(self.maskeTanima):
                        self.maskeAlgila()

            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            pix = pix.scaled(self.ui.lblVid.width(), self.ui.lblVid.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.lblVid.setPixmap(pix)



    def ayiriciCiz(self):
        #frame,x,y,renk,nesne
        x_ust= round(self.x+(self.w/2))
        y_alt = round(self.y+(self.h/2))
        self.araclarArasiKordinat.append([x_ust,y_alt])
        if(len(self.araclarArasiKordinat) >=2):

            renk_cizgi=[0,255,0]

            if((self.araclarArasiKordinat[0][1]+self.sapmaDegeri)>=self.araclarArasiKordinat[1][1] or (self.araclarArasiKordinat[0][1]>=self.araclarArasiKordinat[1][1]+self.sapmaDegeri)):
                self.araclarArasiKordinat.clear()
            else:
                hesap = az.mesafeHesapla(self.araclarArasiKordinat)
                hesap = round(hesap,2)

                if(hesap<1):
                    renk_cizgi=[0,0,255]
                    cv2.putText(self.frame,("YAKIN TEMAS"),(200,200), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 9)
                    self.data.riskDurumuKayit(hesap,1)
                    self.ui.listMessage.addItem("YAKIN TEMAS TESPİT EDİLDİ !")
                self.data.riskDurumuKayit(hesap,0)

                cv2.putText(self.frame,str(hesap)+"PX/CM" , (self.x+self.w,y_alt), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 4)
                cv2.circle(self.frame,(x_ust,y_alt),10,(255,255,255),-1)
                cv2.line(self.frame,(self.araclarArasiKordinat[0][0],self.araclarArasiKordinat[0][1]),(self.araclarArasiKordinat[1][0],self.araclarArasiKordinat[1][1]),(renk_cizgi[0],renk_cizgi[1],renk_cizgi[2]),2)
                self.araclarArasiKordinat.clear()


    def sayNesne(self,aracIsmi):

        bilgi =None
        x1 = round((self.x+self.w))
        renkSen = [255,0,0,3]
        if(self.y>600 and self.y <610 and x1>0 and  x1<1200):
            if(self.plakaAnaliz):
                self.plakaAnalizet(self.frame[self.y:self.y + self.h, self.x:self.x + self.w])
            if(self.aracResimKaydet and aracIsmi in self.aracSinifi):
                cv2.imwrite(f'imagesOto/{self.x,self.y}.png',self.frame[self.y:self.y + self.h, self.x:self.x + self.w])

            renkSen = [0,255,0,-1]
            kr[0]+=1
            bilgi = "GELEN: "+str(kr[0])+" GİDEN:"+str(kr[1])
            self.data.girisCikisKayit(kr[0],kr[1])

        cv2.circle(self.frame,(x1,self.y),10,(255,255,255),-1)

        cv2.rectangle(self.frame,(100,600),(800,610),(renkSen[0],renkSen[1],renkSen[2]),renkSen[3])
        cv2.putText(self.frame,str(kr[0]),(400,590), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 2)
        cv2.putText(self.frame,("Gelenler"),(100,600), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2)

        if(self.y>600 and self.y <610 and x1>1200 and  x1<2300):
            if(self.plakaAnaliz):
                self.plakaAnalizet(self.frame[self.y:self.y + self.h, self.x:self.x + self.w])
            if(self.aracResimKaydet and aracIsmi in self.aracSinifi):
                cv2.imwrite(f'imagesOto/{self.x,self.y}.png',self.frame[self.y:self.y + self.h, self.x:self.x + self.w])
            kr[1]+=1
            renkSen = [0,255,0,-1]
            bilgi = "GELEN: "+str(kr[0])+" GİDEN:"+str(kr[1])

            self.data.girisCikisKayit(kr[0],kr[1])

        cv2.rectangle(self.frame,(1200,600),(1900,610),(renkSen[0],renkSen[1],renkSen[2]),renkSen[3])
        cv2.putText(self.frame,("Gidenler"),(1200,600), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 2)
        cv2.putText(self.frame,str(kr[1]),(1500,590), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 2)
        self.ui.listMessage.addItem(bilgi)
    def maskeAlgila(self):
        if(self.maskeCevreAnalizetSec):
            img =self.frame
        else:
            img=self.frame[self.y:self.y + self.h, self.x:self.x + self.w]
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
        face=self.face_cascade.detectMultiScale(grayImg,scaleFactor=1.1,minNeighbors=3)
        for(x,y,w,h) in face:
            face_img = img[self.y:self.y+self.h, self.x:self.x+self.w]
            cv2.imwrite('maskeModul/temp.jpg',face_img)

            test_image=image.load_img('maskeModul/temp.jpg',target_size=(150,150,3))
            test_image=image.img_to_array(test_image)
            test_image=np.expand_dims(test_image,axis=0)
            pred=self.mymodel.predict(test_image)[0][0]
            if pred==1:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                cv2.imwrite('kigsTemp/yuz.png', img[y:y+h,x:x+w], [cv2.IMWRITE_JPEG_QUALITY, 10])
                self.ui.lblMaskesiz.setPixmap(QtGui.QPixmap("kigsTemp/yuz.png"))
                cv2.putText(img,'MASKE YOK',((x+w)//2,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                cv2.putText(img,'maskesiz sayisi :'+str(face.shape[0]),(0,img.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                self.data.maskeKayit(str(face.shape[0]))
                self.ui.listMessage.addItem(f"MASKESİZ {str(face.shape[0])} KİŞİ TESBİT EDİLDİ")

            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                cv2.putText(img,'MASKE VAR',((x+w)//2,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

            datet=str(datetime.datetime.now())
            cv2.putText(img,datet,(400,450),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

    def plakaAnalizet(self,frame):
        plakaGelenVeri= pltAnaliz.readplate(frame)
        if(self.tanimlananNesneFotografi):
            cv2.imwrite('kigsTemp/tanimli.png', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])
            self.ui.lblAracResim.setPixmap(QtGui.QPixmap("kigsTemp/tanimli.png"))
            strCevirPlaka = str("Araç Girişİ PLAKA: "+str(plakaGelenVeri))
            self.ui.listMessagePlt.addItem(strCevirPlaka)
            self.data.plakaKayitEt(plakaGelenVeri)




if __name__ == "__main__":
    import sys
    app = QApplication([])
    MainWindow = islem()
    MainWindow.show()
    sys.exit(app.exec_())

