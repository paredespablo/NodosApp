# -*- coding: cp1252 -*-
#import matplotlib
import networkx as nx
import urllib2
import codecs
import requests
import matplotlib.pyplot as plt
from BeautifulSoup import *

key='b84f713816cbd9f70ad5d069242a2c5d'

## Codigo para buscar datos a traves de palabras claves##

print ""
print "#######################################"
print "          API de Poderopedia           "
print "          Redes de intereses           "
print "#######################################"
print ""
search = raw_input("Ingresa nombre a buscar: ")
tipo = raw_input("Ingresa tipo de entidad ('persona' u 'organizacion'): ")
payload = {'entity': tipo, 'alias': search, 'user_key':key}
r = requests.get('http://api.poderopedia.org/visualizacion/search', params=payload)
data = r.json()

G=nx.Graph()
try:
    if tipo == 'organizacion':
        t = 'organization'
    else:
        t = 'person'
    for alias in data[t]:
        nom1 = alias['alias']
        id1 = alias['id']
        en1 = tipo
        G.add_node(nom1)

        # Aqui comienza a sacar datos de cada entidad encontrada en el punto anterior
        payload2 = {'entity': tipo, 'id': alias['id'], 'user_key':key}
        k = requests.get('http://api.poderopedia.org/visualizacion/connection', params=payload2)
        data2 = k.json()
        data3 = data2['nodes']
        for person in data3:
            nom2 = person['name']
            id2 = person['id']
            en2 = person['group']
            G.add_node(nom2)
            G.add_edge(nom1, nom2, weight=1)
            print nom1, id1, en1, nom2, id2, en2

    pr = nx.pagerank(G, alpha=0.9)
    d = nx.degree(G)
    pos=nx.spring_layout(G)

    gexf = raw_input("Red construida. Exportar a gexf?(s/n): ")
    if gexf == "s":
        nam = str(str(search) + ".gexf")
        nx.write_gexf(G, nam, encoding='utf-8', prettyprint=True, version='1.1draft')
        print ""
        print "Archivo", nam, "exportado con exito."
    else:
        pass    

    nx.draw(G, nodelist=d.keys(), node_size=[v * 50 for v in d.values()], node_color='r', with_labels=True, font_size=12)
    plt.show()

except Exception,e:
    print str(e)
