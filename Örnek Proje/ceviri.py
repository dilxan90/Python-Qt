from PyQt5 import uic#uic(ui compiler or ui converter)
with open("tekrar.py","w",encoding="utf-8") as dosya:#açılacak dosya
    uic.compileUi("Tekrar.ui",dosya)#ui dosyasını derle açtığın dosyaya kodlarını koy