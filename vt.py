

import sqlite3
from xml.etree.ElementTree import iselement 




class veriTabani():
    def __init__(self):
        self.baglanti = sqlite3.connect("Data/testVeriTabani.sqlite")
        self.imlec = self.baglanti.cursor()
    def olusturTablo(self):
        self.maskeTablo = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_maskeBilgi(id INTEGER PRIMARY KEY AUTOINCREMENT,
                maskeliSayisi TEXT,
                maskesizSayisi TEXT)""")
        self.plakaTablo = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_plakaBilgi(id INTEGER PRIMARY KEY AUTOINCREMENT,
                plakaBilgi TEXT,
                plakaTarih TEXT)""")
        self.girisCikisTablo = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_girisCikis(id INTEGER PRIMARY KEY AUTOINCREMENT,
                girisYapanSayisi TEXT,
                cikisYapanSayisi TEXT,
                girisCikisTarihi TEXT)""")
        self.riskDurumu = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_risk(id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT,
                yakınTemasOlusma TEXT)""")
        self.baglanti.close()
                
            
class AnalizIslem(veriTabani):
    def __init__(self):
        veriTabani.__init__(self)
        veriTabani().olusturTablo()
        self.plaka = None
        self.plakaTarih = None
        self.maskeli = None
        self.maskesiz = None
        self.giren = None
        self.cikan = None
    def veriCek(self,sorgu):
        self.imlec.execute(sorgu)
        return self.imlec.fetchall()
    def komutGonder(self,sorgu):
         self.imlec.execute(sorgu)
         self.baglanti.commit()

    def maskeGuncelle(self,maskeli,maskesiz):
        pass

    def girisCikisGuncelle(self,giren,cikan):
        pass
    def plakaKayitEt(self,maskesizSayisi,tarih):
        pass
    def riskDurumuKayit(self,tarih,temas):
        pass


    def ekranaBas(self):
        print("GELEN PLAKA : ,",self.plaka)
        print("GELEN MASKELİ :,",self.maskeli)
        print("GELEN MASKESİZ :,",self.maskeli)
        print("GİREN :,",self.maskeli)
        print("ÇIKAN :,",self.maskeli)
        print("Okunan Plaka :,",self.plaka)
        print("Okunan Plaka Tarih:,",self.plakaTarih)
    


    
islem = AnalizIslem()
islem.ekranaBas()










