import random
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(ChromeDriverManager().install())

pagina_principal = "https://www.google.com/search?q=george+floyd&sxsrf=ALeKk00mlmMfAJrvFtmSAz2Bz_MIyu-zSA:1595976538932&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjVpbD1g_HqAhXKmuAKHRSaCWgQ_AUoA3oECHYQBQ&biw=1299&bih=620&safe=images"

#Voy a la pagina que quiero
driver.get(pagina_principal)

#Configurando region y numero de noticias por seccion

xpath_bton_herramientas = "/html/body/div[5]/div[2]/div[3]/div/div/div[1]/div/div/div[2]/a"
xpath_bton_preferencias = "/html/body/div[5]/div[2]/div[3]/div/div/div[1]/div/div/div[2]/g-header-menu/a"
xpath_bton_conf_busqueda = "/html/body/div[5]/div[2]/div[5]/div/a[1]"
xpath_bton_mostrar_mas = "/html/body/div[3]/form/div/div[2]/div[1]/div[2]/div[6]/div/a[1]"
xpath_bton_usa = "/html/body/div[3]/form/div/div[2]/div[1]/div[2]/div[6]/div/div/div[2]/div[1]/div[36]/div/span[1]"
xpath_btn_guardar = "/html/body/div[3]/form/div/div[2]/div[2]/div/div[1]"

#Identifico a las noticias en la estructura html
btn_preferencias = driver.find_element_by_xpath(xpath_bton_preferencias)
btn_preferencias.click()
sleep(random.uniform(random.randint(3,5),8.56))

btn_conf_busqueda = driver.find_element_by_xpath(xpath_bton_conf_busqueda)
btn_conf_busqueda.click()
sleep(random.uniform(random.randint(3,5) + random.random(),8.56))

btn_mostrar_mas = driver.find_element_by_xpath(xpath_bton_mostrar_mas)
btn_mostrar_mas.click()
sleep(random.uniform(random.randint(3,5),8.56))

btn_usa = driver.find_element_by_xpath(xpath_bton_usa)
btn_usa.click()
sleep(random.uniform(random.randint(3,5),8.56))

btn_guardar = driver.find_element_by_xpath(xpath_btn_guardar)
btn_guardar.click()
sleep(random.uniform(random.randint(3,5),8.56))

driver.switch_to.alert.accept()

#Extrayendo las noticias
#Cada noticia es un elemento tipo g-card

#Fuente: /html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[8]/g-card/div/div/div[2]/a/div/div[2]/div[1]/text()
#Titulo: /html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[8]/g-card/div/div/div[2]/a/div/div[2]/div[2]/text()
#Encabezado: /html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[8]/g-card/div/div/div[2]/a/div/div[2]/div[3]/div[1]/text()
#fecha: /html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[8]/g-card/div/div/div[2]/a/div/div[2]/div[3]/div[2]/span/span/span/text()
