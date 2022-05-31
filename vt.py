

import sqlite3
import datetime



class veriTabani():
    def __init__(self):
        self.baglanti = sqlite3.connect("Data/kayitVeriTabani.sqlite")
        self.imlec = self.baglanti.cursor()
    def olusturTablo(self):
        self.maskeTablo = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_maskeBilgi(id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT,
                maskeliSayisi INTEGER,
                maskesizSayisi INTEGER)""")
        self.plakaTablo = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_plakaBilgi(id INTEGER PRIMARY KEY AUTOINCREMENT,
                plakaBilgi TEXT,
                tarih TEXT)""")
        self.girisCikisTablo = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_girisCikis(id INTEGER PRIMARY KEY AUTOINCREMENT,
                girisYapanSayisi INTEGER,
                cikisYapanSayisi INTEGER,
                girisCikisTarihi TEXT)""")
        self.riskDurumu = self.imlec.execute("""CREATE TABLE IF NOT EXISTS TBL_risk(id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT,
                yakınTemasOlusma INTEGER)""")
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
        self.tarih = datetime.datetime.now()

    def veriCekFetch(self,sorgu):
        self.imlec.execute(sorgu)
        return self.imlec.fetchall()
    def komutGonder(self,sorgu):
         self.imlec.execute(sorgu)
         self.baglanti.commit()

    def maskeKayit(self,maskesiz):
        self.maskeTarih = self.tarih.strftime("%x")
        self.imlec.execute(f"insert into TBL_maskeBilgi (tarih,maskesizSayisi) values ('{self.maskeTarih}',{maskesiz})")
        self.baglanti.commit()

    def girisCikisKayit(self,giren,cikan):
        self.imlec.execute(f"insert into TBL_girisCikis (girisYapanSayisi,cikisYapanSayisi,girisCikisTarihi) values ({giren},{cikan},'{self.tarih}')")
        self.baglanti.commit()
    def plakaKayitEt(self,plaka):
        self.imlec.execute(f"insert into TBL_plakaBilgi (tarih,plakaBilgi) values ('{self.tarih}','{plaka}')")
        self.baglanti.commit()
    def riskDurumuKayit(self,temas):
        self.imlec.execute(f"insert into TBL_risk (tarih,yakınTemasOlusma) values ('{self.tarih}',{temas})")
        self.baglanti.commit()

    #DAHA SONRA EKLENECEL TOPLU LİSTELEME
    def ekranaBas(self):
        print("GELEN PLAKA : ,",self.plaka)
        print("GELEN MASKELİ :,",self.maskeli)
        print("GELEN MASKESİZ :,",self.maskeli)
        print("GİREN :,",self.maskeli)
        print("ÇIKAN :,",self.maskeli)
        print("Okunan Plaka :,",self.plaka)
        print("Okunan Plaka Tarih:,",self.plakaTarih)
    


"""
islem = AnalizIslem()

islem.maskeKayit(3)
# iki tarih arasındai giris ckis
print(islem.veriCekFetch("select * from TBL_girisCikis where girisCikisTarihi between '2022-05-29' and '2022-05-30'"))
islem.girisCikisKayit(3,5)
islem.plakaKayitEt("13 ab 1313")
islem.riskDurumuKayit(1)
"""







