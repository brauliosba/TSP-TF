# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 00:11:30 2019

@author: ASUS
"""

import matplotlib
matplotlib.use('TkAgg')
import random as rnd
import networkx as nx
import pandas as pd
import numpy as np
import itertools 
import folium
import webbrowser
import heapq as hq
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
from geopy import distance
from PIL import ImageTk, Image
path=[]
optimal_path=[]
min_cost=50000

def Leer():
        df1=pd.read_excel(open('C:/Users/ASUS/Desktop/Complejidad-TF/DataBase-CP.xlsx',
                      'rb'),sheet_name='Hoja1',converters={'n°':int},index_col=[0])
        df2=pd.read_excel(open('C:/Users/ASUS/Desktop/Complejidad-TF/DataBase-CP.xlsx',
                      'rb'),sheet_name='Hoja2',converters={'n°':int},index_col=[0])
        df3=pd.read_excel(open('C:/Users/ASUS/Desktop/Complejidad-TF/DataBase-CP.xlsx',
                      'rb'),sheet_name='Hoja3',converters={'n°':int},index_col=[0])
        
        return df1,df2,df3
def fact(long):
    if long==1:
        return long
    return long *fact(long-1)

def arcos_activos(camino):
    lista_arcos=[]
    for i in range(len(camino)):
        if i==len(camino)-1:
            break
        else:
            lista_arcos.append((camino[i],camino[i+1]))
    return lista_arcos

def distancia(p1, p2): 
    return np.round(distance.distance(p1,p2).km)





class mclass:
    
    pathB=[]
    optimal_pathB=[]
    min_costB=50000
    
    def __init__(self,  window):
        self.window = window
        self.window.title("TSP")
        self.cantidad=StringVar()
        self.nodo=StringVar()
        self.optimal_path=[]
        self.optimal_path_w=0
        self.arcos=[]
        load=Image.open("C:/Users/ASUS/Desktop/Complejidad-TF/logo-upc.jpg")
        
        image = load.resize((200, 200), Image.ANTIALIAS)
        render=ImageTk.PhotoImage(image)
        self.img = Label(window, image = render)
        self.img.image=render
        
        self.img.place(x=30,y=120)
        #Elementos de la interfaz
        #caja de texo
        #Desde que nodo empieza el algoritmo
        self.box1 = Entry(window,textvariable=self.nodo).place(x=120,y=60)
       
        #buttons
        
        self.button1  = Button (window, text="Calcular ", command=self.Calcular).place(x=50,y=90)
        self.button2  = Button (window, text="Mapa ", command=self.mapa).place(x=150,y=90)
        #labels
        self.label=Label(window,text="Base de datos").place(x=0,y=0)
        self.label1=Label(window,text="Algoritmo").place(x=0,y=30)
        self.label2=Label(window,text="Nodo").place(x=0,y=60)
        #Text para mostrar solucion
        
        
        
        self.txt=Text(window,width=60,height=50)
        self.txt.pack(side=RIGHT)
        self.txt.insert(END, "Just a text Widget\nin two lines\n")
        #ComboBox
        self.comboBD=ttk.Combobox(window)
        self.comboBD.place(x=120,y=0)
        self.comboBD['values']=('CP-Regionales','CP-Provinciales','CP-Distritales')
        #ComboBox
        self.combo=ttk.Combobox(window)
        self.combo.place(x=120,y=30)
        self.combo['values']=('Prim','Kruskal')
        #Variables a utilizar
        self.DB1,self.DB2,self.DB3=Leer()
        #DB1
        self.Ln1=[]
        self.Lp1=[]
        self.g1=[]
        #DB2
        self.Ln2=[]
        self.Lp2=[]
        self.g2=[]
        #DB3
        self.Ln2=[]
        self.Lp2=[]
        self.g2=[]
        self.g1,self.Ln1,self.Lp1=self.Grafito(self.DB1)
        self.g2,self.Ln2,self.Lp2=self.Grafito(self.DB2)
        self.g3,self.Ln3,self.Lp3=self.Grafito(self.DB3)
        
        
        self.pathB=[]
        self.optimal_pathB=[]
        self.min_costB=50000
        
        
        #Canvas para dibujar grafo
        
    
    def Grafito(self,CPoblados):
        n = len(CPoblados)
        G = [[] for _ in range(n)]
        j = -1
        auxiliar=[]
        lista_nombres=[]
        lista_pos=[]
        for i in range(len(CPoblados)):
            auxiliar.append(eval(CPoblados.iloc[i][4]))
            lista_nombres.append(CPoblados.iloc[i][0])
            lista_pos.append(eval(CPoblados.iloc[i][4]))
        aux=auxiliar
    
        dest = rnd.choice(auxiliar)
        for i in aux:
            CantDestNodo = rnd.randint(4,7) 
            j +=1
            for _ in range(CantDestNodo):
                dest = rnd.choice(aux)
                c=auxiliar.index(dest)
                dist = distancia(i,dest)
                conexion = (c, dist)
                G[j].append(conexion)
    
        return G,lista_nombres,lista_pos
        
    def Calcular(self):
        nd=int(self.nodo.get())
        baseDato=self.comboBD.get()
        op=self.combo.get()

        if op=="Prim":
            if baseDato=='CP-Regionales':
                p,d,l=self.prim(self.g1,nd)
                matrix=self.matrix(self.g1)
                G1 = [[] for _ in range(len(self.g1))]
                for i in range(len(self.g1)):
                    if p[i]==-1:
                        G1[i].append((i,d[i]))
                    else:
                        G1[i].append((p[i],d[i]))
            elif baseDato=='CP-Provinciales':
                p,d,l=self.prim(self.g2,nd)
                matrix=self.matrix(self.g2)
                G1 = [[] for _ in range(len(self.g2))]
                for i in range(len(self.g2)):
                    if p[i]==-1:
                        G1[i].append((i,d[i]))
                    else:
                        G1[i].append((p[i],d[i]))
            elif baseDato=='CP-Distritales':
                p,d,l=self.prim(self.g3,nd)
                matrix=self.matrix(self.g3)
                G1 = [[] for _ in range(len(self.g3))]
                for i in range(len(self.g3)):
                    if p[i]==-1:
                        G1[i].append((i,d[i]))
                    else:
                        G1[i].append((p[i],d[i]))
            
            
          
        
            G2 = nx.Graph()
            for a in G1:
                c=G1.index(a)
                for b in a:
                    v=b[1]
                    G2.add_edge(c,b[0], weight=v)
                  
            tree1 = nx.dfs_preorder_nodes(G2,nd)
            solucion=list(tree1)
            solucion.append(nd)
            self.arcos=arcos_activos(solucion)
            cant=self.TSP(matrix,solucion)
            self.txt.delete('1.0', END)
            self.txt.insert(END,"Camino : "+ str(solucion))
            self.txt.insert(END, "\n"+"Peso: "+str(cant))
            
          
        elif op=='Kruskal':
            if baseDato=='CP-Regionales':
                T, r = self.kruskal(self.g1)
                matrix=self.matrix(self.g1)
                G1 = [[] for _ in range(len(self.g1))]
                for u, v, w in T:
                    G1[u].append((v, w))
            elif baseDato=='CP-Provinciales':
                T, r = self.kruskal(self.g2)
                matrix=self.matrix(self.g2)
                G1 = [[] for _ in range(len(self.g2))]
                for u, v, w in T:
                    G1[u].append((v, w))
            elif baseDato=='CP-Distritales':
                T, r = self.kruskal(self.g3)
                matrix=self.matrix(self.g3)
                G1 = [[] for _ in range(len(self.g3))]
                for u, v, w in T:
                    G1[u].append((v, w))
             
            G2 = nx.Graph()
            for a in G1:
                c = G1.index(a)
                for b in a:
                    v = b[1]
                    G2.add_edge(c, b[0], weight = v)
            #nx.draw(G2)
               
            tree1 = nx.dfs_preorder_nodes(G2,nd)
            solucion=list(tree1)
            solucion.append(nd)
            self.arcos=arcos_activos(solucion)
            cant=self.TSP(matrix,solucion)
            self.txt.delete('1.0', END)
            self.txt.insert(END,"Camino : "+ str(solucion))
            self.txt.insert(END, "\n"+"Peso: "+str(cant))
            
                        
        
        
   
    
    def mapa(self):
        baseDato=self.comboBD.get()
        if baseDato=='CP-Regionales':
            mapa=folium.Map(location=[self.Lp1[0][0],self.Lp1[0][1]])
            for i,j in self.arcos:
                linea=folium.PolyLine(locations=[[self.Lp1[i][0],self.Lp1[i][1]],
                                         [self.Lp1[j][0],self.Lp1[j][1]]],weight=5)
                mapa.add_child(linea)
                fg=folium.FeatureGroup(name="CentroPoblado")
                for n in range(len(self.Ln1)):
                    fg.add_child(folium.Marker(location=self.Lp1[n],
                                      popup=folium.Popup(self.Ln1[n]),
                                      icon=folium.Icon(color='blue',
                                                      icon_color='white',
                                                      icon='info_sing')
                                      ))
                    mapa.add_child(fg)
            
            mapa.save('index.html')
            
            new = 2 # open in a new tab, if possible
    
            # open a public URL, in this case, the webbrowser docs
            url = "index.html"
            webbrowser.open(url,new=new)
        elif baseDato=='CP-Provinciales':
            mapa=folium.Map(location=[self.Lp2[0][0],self.Lp2[0][1]])
            for i,j in self.arcos:
                linea=folium.PolyLine(locations=[[self.Lp2[i][0],self.Lp2[i][1]],
                                         [self.Lp2[j][0],self.Lp2[j][1]]],weight=5)
                mapa.add_child(linea)
                fg=folium.FeatureGroup(name="CentroPoblado")
                for n in range(len(self.Ln2)):
                    fg.add_child(folium.Marker(location=self.Lp2[n],
                                      popup=folium.Popup(self.Ln2[n]),
                                      icon=folium.Icon(color='blue',
                                                      icon_color='white',
                                                      icon='info_sing')
                                      ))
                    mapa.add_child(fg)
            
            mapa.save('index.html')
            
            new = 2 # open in a new tab, if possible
    
            # open a public URL, in this case, the webbrowser docs
            url = "index.html"
            webbrowser.open(url,new=new)
            
            
        elif baseDato=='CP-Distritales':
            mapa=folium.Map(location=[self.Lp3[0][0],self.Lp3[0][1]])
            for i,j in self.arcos:
                linea=folium.PolyLine(locations=[[self.Lp3[i][0],self.Lp3[i][1]],
                                         [self.Lp3[j][0],self.Lp3[j][1]]],weight=5)
                mapa.add_child(linea)
                fg=folium.FeatureGroup(name="CentroPoblado")
                for n in range(len(self.Ln3)):
                    fg.add_child(folium.Marker(location=self.Lp3[n],
                                      popup=folium.Popup(self.Ln3[n]),
                                      icon=folium.Icon(color='blue',
                                                      icon_color='white',
                                                      icon='info_sing')
                                      ))
                    mapa.add_child(fg)
            
            mapa.save('index.html')
            
            new = 2 # open in a new tab, if possible
    
            # open a public URL, in this case, the webbrowser docs
            url = "index.html"
            webbrowser.open(url,new=new)
       
    def prim(self,G,nodo):
        n = len(G)
        dist = [math.inf]*n
        path = [-1]*n
        visited = [False]*n
        q = []
        c=0
        hq.heappush(q, (0, nodo))
        dist[nodo] = 0
        lista=[]
        while len(q) > 0:
            _, u = hq.heappop(q)
            if not visited[u]:
                visited[u] = True
                lista.append(u)
                for v, w in G[u]:
                    if not visited[v] and w < dist[v]:
                        dist[v] = w
                        path[v] = u
                        c += w
                        hq.heappush(q, (w, v))
        
        return path, dist, lista
    def matrix(self,G):
        matrix=np.zeros((len(G),len(G)))
        for u in range(len(G)):
            for j in G[u]:
                matrix[u][j[0]]=j[1]
                matrix[j[0]][u]=j[1]
        return matrix
    def TSP(self,matrix,camino):
        c=0
        for i in range(len(camino)):
            if i==len(camino)-1:
                break
            else:
                c +=matrix[camino[i]][camino[i+1]]
              
        return c
    def find(self,s, a):
        if s[a] < 0:
            return a
        else:
            granpa = self.find(s, s[a])
            s[a] = granpa
            return granpa
    
    def union(self,s, a, b):
        pa = self.find(s, a)
        pb = self.find(s, b)
        if pa == pb: return
        if s[pa] <= s[pb]:
            s[pa] += s[pb]
            s[pb] = pa
        elif s[pb] < s[pa]:
            s[pb] += s[pa]
            s[pa] = pb
        
    def makeIL(self,G):
        il = []
        n = len(G)
        for u in range(n):
            for v, w in G[u]:
                il.append((w, u , v))
        return il

    def kruskal(self,G):
        il = self.makeIL(G)
        q = []
        n = len(G)
        for edge in il:
            hq.heappush(q, edge)
        roots = [-1]*n
        T = []
        while len(q) > 0:
            w, u, v = hq.heappop(q)
            if self.find(roots, u) != self.find(roots, v):
                self.union(roots, u , v)
                T.append((u, v, w))
        return T, roots
    
    
    
#Inicializador de la APP   
window= Tk()
window.geometry('750x400')
start= mclass (window)
window.mainloop()