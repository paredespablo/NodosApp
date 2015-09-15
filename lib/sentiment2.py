# -*- coding: utf-8 -*-
import codecs, time, re, os

def sentimientos():
    inputd = codecs.open('tmp/tmpfile.txt', 'r', 'utf-8') ## Archivo de tweets
    words = codecs.open('lib/lexico/eng-spa_lexicon.dat', 'r', 'utf-8') ## Archivo con diccionario
    palabras = words.readlines()
    lineas = inputd.readlines()

    u1 = []
    u2 = []
    for i in palabras:
        i = i.split('\t')
        word = i[0]
        sen = i[2]
        u1.append(word)
        u2.append(sen)
    words.close()

    output = codecs.open('tmp/output_sentimientos1.txt', 'w', 'utf-8') ## Archivo de salida

    pos = 0
    neg = 0
    neu = 0
    for i in lineas:
        i = i.split('","')
        texto1 = i[-1].strip()
        texto0 = texto1.lower()
        autor = i[1].strip()
        texto = re.findall(r'\w+', texto0,flags = re.UNICODE | re.LOCALE)
        val = 0
        for u in texto:
            if u in u1:
                pos = u1.index(u)
                sent = u2[pos].strip()
                if sent == 'pos':
                    val += 1
                elif sent == 'neg':
                    val -= 1
                else:
                    val += 0
        if val > 0:
            print >> output, autor,'\t',texto0,'\t',val,'\tPositivo'
            pos +=1
        elif val <0:
            print >> output, autor,'\t',texto0,'\t',val,'\tNegativo'
            neg +=1
        else:
            print >> output, autor,'\t',texto0,'\t',val,'\tNeutral'
            neu +=1

    output.close()
    os.remove('tmp/output_sentimientos1.txt')
    inputd.close()
    total = pos + neg + neu
    totalb = pos + neg
    print 'Positivo preliminar:', round(float(float(pos)/float(total)),1), pos, '(' + str(round(float(float(pos)/float(totalb)),1)) + ')'
    print 'Negativo preliminar:', round(float(float(neg)/float(total)),1), neg, '(' + str(round(float(float(neg)/float(totalb)),1)) + ')'
    print 'Neutral preliminar:', round(float(float(neu)/float(total)),2), neu
    
    print 'Fin del analisis de diccionario'

    print 'Analisis finalizado'
