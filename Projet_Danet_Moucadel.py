#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/10/2020

@author: Matthieu Moucadel et Chloé Danet
"""

################################## Déclaration des classes ##################################
#import nltk
#nltk.download()
#Import d'une liste de mots qui ne sont intéressant à analyser (the, of, in...)
import datetime as dt
import pickle 

class Corpus():
    
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
        self.chainereunie = ""
        self.dico = []
            
    def add_doc(self, doc):
        
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
            
    def add_aut(self, aut_name,doc):
        
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        
        self.naut += 1

    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        id2 = aut2id.get(author_name)
        return id2

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]

    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
            
    def chainereuniefonc(self):
        import re
        if (self.chainereunie == ""):
            for doc in self.collection:
                chaine = self.collection[doc].get_text()
                chaine = re.sub(r'[^\w\s]','',chaine)
                #Suppression de la ponctuation, des apostrophes afin de ne pas perdre des mots dans le compte
                chaine = chaine.replace("  ","")
                #Suppression des doubles espaces qui gênaient dans le compte des mots
                self.chainereunie += (chaine)
                
                
    def search(self, keyword):
            import re
            sample = ""
            self.chainereuniefonc() 
            if keyword in self.chainereunie:
               for m in re.finditer(keyword, self.chainereunie):
                   for i in range(m.start(0) - 50, m.end(0) + 50):
                       sample += self.chainereunie[i]
            print(sample)
                               
    def concorde(self, keyword, taille):
            import re
            sample = ""
            if keyword in self.chainereunie:
               for m in re.finditer(keyword, self.chainereunie):
                   for i in range(m.start(0) - taille, m.end(0) + taille):
                       sample += self.chainereunie[i]
            print(sample)
        
    def stats(self):
        import pandas
        #appel fonction pour suppression des sauts de ligne
        self.nettoyer_texte()
        if len(self.dico) == 0:
            #appel fonction pour former 1 seule chaine de carac. avec les documents
            self.dico = self.chainereunie.split(" ")
            from nltk.corpus import stopwords
            #pour chacun des mots du corpus...
            for word in self.dico:
                #Suppression des mots qui ne sont pas intéressants grâce à la liste stopwords
                if word in stopwords.words('english'):
                    self.dico = list(filter(lambda a: a != word, self.dico))      
            data = pandas.DataFrame.from_dict(self.dico)
            #nbre d'occurences des mots
            occurences = data[0].value_counts()
            #frequence d'apparition
            frequence = data[0].value_counts()/len(self.dico)
            print("--------------Occurences-------------- \n", occurences)
            print("--------------Frequences-------------- \n",frequence)
            
    
    def tf_idf(self):
        import re
        from nltk.corpus import stopwords
        tous_mots = {}
        nbr_mot = []
        cpt = 0
        num_doc = 1
        #idf_dict = {}
        #doc_dict = {}
        
        for doc in self.collection:
            chaine = self.collection[doc].get_text()
            #On récupère le texte du document
            chaine = re.sub(r'[^\w\s]','',chaine)
            #Suppression de la ponctuation, des apostrophes afin de ne pas perdre des mots dans le compte
            chaine = chaine.replace("  ","")
            #Suppression des doubles espaces
            chaine = chaine.split(" ")
            #On transforme la chaine en liste de mots
            for word in chaine:
                if word in stopwords.words('english'):
                    chaine = list(filter(lambda a: a != word, chaine))
            #On retire les stopwords de la chaine
            nbr_mot.append(len(chaine))
            #On garde en mémoire le nombre de mot dans le document
            tous_mots = set(tous_mots).union(set((chaine)))
            #chaque document triés sont unis pour avoir chacun des mots trouvés dans l'ensemble des documents
            
        #print(tous_mots)
        #print(nbr_mot)
        
        for doc in self.collection:
            chaine = self.collection[doc].get_text()
            #On récupère le texte du document
            chaine = re.sub(r'[^\w\s]','',chaine)
            #Suppression de la ponctuation, des apostrophes afin de ne pas perdre des mots dans le compte
            chaine = chaine.replace("  ","")
            #Suppression des doubles espaces
            
            chaine = chaine.split(" ")
            #On transforme la chaine en liste de mots
            for word in chaine:
                if word in stopwords.words('english'):
                    chaine = list(filter(lambda a: a != word, chaine))
            #On retire les stopwords de la chaine         
            mot_dict = dict.fromkeys(tous_mots, 0)
            #On créé un dictionnaire avec comme clé chaques mots uniques relevé dans le document
            for mot in chaine:
                mot_dict[mot] += 1
                #On compte pour chaque mot combien de fois il apparait dans le document
            tf_dict = {}
            for mot, count in mot_dict.items():
                tf_dict[mot] = count / nbr_mot[cpt]
                #Pour chaque mot on calcule le tf, c'est à dire on fais la division entre le nombre de fois ou le mot
                #apparait dans le document divisé par le nombre de mot dans le document
            tf_dict = {k: v for k, v in sorted(tf_dict.items(), key=lambda item: item[1],reverse = True)}
            #On trie le dictionnaire dans l'ordre décroissant pour voir les mots qui apparaissent le plus de fois en premier
            tf_dict = {x:y for x,y in tf_dict.items() if y!=0}
            #On retire les item du dictionnaire pour lesquels la valeur est de 0, pour un affichage plus digeste
            print("TF du document numéro " + str(num_doc))
            print()
            print(tf_dict)
            print()
            cpt += 1
            num_doc += 1

            
        
        
        
        
        
    def nettoyer_texte(self):
        self.chainereunie = self.chainereunie.lower()
        self.chainereunie.replace("\n"," ") 

            
            
        
       

class Author():
    def __init__(self,name):
        self.name = name
        self.production = {}
        self.ndoc = 0
        
    def add(self, doc):     
        self.production[self.ndoc] = doc
        self.ndoc += 1

    def __str__(self):
        return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)
    def __repr__(self):
        return self.name
    


class Document():
    
    # constructor
    def __init__(self, date, title, author, text, url, type):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
        self.type = type
    
    # getters
    
    def get_author(self):
        return self.author

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        return self.source
        
    def get_text(self):
        return self.text

    def __str__(self):
        return "Document " + self.getType() + " : " + self.title
    
    def __repr__(self):
        return self.title
    
    def getType(self):
        return self.type
        
        
        

    
class RedditDocument(Document):
    
    def __init__(self, date, title, author, text, url, type, nbcomm):
        super().__init__(date, title, author, text, url, type)
        self.nbcomm = nbcomm
        
    def getnbcomm(self):
        return self.nbcomm
    
    def setnbcomm(self, nbcomm):
        self.nbcomm = nbcomm
    
    def __str__(self):
        return (super().__str__() + " Nbcomm : " + str(self.nbcomm))
    
    def getType(self):
        return super().getType()
    

class ArxivDocument(Document):
    
    def __init__(self, date, title, author, text, url, type, coauthor):
        super().__init__(date, title, author, text, url, type)
        self.coauthor = coauthor
    
    def getdate(self):
        return self.date
    
    def setdate(self, date):
        self.date = date
        
    def gettitle(self):
        return self.title
    
    def settitle(self, title):
        self.title = title
        
    def getauthor(self):
        return self.author
    
    def setauthor(self, author):
        self.author = author
    
    def gettext(self):
        return self.text
    
    def settext(self, text):
        self.text = text
    
    def geturl(self):
        return self.url
    
    def seturl(self, url):
        self.url = url
    
    def getcoauthor(self):
        return self.coauthor
    
    def setcoauthor(self, coauthor):
        self.coauthor = coauthor
    
    def __str__(self):
        return (super().__str__() + " Co-auteurs : " + self.coauthor)
           
    def getType(self):
        return super().getType()


import praw

import urllib.request
import xmltodict   



################################## Création du Corpus ##################################

corpus_reddit = Corpus("Corpus Reddit")

corpus_arxiv = Corpus("Corpus Arxiv")

reddit = praw.Reddit(client_id='dYbdTHKJ7DSwcw', client_secret='Naoq5Fp2Moby_bORTuf7IKFRQGs', user_agent='td1 progra')
hot_posts = reddit.subreddit('Coronavirus').hot(limit=50)
for post in hot_posts:
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = Document(datet,
                   post.title,
                   post.author_fullname,
                   txt,
                   post.url, "Reddit")
    corpus_reddit.add_doc(doc)

url = 'http://export.arxiv.org/api/query?search_query=all:Coronavirus&start=0&max_results=50'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

for i in docs:
    datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
    try:
        author = [aut['name'] for aut in i['author']][0]
    except:
        author = i['author']['name']
    txt = i['title']+ ". " + i['summary']
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = Document(datet,
                   i['title'],
                   author,
                   txt,
                   i['id'],
                   "Arxiv"
                   )
    corpus_arxiv.add_doc(doc)


print("####REDDIT####")
corpus_reddit.chainereuniefonc()
#corpus_reddit.tf_idf()
#resu_reddit = corpus_reddit.stats()
    

print("--------------------------------------------------------------------------------")

print("####ARXIV####")
corpus_arxiv.chainereuniefonc()
#corpus_arxiv.tf_idf()
#resu_arxiv = corpus_arxiv.stats()

