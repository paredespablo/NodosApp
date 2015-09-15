# -*- coding: UTF-8 -*-
import tweepy, codecs, time, sys, tkFileDialog
from textwrap import TextWrapper
from keys import *
reload(sys)  
sys.setdefaultencoding('utf8')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def streaming_geo():
    trackwords = []

    file_path = tkFileDialog.askopenfilename(title="Abrir archivo de keywords", filetypes=[("txt file",".txt"),("All files",".*")])
    if file_path != "":
        pass
    else:
        print 'Debes seleccionar un archivo'
        return False

    input_data = codecs.open(file_path, 'r', 'utf-8')

    input2 = input_data.readlines()
    for i in input2:
        i = str(i.strip())
        i = i.lower()
        trackwords.append(i)

    infocoord = file('tmp/geo.clr', 'r')
    coord = infocoord.read()
    coord = eval(coord.strip())
    infocoord.close()

    file_save = tkFileDialog.asksaveasfilename(title="Nombre de archivo a guardar", filetypes=[("txt file",".txt"),("All files",".*")])
    if file_save != "":
        pass
    else:
        print 'Debes seleccionar un archivo'
        return False

    class CustomStreamListener(tweepy.StreamListener):
        def on_status(self, status):
            try:
                output = codecs.open(file_save, 'a', encoding='utf-8')
                mensaje = ("%s" % (status.id))
                texto0 = ("%s" % (status.text))
                texto1 = texto0.splitlines()
                mensaje_texto = " ".join(texto1)
                screen_name = ("%s" % (status.author.screen_name))
                user_id = ("%s" % (status.author.id))
                name = ("%s" % (status.author.name))
                followers_count = ("%s" % (status.author.followers_count))
                friends_count = ("%s" % (status.author.friends_count))
                statuses_count = ("%s" % (status.author.statuses_count))
                
                location0 = ("%s" % (status.author.location))
                location1 = location0.splitlines()
                location = " ".join(location1)
                
                created_at = ("%s" % (status.created_at))
                source = ("%s" % (status.source))
                idioma = ("%s" % (status.author.lang))
                autorreg = ("%s" % (status.author.created_at))

                try:
                    geo = ("%s" % (status.geo['coordinates']))
                except:
                    geo = '[0]'

                txt = mensaje_texto.split()
                for x in txt:
                    x = x.lower()
                    if x in trackwords:
                        print geo, location, mensaje_texto
                        print >> output, '"'+str(mensaje)+'","'+screen_name+'","'+name+'","'+str(user_id)+'","'+str(autorreg)+'","'+str(followers_count)+'","'+str(friends_count)+'","'+str(statuses_count)+'","'+location+'","'+str(created_at)+'","'+str(geo)+'","'+source+'","'+idioma+'","'+mensaje_texto+'"'
                        output.close()
                        break
                    else:
                        pass
                else:
                    pass

            except Exception, e:
                print 'Error encontrado:', str(e)
                pass
            except KeyboardInterrupt:
                print 'Scanning stopped'
                return False

    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=90)
    print 'Iniciando descarga de datos en tiempo real'
    print ''

    def stream():
        try:
            streaming_api.filter(locations=coord)
        except Exception,e:
            print str(e)
            print 'Error, reconectando...'
            time.sleep(5)
            stream()

    stream()

    a = raw_input('Presiona ENTER para salir')
    

