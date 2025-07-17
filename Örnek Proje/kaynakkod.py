from tekrar import *
from PyQt5.QtWidgets import *
import sys
import enum
import datetime


flagdil=0#turkce
flagaciklama=""#zorunsuz

#Uygulama Gösterme

app=QApplication(sys.argv)#uygulama nesnesi
window=QMainWindow()#pencere nesnesi
ui=Ui_MainWindow()#ui nesnesi
ui.setupUi(window)#pencereyi doldur
window.show()#doldurulan pencereyi göster



if flagdil==0:
    ui.tableWidget_Liste.setHorizontalHeaderLabels(("Numara","Ad","Soyad","Tarih","Bölüm","Aciklama"))
elif flagdil==1:
    ui.tableWidget_Liste.setHorizontalHeaderLabels(("Number","Name","Surname","Date","Department","Description"))
ui.tableWidget_Liste.horizontalHeader().setStyleSheet("color:rgb(158,44,106);font-size:20px;font-weight:bold")

#Veri Tabanı İşlemleri
import sqlite3
veritabani=sqlite3.connect("tekrar.db")
veritabani.commit()
yertutucu=veritabani.cursor()
tablo="""create table if not exists tekrar (Numara integer primary key not null, Ad text not null,\n
        Soyad text not null, Tarih text not null,Bolum text not null,Aciklama text )"""

yertutucu.execute(tablo)
veritabani.commit()


def veriekleme():
    num=ui.lineEdit_Numara.text()
    ad=ui.lineEdit_Ad.text()
    soyad=ui.lineEdit_Soyad.text()
    tarih=ui.dateEdit.dateTime().date().toString("dd-MM-yyyy")
    bolum=ui.comboBox_bolum.currentText()
    aciklama=ui.plainTextEdit_Aciklama.toPlainText()

    if flagaciklama==0:

        if num=="" or ad=="" or soyad=="" or bolum=="":
            if flagdil==0:
                QMessageBox.information(window,"Bilgilendirme","Lütfen tüm alanları eksiksiz doldur")
            elif flagdil==1:
                QMessageBox.information(window,"Information","Please Fill All Field ")
            return#fonksiyonu kır
    
        try:
            int(num)

        except ValueError:
            if flagdil==0:
                ui.statusbar.showMessage("Lütfen Tam Sayi Giriniz",3000)
            elif flagdil==1:
                 ui.statusbar.showMessage("Please Enter Integer Value",3000)
            ui.statusbar.setStyleSheet("color:red;font-size:20px;")
            return#Fonksiyonu kır
    
        sorgu="insert into tekrar (Numara,Ad,Soyad,Tarih,Bolum,Aciklama) values(?,?,?,?,?,?)"

        try:
            yertutucu.execute(sorgu,(num,ad,soyad,tarih,bolum,aciklama))
            veritabani.commit()
            if flagdil==0:
                #QMessageBox.information(window,"Bilgi","Kayit işlemi Başarılı")
                ekleolumlu()
            if flagdil==1:
                QMessageBox.information(window,"İnformation","Registration Successful")

        except Exception as a:
            if flagdil==0:
                ui.statusbar.showMessage(str(a)+" :HATA KODU")
            if flagdil==1:
                ui.statusbar.showMessage(str(a)+" :ERROR CODE")
            ui.statusbar.setStyleSheet("color:red;font-size:20px")

    elif flagaciklama==1:#zorunlu
        if num=="" or ad=="" or soyad=="" or bolum=="" or aciklama=="" :
            if flagdil==0:
                QMessageBox.information(window,"Bilgilendirme","Lütfen tüm alanları eksiksiz doldur")
            elif flagdil==1:
                QMessageBox.information(window,"İnformation","Please Fill All The Necsseary Field")
            return#fonksiyonu kır
    
        try:
            int(num)

        except ValueError:
            if flagdil==0:
                ui.statusbar.showMessage("Lütfen Tam Sayi Giriniz",3000)
            elif flagdil==1:
                ui.statusbar.showMessage("Please Enter Integer Value",3000)
            ui.statusbar.setStyleSheet("color:red;font-size:20px;")
            return#Fonksiyonu kır
    
        sorgu="insert into tekrar (Numara,Ad,Soyad,Tarih,Bolum,Aciklama) values(?,?,?,?,?,?)"

        try:
            yertutucu.execute(sorgu,(num,ad,soyad,tarih,bolum,aciklama))
            veritabani.commit()
            QMessageBox.information(window,"Bilgi","Kayit işlemi Başarılı")

        except Exception as a:
            ui.statusbar.showMessage(str(a)+" :HATA KODU")
            ui.statusbar.setStyleSheet("color:red;font-size:20px")


    else:
        QMessageBox.information(window,"BİLGİLENDİRME","Lütfen Zorunluluk Var mı Yok mu?")







def verisil():
    #num=ui.lineEdit_Numara.text()
    #ad=ui.lineEdit_Ad.text()

    secilenveri=ui.tableWidget_Liste.selectedItems()
    if not secilenveri:
        QMessageBox.information(window,"BOŞ","Seçilen Veri yok")
        return#fonksiyonu kır
    silinecekveri=secilenveri[0].text()

    QMessageBox.question(window,"Onay",secilenveri[1].text()+" Adlı Kişini Kaydını Silmek İstediğinize Emin Misiniz",QMessageBox.Yes|QMessageBox.No)

    if QMessageBox.Yes:
        sorgu="delete from tekrar where Numara={}".format(silinecekveri)
        try:
            yertutucu.execute(sorgu)
            veritabani.commit()
            ui.statusbar.showMessage("Silme İşlemi Başarılı",3000)
        except Exception as a:
            ui.statusbar.showMessage(str(a)+" Silme İşlemi Başarısız",3000)






def verilistele():
    ui.tableWidget_Liste.clear()
    if flagdil==0:
        ui.tableWidget_Liste.setHorizontalHeaderLabels(("Numara","Ad","Soyad","Tarih","Bölüm","Aciklama"))
    elif flagdil==1:
        ui.tableWidget_Liste.setHorizontalHeaderLabels(("Number","Name","Surname","Date","Department","Description"))
    ui.tableWidget_Liste.horizontalHeader().setStyleSheet("color:rgb(158,44,106);font-size:20px;font-weight:bold;")

    sorgu="select * from tekrar"
    try:
        yertutucu.execute(sorgu)
        for i,j in enumerate(yertutucu):
            for k,s in enumerate(j):
                ui.tableWidget_Liste.setItem(i,k,QTableWidgetItem(str(s)))
        ui.tableWidget_Liste.resizeColumnsToContents()

    except:
        ui.statusbar.showMessage("Başaramadık Abi",3000)
        ui.statusbar.setStyleSheet("color:red;font-size:20px") 

def veriguncelle():
    num=ui.lineEdit_Numara.text()
    ad=ui.lineEdit_Ad.text()
    soyad=ui.lineEdit_Soyad.text()
    tarih=ui.dateEdit.dateTime().date().toString("dd-MM-yyyy")
    bolum=ui.comboBox_bolum.currentText()
    aciklama=ui.plainTextEdit_Aciklama.toPlainText()

    sorgu="update tekrar set Ad=?,Soyad=?,Tarih=?,Bolum=?,Aciklama=? where Numara=?"

    try:
        yertutucu.execute(sorgu,(ad,soyad,tarih,bolum,aciklama,num))
        veritabani.commit()
        QMessageBox.information(window,"Bilgi","Guncelleme işlemi Başarılı")
    except Exception as a:
        ui.statusbar.showMessage(str(a)+" Güncelleme İşlemi Başarısız",3000)
        ui.statusbar.setStyleSheet("color:red;font-size:20px")  







def doldur():
    secilenveri=ui.tableWidget_Liste.selectedItems()


    if not secilenveri:
        return

    ui.lineEdit_Numara.setText(secilenveri[0].text())
    ui.lineEdit_Ad.setText(secilenveri[1].text())
    ui.lineEdit_Soyad.setText(secilenveri[2].text())
    ui.comboBox_bolum.setCurrentText(secilenveri[4].text())
    #ui.dateEdit.setDateTime(secilenveri[3].text())
    ui.plainTextEdit_Aciklama.setPlainText(secilenveri[5].text())




def ingilizcecevir():
    global flagdil

    flagdil=1

    ui.label_ingilizce.setText("ENGLISH")
    ui.label_ad.setText("NAME")
    ui.label_bolum.setText("DEPARTMENT")
    ui.label_numara.setText("NUMBER")
    ui.label_soyad.setText("SURNAME")
    ui.label_tarih.setText("DATE")
    ui.label_turkce.setText("TURKISH")
    ui.label_zorunlu.setText("COMPULSORY")
    ui.label_zorunsuz.setText("OPTIONAL")
    ui.pushButton_ekle.setText("ADD")
    ui.pushButton_guncelle.setText("UPDATE")
    ui.pushButton_listele.setText("LIST")
    ui.pushButton_sil.setText("DELETE")

    verilistele()


def turkcecevir():

    global flagdil

    flagdil=0

    ui.label_ingilizce.setText("İNGİLİZCE")
    ui.label_ad.setText("AD")
    ui.label_bolum.setText("BÖLÜM")
    ui.label_numara.setText("NUMARA")
    ui.label_soyad.setText("SOYAD")
    ui.label_tarih.setText("TARİH")
    ui.label_turkce.setText("TÜRKÇE")
    ui.label_zorunlu.setText("ZORUNLU")
    ui.label_zorunsuz.setText("ZORUNSUZ")
    ui.pushButton_ekle.setText("EKLE")
    ui.pushButton_guncelle.setText("GÜNCELLE")
    ui.pushButton_listele.setText("LİSTELE")
    ui.pushButton_sil.setText("SİL")

    verilistele()




def zorunlu():
    global flagaciklama
    flagaciklama=1


def zorunsuz():
    global flagaciklama
    flagaciklama=0




def ekleolumlu():
    kutu=QMessageBox()
    kutu.setWindowTitle("Bilgi")
    #kutu.setWindowIcon(QMessageBox.information)
    kutu.setStandardButtons(QMessageBox.Ok)
    kutu.setText("Kayıt Başarılı")
    kutu.setStyleSheet("color:green;font-size:20px;background-color:white")
    kutu.setGeometry(200,200,400,200)

    kutu.exec()

   

#Buton signal interrupt

ui.pushButton_ekle.clicked.connect(veriekleme)
ui.pushButton_sil.clicked.connect(verisil)
ui.pushButton_listele.clicked.connect(verilistele)
ui.pushButton_guncelle.clicked.connect(veriguncelle)
ui.tableWidget_Liste.clicked.connect(doldur)
ui.radioButton_ingilizce.clicked.connect(ingilizcecevir)
ui.radioButton_turkce.clicked.connect(turkcecevir)
ui.checkBox_zorunlu.clicked.connect(zorunlu)
ui.checkBox_zorunsuz.clicked.connect(zorunsuz)



sys.exit(app.exec_())#Ugulama çıkma sinyali