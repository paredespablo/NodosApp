import codecs

nombres2 = codecs.open('lib/nombre.nod', 'r', 'utf-8')
nombres = nombres2.readlines()

girls = []
boys = []

for i in nombres:
    i = i.split('\t')
    sex = i[0]
    comuna = i[1]
    nombre = i[2].title()
    if sex == 0:
        girls.append(nombre)
    else:
        boys.append(nombre)


    
    


