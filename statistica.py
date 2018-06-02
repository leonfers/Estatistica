#Atividade de Estatistica

#uso de dados para fazer calculos estitisticos referente a alguma base de dados

#dados usados sao provindos da STEAMAPI , uma api que fornece dados referentes a jogos disponiveis na STEAMAPI

import requests
import json

# Para pegar dados online
# base_url = "http://steamspy.com/api.php?request="
# response = requests.get(base_url+"all")
# data = json.loads(response.text)

with open('api.php.json', encoding='utf-8') as json_file:
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
            if(i.price==9.99):
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

analyzer = Analyzer(games)

print("#### Ferramenta para dados Estatisticos  #######")
print("######## Referente a Jogos da Steam  ###########")

print("jogos gratis: %d" % analyzer.get_free())
print("Quantidade de faixa de precos: %d "% len(analyzer.get_matrix()))

print("Tamanho da amostral: %d" % analyzer.get_size())
print("Minimo: %.2f" % analyzer.get_min_price())
print("Maximo:%.2f" % analyzer.get_max_price())
print("Amplitude: %.2f" % analyzer.get_amplitude())
print("Media: %.2f" % analyzer.get_media())
print("Mediana : %.2f" % analyzer.get_mediana())
print("Moda: %.2f" % analyzer.get_modinha())
print("Variancia^2: %.2f" % analyzer.get_variancia())
print("Desvio padrao: %.4f" % analyzer.get_desvio_padrao())
print("Coeficiente de variacao: %.2f%%" % analyzer.get_coeficiente_de_variacao())


