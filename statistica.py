#Atividade de Estatistica

#uso de dados para fazer calculos estitisticos referente a alguma base de dados

#dados usados sao provindos da STEAMAPI , uma api que fornece dados referentes a jogos disponiveis na STEAMAPI

import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Para pegar dados online
# base_url = "http://steamspy.com/api.php?request="
# response = requests.get(base_url+"all")
# data = json.loads(response.text)

with open('api.php.json') as json_file:
    text = json_file.read()
    data = json.loads(text)

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
        
        return total/self.get_size()
    
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
        return soma_total_amostras/len(self.lista)
    
    def get_desvio_padrao(self):
        return self.get_variancia()**0.5
    
    def get_coeficiente_de_variacao(self):
        return (self.get_desvio_padrao()/self.get_media()) * 100
    
    def get_classes(self):
        self.lista.sort(key=lambda x: x.price)
        classes= [[],[],[],[],[],[],[],[],[],[]]
        divisoriasI=[0,60,120,180,240,300,360,420,480,540]
        divisoriasF=[60,120,180,240,300,360,420,480,540,600]
        contador = 0
        for i in self.lista:
            if(divisoriasI[0]<=i.price<divisoriasF[0]):
                classes[0].append(i)
            elif(divisoriasI[1]<=i.price<divisoriasF[1]):
                classes[1].append(i)
            elif(divisoriasI[2]<=i.price<divisoriasF[2]):
                classes[2].append(i)
            elif(divisoriasI[3]<=i.price<divisoriasF[3]):
                classes[3].append(i)
            elif(divisoriasI[4]<=i.price<divisoriasF[4]):
                classes[4].append(i)
            elif(divisoriasI[5]<=i.price<divisoriasF[5]):
                classes[5].append(i)
            elif(divisoriasI[6]<=i.price<divisoriasF[6]):
                classes[6].append(i)
            elif(divisoriasI[7]<=i.price<divisoriasF[7]):
                classes[7].append(i)
            elif(divisoriasI[8]<=i.price<divisoriasF[8]):
                classes[8].append(i)
            elif(divisoriasI[9]<=i.price<divisoriasF[9]):
                classes[9].append(i)


        return classes
           




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

divisoriasI=[0,60,120,180,240,300,360,420,480,540]
divisoriasF=[60,120,180,240,300,360,420,480,540,600]

classes = analyzer.get_classes()


print("   Clases   | Frequencias ")
for i in range(len(divisoriasF)):
    print("|  %d  -  %d  | %d " %(divisoriasI[i],divisoriasF[i],len(classes[i])))

games_classes = []
frequencias_acumuladas = len(games)

for i in classes[0]:
    obj = Game("",0,60/2)
    games_classes.append(obj)
for i in classes[1]:
    obj = Game("",0,180/2)
    games_classes.append(obj)
for i in classes[2]:
    obj = Game("",0,300/2)
    games_classes.append(obj)
for i in classes[3]:
    obj = Game("",0,420/2)
    games_classes.append(obj)
for i in classes[4]:
    obj = Game("",0,540/2)
    games_classes.append(obj)
for i in classes[5]:
    obj = Game("",0,660/2)
    games_classes.append(obj)
for i in classes[6]:
    obj = Game("",0,780/2)
    games_classes.append(obj)
for i in classes[7]:
    obj = Game("",0,900/2)
    games_classes.append(obj)
for i in classes[8]:
    obj = Game("",0,1020/2)
    games_classes.append(obj)
for i in classes[9]:
    obj = Game("",0,1140/2)
    games_classes.append(obj)

analyzer2=Analyzer(games_classes)




print("Media:###################### %.2f" % analyzer2.get_media())
print("Mediana:#################### %.2f" % analyzer2.get_mediana())
print("Moda:####################### %.2f" % analyzer2.get_modinha())
print("Variancia^2:################ %.2f" % analyzer2.get_variancia())
print("Desvio padrao:############## %.4f" % analyzer2.get_desvio_padrao())
print("Coeficiente de variacao:#### %.2f%%" % analyzer2.get_coeficiente_de_variacao())


print("\n")
print("Pela comparacao da media e da mediana, no caso a minha ")
print("selecao de dados teve uma grande mudanca, mas isso ocorreu")
print("devido a alta concentracao na clases")
print("mas percebes que pela divisao das clases, ambas permaneceram na mesma area")

precos = []

for i in games:
    precos.append(i.price)

bins = [60,120,180,240,300,360,420,480,540,600]

plt.hist(precos, bins, histtype="bar", rwidth=0.5, label=[0,1,2,3,4,5] )
plt.show()