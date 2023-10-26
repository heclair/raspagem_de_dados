import requests
from bs4 import BeautifulSoup
import csv
import time


dados = []
pasta = 'testehtml'
s = requests.Session() 
baseAdress = 'https://www.vestibularfatec.com.br/'

hd = {'Host': 'www.vestibularfatec.com.br'
     ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
     ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
     ,'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'
     ,'Accept-Encoding': 'gzip, deflate'
     ,'DNT': '1'
     ,'Connection': 'keep-alive'
     ,'Upgrade-Insecure-Requests': '1'
     ,'Sec-Fetch-Dest': 'document'
     ,'Sec-Fetch-Mode': 'navigate'
     ,'Sec-Fetch-Site': 'none'
     ,'Sec-Fetch-User': '?1'}

result = s.get(baseAdress+'home/', headers=hd)
with open("testehtml.html",'w', encoding="utf-8") as f:
        f.write(str(result.content.decode('utf-8')) )

hd = {'Host': 'www.vestibularfatec.com.br'
     ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
     ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
     ,'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'
     ,'Accept-Encoding': 'gzip, deflate'
     ,'DNT': '1'
     ,'Connection': 'keep-alive'
     ,'Referer': 'https://www.vestibularfatec.com.br/home/'
     ,'Upgrade-Insecure-Requests': '1'
     ,'Sec-Fetch-Dest': 'document'
     ,'Sec-Fetch-Mode': 'navigate'
     ,'Sec-Fetch-Site': 'same-origin'
     ,'Sec-Fetch-User': '?1'
     ,'TE': 'trailers'}

result = s.get(baseAdress+'demanda/', headers=hd)
with open(pasta+"testehtml.html",'w', encoding="utf-8") as f:
        f.write(str(result.content.decode('utf-8')) )

soup = BeautifulSoup(str(result.content), 'html.parser')
listaAnos = soup.find("select", attrs={'name':'ano-sem'}).find_all("option")

for a in listaAnos:
    if('Selecione' in a.text):
         continue
    
    hd ={'Host': 'www.vestibularfatec.com.br'
        ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
        ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        ,'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'
        ,'Accept-Encoding': 'gzip, deflate'
        ,'Content-Type': 'application/x-www-form-urlencoded'
        ,'Origin': 'https://www.vestibularfatec.com.br'
        ,'DNT': '1'
        ,'Connection': 'keep-alive'
        ,'Referer': 'https://www.vestibularfatec.com.br/demanda/'
        ,'Upgrade-Insecure-Requests': '1'
        ,'Sec-Fetch-Dest': 'document'
        ,'Sec-Fetch-Mode': 'navigate'
        ,'Sec-Fetch-Site': 'same-origin'
        ,'Sec-Fetch-User': '?1'}
    
    body = {'ano-sem': a['value']}
    result = s.post(baseAdress+'demanda/demanda.asp', data=body,headers=hd)
    with open(pasta+"testehtml.html",'w', encoding="utf-8") as f:
        f.write(str(result.content.decode('utf-8')) )

    soup = BeautifulSoup(str(result.content.decode('utf-8')), 'html.parser')
    fatecsOp = soup.find("select", attrs={'id':'FATEC'}).find_all("option")
    fatec = [x for x in fatecsOp if 'Jacare' in x['value']]
    if(len(fatec) == 0):
        continue
    vReq = soup.find("input", attrs={'name':'V_REQCodFatec'})
    anosem = soup.find("input", attrs={'name':'ano-sem'})

    body = {'FATEC': fatec[0]['value'].upper()
            ,'V_REQCodFatec': vReq['value']
            ,'ano-sem': anosem['value']}
    
   

    hd = {'Host': 'www.vestibularfatec.com.br'
         ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
         ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
         ,'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'
         ,'Accept-Encoding': 'gzip, deflate'
         ,'Content-Type': 'application/x-www-form-urlencoded'
         ,'Origin': 'https://www.vestibularfatec.com.br'
         ,'DNT': '1'
         ,'Connection': 'keep-alive'
         ,'Referer': 'https://www.vestibularfatec.com.br/demanda/demanda.asp'
         ,'Upgrade-Insecure-Requests': '1'
         ,'Sec-Fetch-Dest': 'document'
         ,'Sec-Fetch-Mode': 'navigate'
         ,'Sec-Fetch-Site': 'same-origin'
         ,'Sec-Fetch-User': '?1'}

    
    result = s.post(baseAdress+'demanda/demanda.asp', data=body, headers=hd)
    
    with open(pasta+"testehtml.html",'w', encoding="utf-8") as f:
        f.write(str(result.content.decode('utf-8')))
        
    soup = BeautifulSoup(str(result.content.decode('utf-8')), 'html.parser')
    linhaTabela = soup.find("table", attrs={"class","table table-striped"}).find_all("tr")[1:]
    time.sleep(2)
    for linha in linhaTabela:
          colunas = linha.find_all("td")
          dados.append((a.text, colunas[0].text, colunas[1].text, colunas[2].text, colunas[3].text, colunas[4].text))

    dados.append((None, None, None, None, None, None))
cabecalhos = ('SEMESTRE', 'CURSO', 'PERIODO', 'INCRITOS', 'VAGAS', 'DEMANDA')
with open ("demanda por curso e semenstre.csv", "w", newline = "") as csvfile:
    movies = csv.writer(csvfile)
    movies.writerow(cabecalhos)
    for x in dados:
      movies.writerow(x)