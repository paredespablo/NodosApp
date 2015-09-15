# -*- coding: utf-8 -*-
import Tkinter, tkMessageBox, tkFileDialog, time, re, os, shutil, codecs, imp, tweepy, networkx as nx
from Tkinter import *
from keys import *

##Autenticacion con Tweepy y listas globales
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

##Funcion para crear redes de followers a partir de un nombre de usuario
def followers():
    def libfo():
        user002 = user001.get()
        G=nx.DiGraph()
        G.nodes(data=True) 

        followers_user = []

        a = user002
        followers_user.append(a)
        listade = file('listadefollowers.txt', 'a')

        # Descarga de los followers
        followersCursor = tweepy.Cursor(api.followers,id=a)
        print 'Obteniendo followers'
        for follower in followersCursor.items():
            foll = follower.screen_name
            followers_user.append(foll)
            print foll

        followers_ids = []
        for i in followers_user:
            try:
                data = api.get_user(i)
                i1 = data.id
                followers_ids.append(i1)
            except tweepy.error.TweepError, e:
                if e.response.status:
                    error2 = e[0][0]
                    error = error2['code']
                    if error == 88:
                        print error, error2['message'], "Waiting for 15 minutes"
                        time.sleep(750)
                        data = api.get_user(i)
                        i1 = data.id
                        followers_ids.append(i1)
                    else:
                        print e
            G.add_node(i)

        print >> listade, followers_ids
        listade.close()
        print 'Descarga de followers finalizada'

        # Descarga de followers de los followers
        print 'Obteniendo listas de Followers...'
        os.mkdir('datos')
        carpeta = 'datos/'
        for z in followers_ids:
            followers = []
            try:
                o = str(z)
                followersCursor = tweepy.Cursor(api.followers_ids,id=o)
                for follower in followersCursor.items():
                    foll = follower
                    followers.append(foll)
                ii = file(carpeta + o + '.txt', 'w')
                print >> ii, followers
            except tweepy.error.TweepError, e:
                if e.response.status == 400:
                    print e
                    time.sleep(3600)
                    try:
                        o = str(z)
                        followersCursor = tweepy.Cursor(api.followers_ids,id=o)
                        for follower in followersCursor.items():
                            foll = follower
                            followers.append(foll)
                        ii = file(carpeta + o + '.txt', 'w')
                        print >> ii, followers
                    except tweepy.error.TweepError, e:
                        o = str(z)
                        print e
                        time.sleep(1)
                        ii = file(carpeta + o + '.txt', 'w')
                        print >> ii, 0
                else:
                    print e
                    time.sleep(1)
                    ii = file(carpeta + o + '.txt', 'w')
                    print >> ii, 0
            #print o, len(followers)

        ii.close()

        # Cruce de datos para comprobar lazos
        for p in followers_ids:
            h = str(p)
            archivo = file(carpeta + h + '.txt', 'r')
            ff = archivo.read()
            for q in followers_ids:
                k = str(q)
                if (k in ff) is True:
                    k1 = followers_ids.index(p)
                    k2 = followers_ids.index(q)
                    u1 = followers_user[k1]
                    u2 = followers_user[k2]
                    G.add_edge(u2, u1)
                else:
                    pass
        archivo.close()
        print 'Borrando archivos temporales...'
        shutil.rmtree(carpeta)
        # Exportaciones de redes a GEXF y NET
        print 'Red finalizada'
        nx.draw_random(G)
        nx.write_pajek(G, a + ".net", encoding='UTF-8')
        nx.write_gexf(G, a + ".gexf", encoding='utf-8', prettyprint=True)
        return False
        
    if tkMessageBox.askokcancel("Crear red de followers", "Este proceso puede tardar varias horas dependiendo el numero de seguidores de la cuenta\n\n¿Desea continuar con la operación?"):
        global user001
        root2 =Tk()
        f = Frame(root2, width=1000, height=60)
        f.pack(fill=X, expand=True)
        root2.title('NodosApp: Red de Followers')
        l = Label(f, text="Ingresa el nombre de usuario a analizar")
        l.pack()
        user001 = StringVar(f)
        user000 = Entry(f, textvariable=user001, width=30).pack(side= TOP,padx=10,pady=12)
        but1 = Button(f, text='Crear red de followers', command=libfo, width=25)
        but1.pack(side=LEFT)
        root2.resizable(width=FALSE, height=FALSE)
        root2.mainloop()
    else:
        return False

##Funcion para crear redes de friends/following a partir de un nombre de usuario
def following():
    def libfr():
        user002 = user001.get()
        G=nx.DiGraph()
        G.nodes(data=True) 

        followers_user = []

        a = user002
        followers_user.append(a)
        followersCursor = tweepy.Cursor(api.friends,id=a)
        print 'Obteniendo followers'
        for follower in followersCursor.items():
            foll = follower.screen_name
            #print foll
            followers_user.append(foll)

        followers_ids = []
        for i in followers_user:
            try:
                data = api.get_user(i)
                i1 = data.id
                followers_ids.append(i1)
            except tweepy.error.TweepError, e:
                if e.response.status == 400:
                    print e
                    time.sleep(3600)
                    data = api.get_user(i)
                    i1 = data.id
                    followers_ids.append(i1)
                else:
                    print e
            G.add_node(i)

        print 'Obteniendo listas de Followers...'
        os.mkdir('datos')
        carpeta = 'datos/'
        for z in followers_ids:
            followers = []
            try:
                o = str(z)
                followersCursor = tweepy.Cursor(api.friends_ids,id=o)
                for follower in followersCursor.items():
                    foll = follower
                    followers.append(foll)
                ii = file(carpeta + o + '.txt', 'w')
                print >> ii, followers
            except tweepy.error.TweepError, e:
                if e.response.status == 400:
                    print e
                    time.sleep(3600)
                    try:
                        o = str(z)
                        followersCursor = tweepy.Cursor(api.friends_ids,id=o)
                        for follower in followersCursor.items():
                            foll = follower
                            followers.append(foll)
                        ii = file(carpeta + o + '.txt', 'w')
                        print >> ii, followers
                    except tweepy.error.TweepError, e:
                        o = str(z)
                        print e
                        time.sleep(1)
                        ii = file(carpeta + o + '.txt', 'w')
                        print >> ii, 0
                else:
                    print e
                    time.sleep(1)
                    ii = file(carpeta + o + '.txt', 'w')
                    print >> ii, 0
            #print o, len(followers)

        ii.close()
        for p in followers_ids:
            h = str(p)
            archivo = file(carpeta + h + '.txt', 'r')
            ff = archivo.read()
            for q in followers_ids:
                k = str(q)
                if (k in ff) is True:
                    k1 = followers_ids.index(p)
                    k2 = followers_ids.index(q)
                    u1 = followers_user[k1]
                    u2 = followers_user[k2]
                    G.add_edge(u2, u1)
                else:
                    pass
        archivo.close()
        print 'Borrando archivos temporales...'
        shutil.rmtree(carpeta)
        nx.draw_random(G)
        
        nx.write_pajek(G, a + ".net", encoding='UTF-8')
        nx.write_gexf(G, a + ".gexf", encoding='utf-8', prettyprint=True)
        print 'Red finalizada'
        return False

    if tkMessageBox.askokcancel("Crear red de friends", "Este proceso puede tardar varias horas dependiendo el numero de usuarios que siga la cuenta\n\n¿Desea continuar con la operación?"):
        global user001
        root2 =Tk()
        f = Frame(root2, width=1000, height=60)
        f.pack(fill=X, expand=True)
        root2.title('NodosApp: Red de Friends')
        l = Label(f, text="Ingresa el nombre de usuario a analizar")
        l.pack()
        user001 = StringVar(f)
        user000 = Entry(f, textvariable=user001, width=30).pack(side= TOP,padx=10,pady=12)
        but1 = Button(f, text='Crear red de friends', command=libfr, width=25)
        but1.pack(side=LEFT)
        root2.resizable(width=FALSE, height=FALSE)
        root2.mainloop()
    else:
        return False

## Script para descargar los ultimos 3200 tweets de un usuario
    
def menciones():
    def algmen():
        tweets = []
        user002 = user001.get()
        output = codecs.open(user002 + '.txt', 'a', 'utf-8')
        for page in range(1,32):
            data = api.user_timeline(user002, page=page, include_rts=True, count=200)
            for status in data:
                screen_name = status.user.screen_name
                user_id = status.user.id
                name = status.user.name
                followers_count = status.user.followers_count
                friends_count = status.user.friends_count
                statuses_count = status.user.statuses_count
                created_at = status.created_at
                idioma = status.lang
                autorreg = status.user.created_at
                    
                location0 = status.user.location
                location1 = location0.splitlines()
                location2 = " ".join(location1)
                location = re.sub("[,]", '', location2)
                    
                mensaje_id = status.id
                try:
                    geo_d = SearchResult.geo['coordinates']
                except:
                    geo_d = '[0]'
                source = status.source
                texto0 = status.text
                texto1 = texto0.splitlines()
                mensaje_texto1 = " ".join(texto1)
                mensaje_texto = re.sub("[,]", '', mensaje_texto1)

                if mensaje_id in tweets:
                    pass
                else:
                    tweets.append(mensaje_id)
                print >> output, '"'+str(mensaje_id)+'","'+screen_name+'","'+name+'","'+str(user_id)+'","'+str(autorreg)+'","'+str(followers_count)+'","'+str(friends_count)+'","'+str(statuses_count)+'","'+location+'","'+str(created_at)+'","'+str(geo_d)+'","'+source+'","'+idioma+'","'+mensaje_texto+'"'
                total = int(len(tweets))
                    
        print 'Tweets totales descargados:', len(tweets)
        time.sleep(1)
        output.close()
        return False

    global user001
    root2 =Tk()
    f = Frame(root2, width=1000, height=60)
    f.pack(fill=X, expand=True)
    root2.title('NodosApp: Interacciones')
    l = Label(f, text="Ingresa el nombre de usuario a analizar")
    l.pack()
    user001 = StringVar(f)
    user000 = Entry(f, textvariable=user001, width=30).pack(side= TOP,padx=10,pady=12)
    but1 = Button(f, text='Descargar timeline', command=algmen, width=25)
    but1.pack(side=LEFT)
    root2.resizable(width=FALSE, height=FALSE)
    root2.mainloop()

def mapafollow():
    ##Autenticacion con Tweepy y listas globales
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    usuarios = []
    ids = []
    data3 = tkFileDialog.askopenfilename(title="Open file", filetypes=[("TXT files",".txt"),("All files",".*")])
    data2 = file(data3, 'r')
    data = data2.readlines()
    n1 = data3.split('/')
    n2 = n1[-1]
    n3 = n2[0:-4]
    print 'Cargado el archivo', n3

    for i in data:
        i = i.split(" ")
        usuarios.append(i[0].strip())
    print 'Usuarios', usuarios

    G=nx.DiGraph()
    for k in usuarios:
        for p in usuarios:
            time.sleep(5)
            if (G.has_edge(p, k) or G.has_edge(k, p) or (usuarios.index(k) >= usuarios.index(p))) == True:
                pass
            else:
                print k, p
                try:
                    rel = api.show_friendship(source_screen_name=k, target_screen_name=p)
                    for q in rel:
                        if q.following == True:
                            G.add_edge(k, p)

                        if q.followed_by == True:
                            G.add_edge(p, k)
                except:
                    print 'error entre usuarios', k, p

    n4 = str(n3) + ".gexf"
    nx.write_gexf(G, n4, encoding='utf-8', prettyprint=True)

    print 'Se ha terminado de escribir la red', n4
    
