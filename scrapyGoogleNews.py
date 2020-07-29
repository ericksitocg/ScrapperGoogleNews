import random
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

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

        datos["fecha"].append(fecha)
        datos["fuente"].append(fuente.replace(",",""))
        datos["titulo"].append(titulo.replace(",",""))
        datos["encabezado"].append(encabezado.replace(",",""))

def configurarRegionUSA():
    xpath_bton_preferencias = "/html/body/div[5]/div[2]/div[3]/div/div/div[1]/div/div/div[2]/g-header-menu/a"
    xpath_bton_conf_busqueda = "/html/body/div[5]/div[2]/div[5]/div/a[1]"
    xpath_bton_mostrar_mas = "/html/body/div[3]/form/div/div[2]/div[1]/div[2]/div[6]/div/a[1]"
    xpath_bton_usa = "/html/body/div[3]/form/div/div[2]/div[1]/div[2]/div[6]/div/div/div[2]/div[1]/div[36]/div/span[1]"
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

def generarLinkPorFecha(dia,mes,anio=2020):
    link = "https://www.google.com/search?q=george+floyd&biw=1042&bih=590&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{0}%2F{1}%2F{2}%2Ccd_max%3A{0}%2F{1}%2F{2}&tbm=nws".format(mes,dia,anio)
    return link,str(dia) + "/" + str(mes) + "/" + str(anio)
#-------------------------------------------------------------------------------
datos = {"fecha":[],"fuente":[],"titulo":[],"encabezado":[]}
pagina_conf = False
# Instancio el driver de selenium que va a controlar el navegador
driver = webdriver.Chrome(ChromeDriverManager().install())
for dia in range(1,26):
    ##Scraping para el dia 26 de Mayo del 2020
    pagina_principal,fecha = generarLinkPorFecha(dia,7)

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
df = pd.DataFrame(datos,columns = ['fecha', 'fuente', 'titulo', 'encabezado'])
df.to_csv('data_google_news3.csv',index=False)
