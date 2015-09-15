# -*- coding: utf-8 -*-
##Importacion de librerias
import Tkinter, tkMessageBox, tkFileDialog, tkColorChooser, tweepy, codecs, requests, time, sys, os, subprocess, shutil, re, webbrowser, imp, networkx as nx
from Tkinter import *
keys = imp.load_source('keys', 'lib/keys.py')
pyfollowers = imp.load_source('pyfollowers', 'lib/pyfollowers.py')
pygooglevis = imp.load_source('pygooglevis', 'lib/pygooglevis.py')
sentiment2 = imp.load_source('sentiment2', 'lib/sentiment2.py')
streamingfilter = imp.load_source('streamingfilter', 'lib/streamingfilter.py')
streaminggeo = imp.load_source('streaminggeo', 'lib/streaminggeo.py')
d3 = imp.load_source('d3', 'lib/d3_script.py')
from d3 import *
from streamingfilter import *
from streaminggeo import *
from pyfollowers import *
from pygooglevis import *
from keys import *
from sentiment2 import *

##Autenticacion con Tweepy y listas globales

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

root =Tk()

sinceid = None
tweets = []
maxids = []

##Funcion de apertura de datos en formato de texto plano
def abrirdatos():
    global fpname
    global hashtag2
    global file_path
    file_path = tkFileDialog.askopenfilename(title="Open file", filetypes=[("txt file",".txt")])
    if file_path != "":
        hashtag2 = file_path
        editmenu.entryconfig(0,state=NORMAL) ## Crear gexf
        editmenu.entryconfig(3,state=NORMAL) ## Hashtags mas mencionados
        editmenu.entryconfig(4,state=NORMAL) ## Usuarios mas mencionados
        editmenu.entryconfig(5,state=NORMAL) ## Emisores de tweets
        editmenu.entryconfig(6,state=NORMAL) ## Sentiment analysis
        editmenu.entryconfig(7,state=NORMAL) ## Gender analysis
        editmenu.entryconfig(11,state=NORMAL) ## Google Maps
    else:
        print 'You have to choose a file'
        return False
    tmpdir = 'tmp/'
    shutil.copyfile(file_path, tmpdir + 'tmpfile.txt')
    data = codecs.open(hashtag2, 'r', 'utf-8')
    archivo = data.readlines()[1:]
    fp = hashtag2.split('/')
    fpname = fp[-1]

    fname = file('tmp/enam.nme', 'w')
    print >> fname, fpname[0:-4]
    fname.close()

    print 'Loaded file:', fpname
    return False

##Funcion de apertura de redes estaticas en formato GEXF
def abrirred():
    global G
    global fpname
    global file_path
    file_path = tkFileDialog.askopenfilename(title="Open file", filetypes=[("GEXF files",".gexf")])
    if file_path != "":
        G = nx.read_gexf(file_path, relabel=False)
        fp = file_path.split('/')
        fpname = fp[-1]
        print 'Loaded network:', fpname
        
        editmenu.entryconfig(1,state=NORMAL) ## Estadisticas
        editmenu.entryconfig(9,state=NORMAL) ## Sigma-JS
        editmenu.entryconfig(10,state=NORMAL) ## D3 HTML Graph
    else:
        print 'You have to choose a file'
        return False

    tmpdir = 'tmp/'
    shutil.copyfile(file_path, tmpdir + 'tmpfile.gexf')
    fp = file_path.split('/')
    fpname = fp[-1]
    fname = file('tmp/enamgexf.nme', 'w')
    print >> fname, fpname[0:-4]
    fname.close()
    
    return False

##Funcion de creacion de estadisticas de redes
def estgexf():
    global fpname
    indegree_list = []
    outdegree_list = []
    closeness_list = []
    betweenness_list = []
    users_list = []
    clustering_list = []
    file_path = fpname
    output_est = file(file_path + '_stats.txt', 'w')
    print >> output_est, 'node\tindegree\toutdegree\tcloseness\tbetweenness\tclustering\tcomponents\tdiameter'
    indegree = nx.in_degree_centrality(G)
    outdegree = nx.out_degree_centrality(G)
    closeness = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    ndG = G.to_undirected()
    clustering = nx.clustering(ndG)
    try:
        diameter = nx.diameter(G)
    except:
        diameter = 1000
    for key, value in clustering.items():
        clustering_list.append(value)
    clusv = sum(clustering_list)/float(len(clustering_list))
    for key, value in indegree.items():
        indegree_list.append(value)
    indv = sum(indegree_list)/float(len(indegree_list))
    for key, value in outdegree.items():
        outdegree_list.append(value)
    outv = sum(outdegree_list)/float(len(outdegree_list))
    for key, value in closeness.items():
        closeness_list.append(value)
    closev = sum(closeness_list)/float(len(closeness_list))
    for key, value in betweenness.items():
        betweenness_list.append(value)
        users_list.append(key)
    betv = sum(betweenness_list)/float(len(betweenness_list))
    components_count = len(users_list)
    for i in users_list:
        pos = users_list.index(i)
        print >> output_est, i,'\t',indegree_list[pos],'\t',outdegree_list[pos],'\t',closeness_list[pos],'\t',betweenness_list[pos],'\t',clustering_list[pos],'\t',components_count,'\t',diameter

    output_est.close()
    ascoef = nx.degree_assortativity_coefficient(G)
    estr = nx.estrada_index(ndG)

    print 'Network indicators for', fpname
    print ''
    print '---------------------------------------'
    if diameter == 1000:
        print 'Diameter: disconnected network'
    else:
        print 'Diameter:', diameter
    print 'Average clustering:', clusv
    print 'Average Indegree centrality:', indv
    print 'Average Outdegree centrality:', outv
    print 'Average Closeness centrality:', closev
    print 'Average Betweenness centrality:', betv
    print 'Components count:', components_count
    print 'Assortativity coefficient:', ascoef
    print 'Estrada index', estr
    print '---------------------------------------'
    print ''
    return False

##Calculo de API Calls restantes 
def apicalls():
    data2 = api.rate_limit_status()
    data = data2['resources']['followers']['/followers/ids']
    print data
    reset_time = data['reset']
    remaining_hits = data['remaining']
    hourly_limit = data['limit']

    gmt_hora = time.strftime("%H", time.gmtime())
    gmt_min = time.strftime("%M", time.gmtime())
    gmt_sec = time.strftime("%S", time.gmtime())
    hora_gmt = (int(gmt_hora)*3600) + (int(gmt_min)*60) + int(gmt_sec)

    count = time.strftime('%H:%M:%S', time.gmtime(reset_time))
    tiempo = count.split(':')
    restante = (int(tiempo[0])*3600 + int(tiempo[1])*60 + int(tiempo[2]))
    tiempo_sec = restante - hora_gmt
    tiempo_min = int(float(tiempo_sec)/float(60))

    datos = 'Next reset (GMT)',count,'\nRemaining API calls',remaining_hits,'\nLlamadas por hora', hourly_limit,'\nMinutos para proximo reset', tiempo_min
    tkMessageBox.showinfo('Remaining API calls: ', datos)
    return False

##Funcion para creacion de redes GEXF en base a datos abiertos
def gexf():
    global G
    global hashtag2

    G=nx.DiGraph()
    data = codecs.open(hashtag2, 'r', 'utf-8')
    archivo = data.readlines()[1:]
    print 'Construyendo red'
    for i in archivo:
        try:
            campos = i.split('","')
            autor2 = campos[1].lower()
            autor = autor2.strip()
            atr_user = {}

            atr_user["user_name"] = campos[2].strip()
            atr_user["user_id"] = campos[3].strip()
            atr_user["register_time"] = campos[4].strip()
            atr_user["user_followers"] = campos[5].strip()
            atr_user["user_following"] = campos[6].strip()
            atr_user["user_statuses"] = campos[7].strip()
            atr_user["user_location"] = campos[8].strip()

            atr_tweet = {}
            atr_tweet["tweet_id"] = campos[0].strip()
            atr_tweet["tweet_timestamp"] = campos[9].strip()
            atr_tweet["tweet_source"] = campos[11].strip()
            atr_tweet["tweet_lang"] = campos[12].strip()
            atr_tweet["tweet_msg"] = campos[13].strip()
            
            G.add_node(autor, attr_dict=atr_user)
            mensaje = campos[-1]
            mensaje = mensaje.lower()
            words = re.findall(r'@\w+', mensaje,flags = re.UNICODE | re.LOCALE)
            for o in words:
                user = re.findall(r'\w+', o,flags = re.UNICODE | re.LOCALE)
                k = user[0].lower()
                G.add_edge(autor,k, attr_dict=atr_tweet)
        except Exception, e:
            print str(e)

    name = hashtag2[0:-4]
    nx.write_gexf(G, name + ".gexf", encoding='utf-8', prettyprint=True)
    data.close()
    print 'GEXF file finished'
    return False

##Grafico basico a partir de redes abiertas
def plot_sigmajs():
    try:
        nvodir = fpname[0:-5] + '_sigmajs/'
        shutil.copytree('visual/sigma-js/', nvodir)
        shutil.copyfile(file_path, nvodir + '/data/graph_signod.gexf')
        print 'Sigma.js network has been created'
        #webbrowser.open(nvodir + 'index.htm',new=2)
    except Exception, e:
        print str(e)
    return False

# Plot sobre Google Maps
def pygmap():
    global hashtag2
    
    data = {
        'API_KEY': 'AIzaSyDuM0jdi4F3Toxu3so44y_01dCjYjwVnKE',
        'SENSOR': 'false',
        'COORD': '0, 0'
    }
    nombre = hashtag2[0:-4] + '_Maps.html'
    ## Primera parte del codigo HTML ##
    outputmap = codecs.open(nombre, 'w', encoding='utf-8')

    template = '''
        <!DOCTYPE html>
        <html>
          <head>
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
            <style type="text/css">
              html { height: 100%% }
              body { height: 100%%; margin: 0; padding: 0 }
              #map_canvas { height: 100%% }
            </style>
            <script type="text/javascript"
              src="http://maps.googleapis.com/maps/api/js?key=%(API_KEY)s&sensor=%(SENSOR)s">
            </script>
            <script type="text/javascript">
              function initialize() {
                var myOptions = {
                  center: new google.maps.LatLng(%(COORD)s),
                  zoom: 2,
                  mapTypeId: google.maps.MapTypeId.ROADMAP
                };
                var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
                var infowindow = new google.maps.InfoWindow();'''
    print >> outputmap, template % data

    # Identificacion y marca de coordenadas
    lats = []
    lngs = []
    populations = [] #millions
    data = codecs.open(hashtag2, 'r', encoding='utf-8')

    data2 = data.readlines()[1:]
    filterg = ['[0]', 'geo']
    try:
        for i in data2:
            lineas = i.split('","')
            if lineas[10] in filterg:
                pass
            else:
                try:
                    coord = eval(lineas[10])
                    texto0 = lineas[-1].strip()
                    autor0 = lineas[1].strip()
                    autor = re.sub('''["']''', '', autor0)
                    texto = re.sub('''["']''', '', texto0)
                    tweets = {'autor': autor, 'text': texto, 'lat': coord[0], 'lon': coord[1] }
                    if float(tweets['lat']) and float(tweets['lon']):
                        pt1 = '''               var marker = new google.maps.Marker({ position: new google.maps.LatLng('''+ str(tweets['lat']) +''', '''+ str(tweets['lon']) +'''), map: map,});'''
                        pt2 = '''                 google.maps.event.addListener(marker, 'click', function() {'''
                        pt3 = '''                  infowindow.setContent("''' + autor +': '+ texto + '''");'''
                        pt4 = '''                  infowindow.open(map, this);});'''
                        print >> outputmap, pt1
                        print >> outputmap, pt2
                        print >> outputmap, pt3
                        print >> outputmap, pt4
                        
                        #tweet2 = tweet.encode('utf-8')
                        #print >> outputmap, tweet2 % tweets
                    else:
                        print 'There is an error in the file'
                        continue
                except Exception, e:
                    print str(e)
                    continue
    except Exception, e:
        print str(e)


    ## Parte final del codigo HTML
    template = '''
          }
        </script>
      </head>
    <title>NodosApp: Geo-tweets</title>
    <body onload="initialize()">
        <div id="map_canvas" style="width:100%%; height:100%%"></div>
      </body>
     </html>'''
    print >> outputmap, template

    ## Cierre de archivo
    print 'File', nombre, 'created succesfully'
    outputmap.close()
    data.close()
    return False


##Funcion de descarga de hashtags a partir de parametros señalados

def scan():
    global fecha_inicial1, fecha_final1, id_inicial1, id_final1, geo1, lang1, hashtag1
    fecha_inicial2 = fecha_inicial1.get()
    fecha_final2 = fecha_final1.get()
    id_inicial2 = id_inicial1.get()
    id_final3 = id_final1.get()
    geo2 = geo1.get()
    lang2 = lang1.get()
    hashtag2 = hashtag1.get()
    
    if not fecha_inicial2:
        fecha_inicial2 = None
    if not fecha_final2:
        fecha_final2 = None
    if not id_inicial2:
        id_inicial2 = None
    if not id_final3:    ## mod
        id_final3 = None ## mod
    if not geo2:
        geo2 = None
    if not lang2:
        lang2 = None
    if not hashtag2:
        tkMessageBox.showinfo('Hashtag', 'You have to specify a hashtag or keyword')
        return False

    archivo = codecs.open(hashtag2 + '.txt', 'a', encoding='utf-8')
    print 'Scanning Twitter Search API.'
    print 'You can stop the process pressing Ctrl+C, but errors may arise in the results'
    print ''
    print >> archivo, '"mensaje_id","screen_name","name","id_name","register_time","followers","following","statuses","location","timestamp","geo","source","idioma","tweet"'
    
    def scan2():
            
        if (not tweets) and (id_final3 == None):
            id_final2 = None
            
        elif (not tweets) and (id_final3 != None):
            id_final2 = id_final3
        else:
            id_final2 = str(int((tweets[-1]) - 1))

            
        print 'Last id:', id_final2
        time.sleep(5)

        for page in range(1,16):
            if id_final2 in maxids:
                return False
            else:
                maxids.append(id_final2)
            try:
                datos = api.search(hashtag2, count=100, geocode=geo2, lang=lang2, since=fecha_inicial2, until=fecha_final2, since_id=id_inicial2, max_id=id_final2)
                for SearchResult in datos:
                    screen_name = SearchResult.user.screen_name
                    user_id = SearchResult.user.id
                    name = SearchResult.user.name
                    followers_count = SearchResult.user.followers_count
                    friends_count = SearchResult.user.friends_count
                    statuses_count = SearchResult.user.statuses_count
                    created_at = SearchResult.created_at
                    idioma = SearchResult.lang
                    autorreg = SearchResult.user.created_at
                    
                    location0 = SearchResult.user.location
                    location1 = location0.splitlines()
                    location2 = " ".join(location1)
                    location = re.sub("[,]", '', location2)
                    
                    mensaje_id = SearchResult.id
                    try:
                        geo_d = SearchResult.geo['coordinates']
                    except:
                        geo_d = '[0]'
                    source = SearchResult.source
                    texto0 = SearchResult.text
                    texto1 = texto0.splitlines()
                    mensaje_texto1 = " ".join(texto1)
                    mensaje_texto = re.sub("[,]", '', mensaje_texto1)
                    del tweets[:]
                    tweets.append(SearchResult.id)
                    print >> archivo, '"'+str(mensaje_id)+'","'+screen_name+'","'+name+'","'+str(user_id)+'","'+str(autorreg)+'","'+str(followers_count)+'","'+str(friends_count)+'","'+str(statuses_count)+'","'+location+'","'+str(created_at)+'","'+str(geo_d)+'","'+source+'","'+idioma+'","'+mensaje_texto+'"'
                    total = int(len(tweets))
                    
                scan2()
                
            except Exception, e:
                print str(e)
                time.sleep(5)
                scan2()
            except KeyboardInterrupt:
                print 'Scanning stopped'
                break

    scan2()
    del tweets[:]
    del maxids[:]
    archivo.close()

    tkMessageBox.showinfo('Done!', 'File succesfully created')


    archivo.close()
    return False

## Ranking de Hashtags, tweeters y usuarios mencionados

## Funcion que cuenta la cantidad de veces que es mencionado un hashtag (#) en una conversacion
def rank_hashtags():
    temp_hs = codecs.open('input_hashtag.txt', 'w', 'utf-8')
    hashtags = []
    hashvalores = []
    tuples = []
    global hashtag2
    data = codecs.open(hashtag2, 'r', 'utf-8')
    data2 = data.readlines()[1:]
    for i in data2:
        try:
            lineas = i.split('","')
            tweet = lineas[-1]
            tweet = tweet.lower()

            palabras = []
            for t in tweet.split():
                if t.startswith('#'):
                    t = t.replace("'", "")
                    t = t.replace('"', "")
                    palabras.append(t)
                else:
                    pass
            for o in palabras:
                if o not in hashtags:
                    hashtags.append(o)
                    hashvalores.append(1)
                else:
                    pos = hashtags.index(o)
                    val = hashvalores[pos]
                    hashvalores[pos] = val + 1
        except Exception, e:
            print str(e)
        
        
    for i in hashtags:
        ps = hashtags.index(i)
        count = hashvalores[ps]
        tuples.append( ( count, i ) )

    tuples.sort(reverse=True)
    print 'Mentions\tHashtag'

    for o in tuples:
        if tuples.index(o) < 16:
            numb = o[0]
            hasht = o[1]

            hasht2 = hasht.decode('utf-8-sig')
            hasht2 = hasht2.encode('utf-8')
            
            print >> temp_hs, numb, hasht
            print numb,'\t',hasht2

    temp_hs.close()
    pygooglevis_hs()
    os.remove('input_hashtag.txt')

    print 'Ranking of hashtags created successfully'
    
    return False

## Funcion que cuenta la cantidad de veces que es mencionado un usuario (@) en una conversacion
def rank_users():
    temp_hs = codecs.open('input_usuarios.txt', 'w', 'utf-8')
    usuarios = []
    usrvalores = []
    tuples = []
    global hashtag2
    data = codecs.open(hashtag2, 'r', 'utf-8')
    data2 = data.readlines()[1:]
    for i in data2:
        try:
            lineas = i.split('","')
            tweet = lineas[-1]
            tweet = tweet.lower()
            palabras = re.findall(r'@\w+', tweet,flags = re.UNICODE | re.LOCALE)
            for o in palabras:
                if o not in usuarios:
                    usuarios.append(o)
                    usrvalores.append(1)
                else:
                    pos = usuarios.index(o)
                    val = usrvalores[pos]
                    usrvalores[pos] = val + 1
        except Exception, e:
            print str(e)
                
    for i in usuarios:
        ps = usuarios.index(i)
        count = usrvalores[ps]
        i = i.replace("@", "")
        tuples.append( ( count, unicode(i) ) )

    tuples.sort(reverse=True)
    print 'Mentions\tUsername'

    for o in tuples:
        if tuples.index(o) < 15:
            
            print >> temp_hs, o[0], o[1]
            print o[0],'\t',o[1]

    temp_hs.close()
    pygooglevis_usr()
    os.remove('input_usuarios.txt')

    print 'Ranking of users created successfully'
    
    return False

## Rankea a los mayores tweeters de una serie de datos
def rank_tweeters():
    temp_hs = codecs.open('input_tweeters.txt', 'w', 'utf-8')
    global hashtag2
    usuarios = []
    tuples = []
    usrvalores = []
    data = codecs.open(hashtag2, 'r', 'utf-8')
    data2 = data.readlines()[1:]
    for i in data2:
        try:
            i = i.split('","')
            j = i[1].strip()
            if j not in usuarios:
                usuarios.append(j)
                usrvalores.append(1)
            else:
                pos = usuarios.index(j)
                val = usrvalores[pos]
                usrvalores[pos] = val + 1
        except Exception, e:
            print str(e)

    for i in usuarios:
        ps = usuarios.index(i)
        count = usrvalores[ps]
        tuples.append( ( count, unicode(i) ) )

    tuples.sort(reverse=True)
    print 'Mentions\tUsername'

    for o in tuples:
        if tuples.index(o) < 15:
            
            print >> temp_hs, o[0], o[1]
            print o[0],'\t',o[1]

    temp_hs.close()
    pygooglevis_twe()
    os.remove('input_tweeters.txt')
    print 'Ranking of tweeters created successfully'
    
    return False            

## Cambiar color

def selectcolor():
    askcolor = tkColorChooser.askcolor(color=None)
    if askcolor == (None, None):
        askcolor = "((158, 158, 158), '#9e9e9e')"
        
    tmpcolor = file('tmp/color.clr', 'w')
    print >> tmpcolor, askcolor
    tmpcolor.close()
    return False

def selectgeo():
    def geoalg():
        geo002 = geo1.get()

        if geo002 == '':
            geo002 = '[-75.68, -55.97, -66.38, -17.49]'
            print 'No se han introducido coordenadas válidas'
            print 'Por defecto se han conservado las coordenadas de Chile'
        else:
            geo002 = '[' + geo002 + ']'
            print 'Coordenadas de georeferenciacion guardadas'
            
        tmpgeo = file('tmp/geo.clr', 'w')
        print >> tmpgeo, geo002
        tmpgeo.close()
        root5.destroy()

    def geogoogle():
        name = ''
        pais = geo4.get()
        url = 'http://maps.google.com/maps/api/geocode/json?address='
        try:
            pag = (url + pais)
            k = requests.get(pag)
            data2 = k.json()
            results = data2['results']
            
            coor1 = results[0]['geometry']['viewport']['northeast']['lat']
            coor2 = results[0]['geometry']['viewport']['northeast']['lng']
            coor3 = results[0]['geometry']['viewport']['southwest']['lat']
            coor4 = results[0]['geometry']['viewport']['southwest']['lng']
            name = results[0]['address_components'][0]['long_name']
            coords = str(coor4) +', '+ str(coor3) +', '+ str(coor2) +', '+ str(coor1)
            geo1.set(coords)
            print 'Resultado encontrado:', name, coords
        except Exception, e:
            print str(e)
            
        

    root5 = Tk()
    f = Frame(root5, width=200, height=160)
    f.pack(fill=X, expand=True)
    root5.title('NodosApp: Area de Georeferenciacion')
    global geo4
    global geo1
    
    l2 = Label(f, text="Insert the name of the country or region to find in Google")
    l2.pack()
    geo4 = StringVar(f)
    geo3 = Entry(f, textvariable=geo4, width=50).pack(side= TOP,padx=10,pady=12)
    
    l = Label(f, text="If you already know your coordinates, type them here:\n\nExample for Chile:\n-75.68,-55.97,-66.38,-17.49")
    l.pack()
    geo1 = StringVar(f)
    geo0 = Entry(f, textvariable=geo1, width=50).pack(side= TOP,padx=10,pady=12)
    
    but1 = Button(f, text='Save settings', command=geoalg, width=25)
    but2 = Button(f, text='Find in Google', command=geogoogle, width=25)
    but1.pack(side=LEFT)
    but2.pack(side=RIGHT)
    root5.resizable(width=FALSE, height=FALSE)
    root5.mainloop()

# Analisis de genero de los usuarios
def gender():
    global hashtag2
    nombres2 = codecs.open('lib/nombres.dat', 'r', 'utf-8')
    nombres = nombres2.readlines()[1:]

    girls = []
    boys = []

    for i in nombres:
        i = i.split('\t')            
        sex = i[0]
        comuna = i[1]
        nombre = i[2].strip()
        nombre = nombre.title()
        if sex == '0':
            girls.append(nombre)
        elif sex == '1':
            boys.append(nombre)
        else:
            pass
    nombres2.close()

    data2 = codecs.open(hashtag2, 'r', 'utf-8')
    data = data2.readlines()
    hombres = 0
    mujeres = 0
    raro = 0
    try:
        for i in data:
            i = i.split('","')
            
            nombre3 = i[2].split(' ')
            nombre2 = nombre3[0]
            nombre1 = nombre2.strip()
            nombre = nombre1.title()
            
            if nombre in boys:
                hombres +=1
            elif nombre in girls:
                mujeres +=1
            else:
                raro +=1
    except Exception, e:
        print str(e)

            
    total = hombres + mujeres + raro
    print 'Hombres:', hombres
    print 'Mujeres:', mujeres
    print 'Indefinido:', raro
    print 'Total:', total
    data2.close()

## Desactiva menus y cierra variable de datos
def cerrartodo():
    global hashtag2
    try:
        if hashtag2:
            del hashtag2
            os.remove('tmp/tmpfile.txt')
            os.remove('tmp/enam.nme')
        editmenu.entryconfig(0,state='disabled') ## crear gexf 
        editmenu.entryconfig(1,state='disabled') ## estadisticas
        editmenu.entryconfig(3,state='disabled') ## Hashtags mas mencionados
        editmenu.entryconfig(4,state='disabled') ## Usuarios mas mencionados
        editmenu.entryconfig(5,state='disabled') ## Emisores de tweets
        editmenu.entryconfig(6,state='disabled') ## sentiment analysis
        editmenu.entryconfig(7,state='disabled') ## gender analysis
        editmenu.entryconfig(9,state='disabled') ## sigmajs
        editmenu.entryconfig(10,state='disabled') ## d3js
        editmenu.entryconfig(11,state='disabled') ## googleearth
        print 'Se han cerrado todos los datos'
    except:
        print 'There are no open data'
    return False
    
##Cerrar programs
def salir():
    cerrartodo()
    print 'All variables closed'
    root.destroy()
    for uniquevar in [var for var in globals().copy() if var[0] != "_" and var != 'clearall']:
        del globals()[uniquevar]
    return False

##Abrir sitio web oficial    
def abweb():
    new = 2
    url = "http://www.nodoschile.org"
    webbrowser.open(url,new=new)
    return False

## Acera del programa
def abacerca():
    tkMessageBox.showinfo('About NodosApp', 'NodosApp v0.9 - Sep 15 2015\nNodosChile Ltda. 2012-2015\n\nNodosApp is distributed under a BSD license\n\nThis app is written in Python 2.7 and TK, and makes use of the following external libraries\n\n-NetworkX 1.10\n-Tweepy 3.4\n-Sigma.js 0.1\n-D3.js')

##Ventana inicial
hashtag1 = StringVar()
fecha_inicial1 = StringVar()
fecha_final1 = StringVar()
id_inicial1 = StringVar()
id_final1 = StringVar()
geo1 = StringVar()
lang1 = StringVar()
var = IntVar()

root.title('NodosApp: Social Network Analysis')

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open data', command=abrirdatos, underline=0)
submenu = Menu(filemenu, tearoff=0)

filemenu.add_command(label="Open network", command=abrirred)
filemenu.add_separator()
filemenu.add_command(label="Close all", command=cerrartodo)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=salir)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Create GEXF file", state='disabled', command=gexf)
editmenu.add_command(label="Statistics", state='disabled', command=estgexf)
editmenu.add_separator()
editmenu.add_command(label="Ranking Hashtags", state='disabled', command=rank_hashtags)
editmenu.add_command(label="Ranking Users", state='disabled', command=rank_users)
editmenu.add_command(label="Ranking Tweeters", state='disabled', command=rank_tweeters)
editmenu.add_command(label="Sentiment Analysis", state='disabled', command=sentimientos)
editmenu.add_command(label="Gender Analysis", state='disabled', command=gender)
editmenu.add_separator()
editmenu.add_command(label="Sigma.js Network", state='disabled', command=plot_sigmajs)
editmenu.add_command(label="D3.js Network", state='disabled', command=d3)
editmenu.add_command(label="Google Map", state='disabled', command=pygmap)
editmenu.add_separator()
editmenu.add_command(label="API Calls check", command=apicalls)
menubar.add_cascade(label="Network analysis", menu=editmenu)

redmenu = Menu(menubar, tearoff=0)
redmenu.add_command(label="Twitter Timeline", command=menciones)
redmenu.add_command(label="Streaming Filter API", command=streaming_filter)
redmenu.add_command(label="Streaming Geo API", command=streaming_geo)
redmenu.add_separator()
redmenu.add_command(label="Result's colour", command=selectcolor)
redmenu.add_command(label="Georeferencing area", command=selectgeo)
menubar.add_cascade(label="Tools", menu=redmenu)

abmenu = Menu(menubar, tearoff=0)
abmenu.add_command(label="Official website", command=abweb)
abmenu.add_separator()
abmenu.add_command(label="About", command=abacerca)
menubar.add_cascade(label="Help", menu=abmenu)

Label(text='Complete the next fields to start scanning').pack(pady=15)
Label(text='Hashtag or keyword').pack(side=TOP)
hashtag0 = Entry(textvariable=hashtag1, width=50).pack(side= TOP,padx=10,pady=12)
Label(text='Start date(YYYY-MM-DD)').pack(side=TOP)
fecha_inicial0 = Entry(textvariable=fecha_inicial1, width=50).pack(side= TOP,padx=20,pady=12)
Label(text='Final date (YYYY-MM-DD)').pack(side=TOP)
fecha_final0 = Entry(textvariable=fecha_final1, width=50).pack(side= TOP,padx=20,pady=12)
Label(text='Start Id (more recent than)').pack(side=TOP)
id_inicial0 = Entry(textvariable=id_inicial1, width=50).pack(side= TOP,padx=10,pady=12)
Label(text='Final Id (older than)').pack(side=TOP)
id_final0 = Entry(textvariable=id_final1, width=50).pack(side= TOP,padx=10,pady=12)
Label(text='Language (ISO 639-1: en, es, de, fr, etc.)').pack(side=TOP)
idioma0 = Entry(textvariable=lang1, width=50).pack(side= TOP,padx=10,pady=12)
Label(text='Geo (lat, long, rad; rad en mi o km)').pack(side=TOP)
geo0 = Entry(textvariable=geo1, width=50).pack(side= TOP,padx=10,pady=12)

Button( text='Find results', command=scan, width=50) .pack(side=LEFT, padx=10,pady=10)


print ''
print '        __     __  ___    ___  __  __ '
print '  /| / / / /\ / / /__    ___/ /_/ /_/ '
print ' / |/ /_/ /_//_/ ___/   /__/ /   /    '
print '      Social Network Analysis         '
print '     http://www.nodoschile.org        '
print ''

root.config(menu=menubar)
root.resizable(width=FALSE, height=FALSE)
root.mainloop()
