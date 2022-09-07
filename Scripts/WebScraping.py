from calendar import firstweekday
from multiprocessing.sharedctypes import Value
from datetime import datetime

from selenium import webdriver
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ScrollOrigin
import time

#exe_path = GeckoDriverManager().install()
#service=Service(exe_path)
#options = Options()
# options.headless = True
#options.add_argument("--incognito")
#browser = webdriver.Firefox(service=service, options=options)
browser = webdriver.Chrome()

#posts = []

url = 'https://twitter.com/search?q=ELEI%C3%87%C3%95ES%202022&src=typed_query&f=live'

browser.get(url) #Abre o site

chave = ['bolsonaro','eleições 2022','lula','ciro gomes','simone tebet','felipe d’avila','leo pericles','roberto jefferson']
chaveEs = ['Carlos Manato','Audifax','Renato Casagrande','Guerino Zanon','Aridelmo','Claudio Paiva','Capitão Vinicius Sousa']

action = ActionChains(browser) #Utilizado para executar algumas ações especiais 

def name_aleatory():
    hora = datetime.now()
    hora=str(hora)
    caracter = " .-:"

    for c in caracter:
        if c in hora:
            hora=hora.replace(c,'')
    return hora        

def find_posts(key,file_name):
    time.sleep(5)
    pesquisa = browser.find_element('xpath', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    pesquisa.click()
    time.sleep(2)
    
    
    
    for i in key: #Percorre as chaves para utilizar na pesquisa

        posts = []

        pesquisa.send_keys(Keys.CONTROL + 'A') #Seleciona todo o texto da barra de pesquisa
        pesquisa.send_keys(Keys.BACKSPACE) #Apaga o texto que está na barra de pesquisa

        pesquisa.send_keys(i) #Passa a palavra chave para busca
        time.sleep(2)
        pesquisa.send_keys(Keys.ENTER)
        
         
        #while(True):

        for j in range(0,5): #Loop para continuar pegando os posts
            time.sleep(10)
            txt = browser.find_elements('xpath', "//div/div[@data-testid='tweetText']") #Pega os textos dos posts já visiveis na página
            #date_post = browser.find_element('xpath', "//*[@id='id__ubzlzwbe559']/div[2]/div/div[3]/a/time")
        
            for p in range(0,len(txt)): 
                #print(txt[p].text)          
                #posts.append(date_post[p].text, "\t", txt[p].text) #salva o texto dos posts no vetor
                #print(txt[p].text.split("\n"))
                frase = txt[p].text.split("\n")
                linha = ""
                for f in frase:
                    linha += f
                
                posts.append(linha+"\n") #salva o texto dos posts no vetor
                
                
            action.scroll_by_amount(0,4000).perform() #Rola a página para atualizar os posts
            action.scroll_by_amount(0,2000).perform() #Rola a página para atualizar os posts
            
        
            
       # arquivo = open(file_name + '.txt','w') #Cria/Abre o arquivo para escrita
        arquivo = open('.\DataBase\\'+i+file_name+'.txt','w', encoding="utf-8")
        for k in range(0,len(posts)):
            str(arquivo.write(posts[k])).encode(errors="ignore")
            #print(posts[k])
          #  arquivo.write(posts[k]) #Escreve cada linha de texto no arquivo

        arquivo.close() #Fecha o arquivo

        time.sleep(2)
        pesquisa.click()
        time.sleep(2)

find_posts(chave, name_aleatory())

find_posts(chaveEs, name_aleatory())
