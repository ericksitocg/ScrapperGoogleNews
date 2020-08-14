import random
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from playsound import playsound


def dormir():
    sleep(random.uniform(random.randint(3, 6) + random.random(), 10 + random.random()))

def clickEnElemento(rutaxpath):
    btn_elemento = driver.find_element_by_xpath(rutaxpath)
    btn_elemento.click()
    dormir()

def recoletarNoticias(datos,fecha):
    # Cada noticia es un elemento tipo g-card
    noticias = driver.find_elements_by_xpath('//g-card/div/div/div[2]/a/div/div[2]')

    for noticia in noticias:
        try:
            fuente = noticia.find_element_by_xpath('./div[1]').text
        except:
            fuente = ""
        try:
            titulo = noticia.find_element_by_xpath('./div[2]').text
        except:
            titulo = ""
        try:
            encabezado = noticia.find_element_by_xpath('./div[3]/div').text
        except:
            encabezado = ""
        if fuente!="" and titulo!="" and encabezado!="":
            datos["fecha"].append(fecha)
            datos["fuente"].append(fuente.replace(",",""))
            datos["titulo"].append(titulo.replace(",",""))
            datos["encabezado"].append(encabezado.replace(",",""))
            print("dato ok")
        else:
            print("dato no valido")

def configurarRegionUSA():
    xpath_bton_preferencias = "/html/body/div[5]/div[2]/div[3]/div/div/div[1]/div/div/div[2]/g-header-menu/a"
    xpath_bton_conf_busqueda = "/html/body/div[5]/div[2]/div[5]/div/a[1]"
    xpath_bton_mostrar_mas = "/html/body/div[3]/form/div/div[2]/div[1]/div[2]/div[6]/div/a[1]"
    xpath_bton_usa = "/html/body/div[3]/form/div/div[2]/div[1]/div[2]/div[6]/div/div/div[2]/div[1]/div[37]/div/span[1]"
    xpath_btn_guardar = "/html/body/div[3]/form/div/div[2]/div[2]/div/div[1]"

    # Identifico a las noticias en la estructura html
    clickEnElemento(xpath_bton_preferencias)
    clickEnElemento(xpath_bton_conf_busqueda)
    clickEnElemento(xpath_bton_mostrar_mas)
    clickEnElemento(xpath_bton_usa)
    clickEnElemento(xpath_btn_guardar)

    driver.switch_to.alert.accept()

def siguientePaginaNoticias():
    xpath_bton_siguiente = "//a[@id='pnnext']"
    try:
        btn_siguiente = driver.find_element_by_xpath(xpath_bton_siguiente)
        btn_siguiente.click()
        sleep(10)
        return True
    except:
        return False


def generarLinkPorFecha(palabras_clave,dia,mes,anio=2020):
    if palabras_clave.count(" ") > 0:
        clave = "+".join(palabras_clave.split(" "))
    else:
        clave = palabras_clave
    link = "https://www.google.com/search?q={3}&biw=1042&bih=590&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{0}%2F{1}%2F{2}%2Ccd_max%3A{0}%2F{1}%2F{2}&tbm=nws".format(mes,dia,anio,clave)
    return link,str(dia) + "/" + str(mes) + "/" + str(anio)

def obtenerNoticiasFecha(palabra_clave,dia,mes,anio=2020):
    L_mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    datos = {"fecha": [], "fuente": [], "titulo": [], "encabezado": []}
    pagina_conf = False
    if dia.count("-") > 0:
        inicio,final = dia.split("-")
    else:
        inicio,final = dia,dia
    print(inicio,final)
    for dia_i in range(int(inicio),int(final) + 1):

        pagina_principal,fecha = generarLinkPorFecha(palabra_clave,dia_i,mes)#Se configura el mes

        #Voy a la pagina que quiero
        driver.get(pagina_principal)

        #Configurando region y numero de noticias por seccion
        if not pagina_conf:
            configurarRegionUSA()
            pagina_conf = True

        #Pagina configurada, ahora vamos a recoger las noticias
        recoletarNoticias(datos,fecha)

        #Debemos avanzar hasta la siguiente pagina
        while siguientePaginaNoticias():
            recoletarNoticias(datos,fecha)
        print("Terminado: %s"%fecha)

    #guardando datos
    nombreUnido = "".join(list(map(lambda x:x.capitalize(),palabra_clave.split(" "))))
    os.makedirs('datasets/' + nombreUnido.lower(),exist_ok=True)
    nombre_archivo = nombreUnido + L_mes[int(mes) - 1]
    df = pd.DataFrame(datos,columns = ['fecha', 'fuente', 'titulo', 'encabezado'])
    df.to_csv('datasets/'+nombreUnido.lower() + '/' +nombre_archivo+'.csv',index=False)
    print("News guardados exitosamente en " + nombre_archivo + ".csv")
    while True:
        playsound("alert.mp3")
        sleep(10)

#----------------------------------------------------------------------------------------------------------------------------------------

# Instancio el driver de selenium que va a controlar el navegador
driver = webdriver.Chrome(ChromeDriverManager().install())
#Las noticias sobre un covid-19 desde 1 hasta el 31 de Enero
obtenerNoticiasFecha("covid-19","1-31","1")
#Las noticias sobre un covid-19 desde 1 hasta el 29 de Febrero
#obtenerNoticiasFecha("covid-19","1-29","2")
#Las noticias sobre un covid-19 desde 1 hasta el 31 de Marzo
#obtenerNoticiasFecha("covid-19","1-31","3")
#Las noticias sobre un covid-19 desde 1 hasta el 30 de Abril
#obtenerNoticiasFecha("covid-19","1-30","4")
#Las noticias sobre un covid-19 desde 1 hasta el 31 de Mayo
#obtenerNoticiasFecha("covid-19","1-31","5")
#Las noticias sobre un covid-19 desde 1 hasta el 30 de Junio
#obtenerNoticiasFecha("covid-19","1-30","6")
#Las noticias sobre un covid-19 desde 1 hasta el 31 de Julio
#obtenerNoticiasFecha("covid-19","1-31","7")


