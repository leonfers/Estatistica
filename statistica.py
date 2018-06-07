#Atividade de Estatistica
#uso de dados para fazer calculos estitisticos referente a alguma base de dados
#dados usados sao provindos da STEAMAPI , uma api que fornece dados referentes a jogos disponiveis na STEAMAPI

import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Para pegar dados online
base_url = "http://steamspy.com/api.php?request="
response = requests.get(base_url+"all")
data = json.loads(response.text)

# with open('api.php.json') as json_file:
#     text = json_file.read()
#     data = json.loads(text)

games = []

class Game(object):
    name = ""
    userscore = 0
    price = 0

    def __init__(self, name, userscore, price):
        self.name = name
        self.userscore = userscore
        self.price = price

    def __str__(self):
        return self.name +" score: "+str(self.userscore)+" $: "+ str(self.price)


for i in data:
    obj = Game(data[i]['name'],int(data[i]['userscore']),float(data[i]['price'])/100)
    if(obj.price<=60):
        games.append(obj)

class Analyzer(object):
    lista=[]

    def __init__(self, dados):
        self.lista=dados

    def get_max_price(self):
        mv=0
        title=""
        for i in self.lista:
            if i.price>mv:
                mv = i.price
                title = i.name

        return mv

    def get_min_price(self):
        mv=99999
        title=""
        for i in self.lista:
            if i.price<mv:
                mv = i.price
                title = i.name

        return mv
    
    def get_amplitude(self):
        return (self.get_max_price() - self.get_min_price())
    
    def get_size(self):
        return len(self.lista)
    
    def get_media(self):
        total = 0
        for i in self.lista:
            total=total+i.price
        
        return total/float(self.get_size())
    
    def get_mediana(self):
        self.lista.sort(key=lambda x: x.price)
        if(self.get_size()%2==0):
            return (self.lista[(self.get_size()//2)-1].price+self.lista[self.get_size()//2].price)/2
        else:
            return self.lista[(self.get_size()//2+1)-1].price
        
    def get_free(self):
        free = []
        for i in self.lista:
            if(60 <=i.price):
                free.append(i)
        return len(free)
    
    def get_matrix(self):
        self.lista.sort(key=lambda x: x.price)
        dados = []
        frequencias = []
        
        for i in self.lista:
            if not len(dados)==0:
                if i.price != dados[0].price :
                    frequencias.append(dados[:])
                    dados = []
                    dados.append(i)
                    if i == self.lista[len(self.lista)-1]:
                        frequencias.append(dados[:])
                else:
                    if(len(dados)==len(self.lista)-1):
                        dados.append(i)
                        frequencias.append(dados[:])
                    else:
                        dados.append(i)
            else:
                if(len(dados)==len(self.lista)-1):
                        dados.append(i)
                        frequencias.append(dados[:])
                else:
                    dados.append(i)
    
        return frequencias
    
    def get_modinha(self):
        moda = []
        for i in self.get_matrix():
            if len(i)>len(moda):
                moda = i
        
        return moda[0].price

    def get_variancia(self):
        media = self.get_media()
        soma_total_amostras = 0
        for i in self.lista:
            soma_total_amostras += (i.price - media)**2
        return soma_total_amostras/float(len(self.lista))
    
    def get_desvio_padrao(self):
        return self.get_variancia()**0.5
    
    def get_coeficiente_de_variacao(self):
        return (self.get_desvio_padrao()/self.get_media()) * 100
    
    def get_classes(self):
        self.lista.sort(key=lambda x: x.price)
        classes=[]
        classe=[]
        contador = 0
        divisoriasI=[]
        for i in range(15):
            divisoriasI.append(contador)
            contador+=4
        
        divisoriasF=[]
        contador=4
        for i in range(15):
            divisoriasF.append(contador)
            contador+=4
       
        for i in range(len(divisoriasI)):
            classes.append(classe[:])

        for j in self.lista:
            for i in range(len(divisoriasI)):
                if(divisoriasI[i]<=j.price<divisoriasF[i]):
                    classes[i].append(j)

        return classes

class AnalyzerG(object):
    lista=[]

    def __init__(self, dados):
        self.lista=dados
    
    def get_media(self):
        dados = 0
        for i in self.lista:
            dados += (float(i[0]+i[1])/2)*i[2]
        frequencias_acumulada = self.get_somatorio_frequencia_absoluta()
        
        return float(dados)/frequencias_acumulada
    
    def get_mediana(self):
        somatorio_frequencia_absoluta_simples = self.get_somatorio_frequencia_absoluta()
        frequencia_acumulada_anterior = 0
        classe_mediana = []
        

        for i in range(len(self.lista)):
            frequencia_acumulada_anterior+=self.lista[i][2]
            if(frequencia_acumulada_anterior > somatorio_frequencia_absoluta_simples/2):
                classe_mediana = self.lista[i]
                frequencia_acumulada_anterior -= classe_mediana[2]
                break
                

        return (classe_mediana[0]+((float((somatorio_frequencia_absoluta_simples/2)-frequencia_acumulada_anterior))/classe_mediana[2])*(classe_mediana[1]-classe_mediana[0]))
            

        
            
    def get_moda(self):
        classe_modal=[]
        for i in range(len(self.lista)):
            if classe_modal == []:
                classe_modal = self.lista[i]
            elif self.lista[i][2] > classe_modal[2]:
                classe_modal = self.lista[i]
        return (float(classe_modal[0]+classe_modal[1]))/2

    def get_variancia(self):

        s=0
        s2=0
        for i in self.lista:
            s2+=i[2]*((i[0]+i[1])/2)**2

        for i in self.lista:
            s+=i[2]*((i[0]+i[1])/2)
        s=float(s)
        s2=float(s2)
        return (float(s2-(float((s**2))/self.get_somatorio_frequencia_absoluta())))/float(self.get_somatorio_frequencia_absoluta()-1)

    def get_desvio_padrao(self):
        return self.get_variancia()**0.5
    
    def get_coeficiente_de_variacao(self):
        return 100*(self.get_desvio_padrao()/self.get_media())


    def get_somatorio_frequencia_absoluta(self):
        f=0
        for i in self.lista:
            f+=i[2]
        
        return f

class gerarTabela():
    lista = []

    def __init__(self, lista):
        self.lista = lista
    
    def get_tabela(self):
        frequencias_acumulada = 0
        
        for i in self.lista:
            frequencias_acumulada+=i[2]
            i.append(frequencias_acumulada)       
            

        for i in self.lista:
            i.append(i[2]/float(frequencias_acumulada))
        
        acumulador = 0
        for i in self.lista:
            acumulador+=i[4]
            i.append(acumulador)    
                
        return self.lista



analyzer = Analyzer(games)

print("#### Ferramenta para dados Estatisticos  #######")
print("######## Referente a Jogos da Steam  ###########")
print("################################################")
print("Tamanho da amostral:######## %d" % analyzer.get_size())
print("Minimo:##################### %.2f" % analyzer.get_min_price())
print("Maximo:##################### %.2f" % analyzer.get_max_price())
print("Amplitude:################## %.2f" % analyzer.get_amplitude())
print("Media:###################### %.2f" % analyzer.get_media())
print("Mediana:#################### %.2f" % analyzer.get_mediana())
print("Moda:####################### %.2f" % analyzer.get_modinha())
print("Variancia^2:################ %.2f" % analyzer.get_variancia())
print("Desvio padrao:############## %.4f" % analyzer.get_desvio_padrao())
print("Coeficiente de variacao:#### %.2f%%" % analyzer.get_coeficiente_de_variacao())
print("################################################")

classes = analyzer.get_classes()

contador = 0
divisoriasI=[]
for i in range(15):
    divisoriasI.append(contador)
    contador+=4
        
divisoriasF=[]
contador=4
for i in range(15):
    divisoriasF.append(contador)
    contador+=4

games_classes = []
for i in range(len(divisoriasI)):
    item = []
    item.append(divisoriasI[i])
    item.append(divisoriasF[i])
    item.append(len(classes[i]))
    games_classes.append(item[:])


games_classes = gerarTabela(games_classes).get_tabela()

print("   Clases   | fi     | Fi    | fri    |  Fri  | ")
for i in games_classes:  
    print("|  %d  -  %d  | %d  | %d | %.2f%%  | %.2f%% |" %(i[0],i[1],i[2],i[3],i[4]*100,i[5]*100))




analyzer2=AnalyzerG(games_classes)




print("Media:###################### %.2f" % analyzer2.get_media())
print("Mediana:#################### %.2f" % analyzer2.get_mediana())
print("Moda:####################### %.2f" % analyzer2.get_moda())
print("Variancia^2:################ %.2f" % analyzer2.get_variancia())
print("Desvio padrao:############## %.4f" % analyzer2.get_desvio_padrao())
print("Coeficiente de variacao:#### %.2f%%" % analyzer2.get_coeficiente_de_variacao())


print("\n")
print("Os resultados foram similares, onde e possivel abstrair a bservao simlar de ambos ")

precos = []

for i in games:
    precos.append(i.price)

bins = divisoriasI

plt.hist(precos, bins, histtype="bar", rwidth=0.5 )
plt.show()