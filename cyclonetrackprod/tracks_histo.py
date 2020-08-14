
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from . import tracks_read.py
from . import tracks_tools.py

def histo_curve(variableslist,labelvariables,colors,title,xlabel,path):
    """
    Fonction de trace de plusieurs histogrammes sous forme de courbes sur une meme figure.
    Cette fonction a l'avantage de pouvoir tracer autant d'histogrammes que l'on souhaite sur la meme figure.
    Les figures sont sauvegardees dans le repertoire indique.
    in : _variableslist : colonne d'une meme variable pour plusieurs dataframe (exemple : ListeVariable=[ colonne de la pression du dataframe 1, colonne de la pression du dataframe 2, ...]) / fonctionne egalement avec des vecteurs
    labelvariables : noms des courbes labelvariables=['courbe1','courbe2',...], colors=['couleur 1','couleur 2'], title ='title de la figure', xlabel='nom de l'axe des abscisses', path='repertoire/nom_fichier.png'
    out : _figure des histogrammes sous forme de courbes superposees.
    """

    #on s'assure  d'effacer tout fichier du repertoire portant le meme nom
    if os.path.isfile(path) :
        os.remove(path)

    #On trace les courbes de toutes les variables presentes dans la liste, avec leur label et leur couleur respectifs
    for i in range(len(variableslist)):
        sns.kdeplot(variableslist[i], shade=True,bw = 0.5, color = colors[i], legend = True, label = labelvariables[i])

    plt.ylabel('Frequency')
    plt.xlabel(xlabel)
    plt.title(title, fontsize=10)
    plt.legend()
    #sauvegarde de la figure
    plt.savefig(path)
    plt.close()

    return None

def histo(variableslist,labelvariables,colors,title,xlabel,path):
    """
    Fonction de trace de plusieurs figures, un seul histogramme sous forme de bâtons par figure.
    Les figures sont sauvegardees dans le repertoire indique.
    in : _variableslist : colonnes de dataframes (exemple : ListeVariable=[ colonne de la pression du dataframe 1, colonne de la pression du dataframe 2, ...]) / fonctionne egalement avec des vecteurs
    labelvariables : noms des histogrammes labelvariables=['histo1','histo2',...], colors=['couleur 1','couleur 2'], title ='title commun a toutes les figures', xlabel='nom de l'axe des abscisses', path='repertoire/nom_fichier.png'
    out : _figure des histogrammes sous forme de courbes superposees.
    """

    #on s'assure  d'effacer tout fichier du repertoire portant le meme nom
    if os.path.isfile(path) :
        os.remove(path)

    #On trace les histogrammes de toutes les variables presentes dans la liste, avec leur label et leur couleur respectifs
    #Chaque histogramme est trace sur une figure differente.
    for i in range(len(variableslist)):
        #plt.hist(variableslist[i], color = colors[i],bins=20,label=labelvariables[i])
        plt.hist(variableslist[i], color = colors[i],bins=20,label=labelvariables[i])

        plt.ylabel('Number of points')
        plt.xlabel(xlabel)
        plt.title(title, fontsize=10)
        plt.legend()

        #sauvegarde de la figure
        plt.savefig(path+labelvariables[i]+'.png')
        plt.close()

    return None

def histo_joint(variableslist,labelvariables,title,filename):
    """
    Fonction qui trace deux histogrammes sur le meme graphe et les met en relation : un histogramme est associe a l'axe des abscisses, le second a l'axe des ordonnees.
    in : _variableslist : liste de la colonne des 2 variables d'un dataframe a mettre en relation, VariableLabels liste des noms des variables,title='title de la figure', filename='nom du fichier.png'
    out : figure des deux histogrammes en relation
    """

    #ne fonctionne que pour 2 histogrammes, i.e 2 variables dans variableslist
    if len(variableslist)==2 :
        #trace de la figure
        sns.jointplot(Variable[0],Variable[1],kind="kde",space=0,color="g")

        #sauvegarde de la figure 
        plt.title(title, fontsize=10)
        plt.savefig(filename)
        plt.show()
    
    return None

def histo_time(df_present,df,df_S,path):
    if os.path.isfile(path) :
        os.remove(path)

    g=df.groupby('ID')
    h=df_S.groupby('ID')
    #i=df_EX.groupby('ID')
    yearlist, yearlist_S=[], []
    for id_cyclone in list(set(df_present.ID)):
        annee=list(set(g.get_group(id_cyclone)['Year']))
        yearlist.append(annee[0])
    for id_cyclone in list(set(df.ID)):
        annee=list(set(g.get_group(id_cyclone)['Year']))
        yearlist.append(annee[0])
    for id_cyclone in list(set(df_S.ID)) :
        annee_S=list(set(h.get_group(id_cyclone)['Year']))
        yearlist_S.append(annee_S[0])
    #for id_cyclone in list(set(df_EX.ID)):
     #   annee_EX=list(set(i.get_group(id_cyclone)['Annee']))
     #   yearlist_EX.append(annee_EX[0])

    b=max(yearlist)-min(yearlist)
    ticks=[]
    for i in range(min(yearlist),max(yearlist)+1,1) :
        ticks.append(str(i))
    plt.hist([yearlist,yearlist_S],color=['dodgerblue','crimson'],bins=b,width=0.2,label=['cyclones','strong cyclones'])
    plt.xticks(range(min(yearlist),max(yearlist)+1,1),ticks,fontsize=5)
    plt.xlabel('Years ('+str(min(yearlist))+'-'+str(max(yearlist))+')',fontsize=7)
    plt.ylabel('Number of cyclones')
    plt.legend()
    plt.title('Change in number of cyclones')
    plt.savefig(path)
    plt.close()
    return None
