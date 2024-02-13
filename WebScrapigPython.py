from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

navegador = webdriver.Firefox()

navegador.get('https://www.rottentomatoes.com/m/joker_2019')


#Achando o botão de carregar comentários
criticas = navegador.find_element(By.PARTIAL_LINK_TEXT,'All Critics')
criticas.click()

#Carregando a pagina inteira
interacoes = 0
load_more = navegador.find_element(By.CLASS_NAME,"load-more-container")
for interacoes in range(0,30,1):
    load_more.click()
    sleep(1)

#Salvando a pagina inteira
pagina_inteira = navegador.page_source
pagina = BeautifulSoup(pagina_inteira,'html.parser')

#Salvando todos os comentarios
comentarios = pagina.findAll('p',class_ ='review-text')

#Retirar as marcações HTML
lista = []
for x in comentarios:
    lista.append(x.text)

#Salvar os elementos em uma unica string
texto = ""
for frase in lista:
    texto = texto + frase

#Criando uma nuvem de palavras
mascara = np.array(Image.open('joker1.webp'))
mapa_cores = ImageColorGenerator(mascara)

stop = set(list(STOPWORDS) + ['Joker'] +
           ['Joaquin'] + ['Full'] + ['Review']
           + ['Phoenix'] + ['Film'] + ['Movie']
           + ['Us'] + ['Spanish'] + ['Will']
           + ['Phillips'] + ['Todd']) 


nuvem_palavras = WordCloud(stopwords = stop,
                          background_color = "white",
                          min_font_size = 10,
                          max_words = 200,
                          contour_color = "black",
                          mask = mascara).generate(texto)
nuvem_palavras.recolor(color_func = mapa_cores)

#Plotando as imagens
figura,graficos = plt.subplots(1,2,figsize=(20,10))
graficos[0].imshow(mascara) 
graficos[0].set_axis_off()
graficos[0].set_xlim(250,1700)
graficos[0].set_ylim(1700,250)

graficos[1].imshow(nuvem_palavras,aspect='auto')
graficos[1].set_axis_off()

graficos[1].set_xlim(250,1700)
graficos[1].set_ylim(1700,250)
plt.show()
