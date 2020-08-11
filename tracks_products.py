
import matplotlib.pyplot as plt
import matplotlib.patches 
import matplotlib as mpl
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os

import tracks_read
import tracks_density
import tracks_tools

def map_background(domain):
    """
    Construit le fond de carte a partir d'une image et d'un fichier .json.
    in : _coordonnees en degres du domaine geographique sur lequel former le fond de carte. domaine =[Longitude min, Longitude max, Latitude min, Latitude max ] 
    out : _ax : fond de carte, axes nommes
    """

    #recuperation de l'image utilisee comme fond de carte
    #os.environ["CARTOPY_USER_BACKGROUNDS"] = "C:.\\PYTHON\\cartopy\\BG"

    fig, ax = plt.subplots(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.background_img(name='BM', resolution='high', extent=None, cache=False)
    ax.add_feature(cfeature.OCEAN)
    ax.coastlines('50m',color='white',linewidth=1.5)
    ax.add_feature(cfeature.LAKES, alpha=0.95)
    ax.add_feature(cfeature.RIVERS)
    ax.set_ylabel('Latitudes')
    ax.set_xlabel('Longitudes')
    ax.set_extent(domain)
    return ax

def drawtrajectory(Longitudes,Latitudes,ax,color):
    """
    Trace un segment de droite de la couleur choisie, entre 2 points A et B dont les coordonnees sont donnees.
    in : _Longitudes = [Longitude A, Longitude B], Latitudes = [Latitude A, Latitude B], ax = figure sur laquelle tracer le segment (exemple : fond de carte), color = 'couleur du segment'
    out: _ ax = figure sur laquelle a ete rajoutee le segment
    """

    ax.plot(Longitudes, Latitudes, color=color, linewidth=1,transform=ccrs.PlateCarree())
    return ax

def trajectories(df,color,title,filename,boundaries):
    """
    Trace les trajectoires de tous les cyclones qu'on lui donne sur un fond de carte. La carte est ensuite sauvegardee et la fonction de renvoit rien.
    in : _df = dataframe des points des trajectoires des cyclones , du format ressorti par la fonction Readfile, color='couleur des trajectoires', title='titre de la figure', filename='nom de la carte.png'
    out: _carte des trajectoires des cylones sur fond de carte. La carte est enregistree dans le repertoire Maps. Si un fichier preexistant porte le meme nom que la carte, celui-ci est efface.
    """

    #on s'assure  d'effacer tout fichier du repertoire portant le meme nom
    path=os.path.join('.',filename)
    if os.path.isfile(path) :
        os.remove(path)

    #on genere un fond de carte
    #    Boundaries = [-90,29, 30, 89]
    ax=map_background(boundaries)

    #on trace les trajectoires des cyclones une par une
    h=df.groupby('ID')
    for id_cyclone in list(set(df.ID)) :
        Latitudes = h.get_group(id_cyclone)['Latitude']
        Longitudes = h.get_group(id_cyclone)['Longitude']
        ax=drawtrajectory(Longitudes, Latitudes,ax,color=color)

    #sauvegarde de la figure
    plt.title(title)
    plt.savefig(path)
    plt.close()

    return None

def colortendencies(df,title,filename,boundaries):
    """
    Trace des trajectoires des cyclones sur un fond de carte. Les trajectoires sont tracees en fonction de la tendance de pression des cyclones.
    int : _df = dataframe des points des trajectoires des cyclones du format genere par Readfile, title ='titre de la figure', filename='nom du fichier.png'
    out : carte des trajectoires des cyclones tracees selon leur tendance de pression, sauvegardee dans le repertoire Maps
    """

    #on s'assure  d'effacer tout fichier du repertoire portant le meme nom
    path=os.path.join('.',filename)
    if os.path.isfile(path) :
        os.remove(path)

    #on genere un fond de carte
    #    Boundaries = [-90,29, 30, 89]
    ax=map_background(boundaries)

    #on trace les trajectoires des cyclones une par une
    h=df.groupby('ID')
    for id_cyclone in list(set(df.ID)) :

        groupe = h.get_group(id_cyclone)
        Latitudes = groupe['Latitude']
        Longitudes = groupe['Longitude']


        #On calcule la tendance de pression du cyclone le long de sa trajectoire
        tendency = tracks_tools.Tendency1Cyclone(groupe['Pressure'],groupe['Hour'],groupe['Day'])
        j=0
        for i in Latitudes.index[0:-1]:
            #Selon la valeur de la tendance de pression, le segment est trace d'une couleur differente.
            if tendency[j] <= -1.0 :
                color='dodgerblue'
            elif (tendency[j]>=-1) and (tendency[j]<=1):
                color='yellow'
            else:
                color='crimson'
            ax = drawtrajectory([Longitudes[i],Longitudes[i+1]],[Latitudes[i],Latitudes[i+1]],ax,color)
            j+=1
    
    #sauvegarde de la figure
    plt.title(title)
    plt.savefig(path)
    plt.close()

    return None

def map_density(df,title,filename,domain,boundaries):
    """
    Carte de densite totale des trajectoires des cyclones sur toute la periode d'etude, sur fond de carte.
    in : df = dataframe des points des trajectoires des cyclones du format genere par Readfile, title ='titre de la figure', filename='nom du fichier.png'
    out : carte des densites totales des trajectoires des cyclones sur toute la periode d'etude., sauvegardee dans le repertoire Maps. L'unite de la densite depend de l'increment rentre dans la fonction du module de Densite.
    """

    #initialisation des parametres necessaires au calcul de la matrice de densite
    #    domain['lon_min']=-90
    #    domain['lon_max']=90
    #    domain['lat_min']=-90
    #    domain['lat_max']=90
    #    domain['zradius']=3.0e+5
    #    domain['ires']=4
    #    domain['resolution']=1.5

    print("Generating total density map...")
    
    #on s'assure  d'effacer tout fichier du repertoire portant le meme nom
    path=os.path.join('.',filename)
    if os.path.isfile(path) :
        os.remove(path)

    #Calcul de la matrice de densite sur toute la periode d'etude, toutes les annees, associee a df.
    matrix_density = tracks_density.densitymatrix(df,domain)

    n_lon=int((domain['lon_max']-domain['lon_min'])/domain['resolution'])
    n_lat=int((domain['lat_max']-domain['lat_min'])/domain['resolution'])
    Longitudes=np.array([domain['lon_min'] + k*domain['resolution'] for k in range (0,n_lon)])
    Latitudes=np.array([domain['lat_min'] + k*domain['resolution'] for k in range (0,n_lat)])
    
    #on genere un fond de carte
    #    Boundaries = [-90,29, 30, 89]
    ax=map_background(boundaries)

    try :
        #On s'affranchit des valeurs nulles de densite. Celles-ci ne seront pas affichees sur la carte.
        thresh=0
        mask = np.abs(matrix_density) == thresh
        x_ma = np.ma.masked_where(mask, matrix_density)

        #trace des densites en 8 plages de couleurs differentes.
        cfset = ax.contourf(Longitudes,Latitudes,x_ma,8, cmap='rainbow')
        cset = ax.contour(Longitudes,Latitudes, x_ma,8, colors='k')

        #sauvegarde de la figure
        plt.title(title)
        plt.colorbar(cfset)
        plt.savefig(path)
        plt.close()
        print("############## Generation of density map: OK ##############")
    #permet d'eviter les cas ou la matrice de densite est vide, par exemple dans le cas ou le df fourni par l'utilisateur est vide sans le savoir.
    except ValueError:
        print('Error: density matrix is empty. Map cannot be generated. ')
    except :
        print('Unknown error. Map cannot be generated.')

    return None


def map_monthly_density(df,dirname,domain,boundaries):
    """
    Cartes des densites mensuelles des trajectoires des cyclones sur toute la periode d'etude, sur fond de carte.
    in : df = dataframe des points des trajectoires des cyclones du format genere par Readfile, filename='nom du sous-repertoire de Maps'
    out : 12 cartes des densites mensuelles des trajectoires des cyclones sur toute la periode d'etude., sauvegardees dans le repertoire Maps. L'unite de la densite depend de l'increment rentre dans la fonction du module de Densite.
    """

    #    lon_min=-90
    #    lon_max=90
    #    lat_min=-90
    #    lat_max=90
    #    zradius=3.0e+5
    #    ires=4
    #    resolution=1.5

    print("Generate monthly density map...")
    #on s'assure  de l'existence du repertoire, sinon on le cree
    path=os.path.join('.',dirname)
    if not(os.path.isdir(path)) :
        os.mkdir(path)

    n_lon=int((domain['lon_max']-domain['lon_min'])/domain['resolution'])
    n_lat=int((domain['lat_max']-domain['lat_min'])/domain['resolution'])
    Longitudes=np.array([domain['lon_min'] + k*domain['resolution'] for k in range (0,n_lon)])
    Latitudes=np.array([domain['lat_min'] + k*domain['resolution'] for k in range (0,n_lat)])

    monthnames=['0','January','February','March','April','May','June','July','August','October','September','November','December']

    #Pour tous les mois de l'annee :

    for month in range (1,13,1):

        #selection des cyclones correspondant au mois traite
        listmonths=[]
        g=df.groupby('ID')
        for id_cyclone in list(set(df.ID)) :
            Tab=g.get_group(id_cyclone)['Month']
            taille=Tab.shape[0]
            if (sum(Tab==month)>taille/2):
                listmonths.append(id_cyclone)

        listmonths = list(set(listmonths))
        df_monthly = df.loc[df['ID'].isin(listmonths),:]
        df_monthly.reset_index(drop=True,inplace=True)

        #Calcul de la matrice de densite sur toute la periode d'etude, du mois traite.
        matrix_density = tracks_density.densitymatrix(df_monthly,domain)
        
        try :
            #on genere un fond de carte
            #            Boundaries = [-90,29, 30, 89]
            ax=map_background(boundaries)

            #On s'affranchit des valeurs nulles de densite. Celles-ci ne seront pas affichees sur la carte.
            thresh=0
            mask = np.abs(matrix_density) == thresh
            x_ma = np.ma.masked_where(mask, matrix_density)

            #trace des densites en 8 plages de couleurs differentes.
            cfset = ax.contourf(Longitudes,Latitudes,x_ma,8, cmap='rainbow')
            cset = ax.contour(Longitudes,Latitudes, x_ma,8, colors='k')


            #sauvegarde de la carte generee pour le mois traite
            filename = os.path.join(path,"monthly_density_"+monthnames[month]+".png")
            if os.path.isfile(filename):
                os.remove(filename)

            plt.title("Cyclone Tracks Density for "+monthnames[month])
            plt.colorbar(cfset)
            plt.savefig(filename)
            plt.close()
            print("############## Generating density map for "+monthnames[month]+": OK ##############")
        #permet d'eviter les cas ou la mtrice de densite est vide, par exemple dans le cas ou le df fourni par l'utilisateur est vide sans le savoir.
        except ValueError:
            print('Error: density matrix is empty. Map cannot be generated. ')
        except :
            print('Unknown error. Map cannot be generated.')

    return None

def map_seasonal_density(df,dirname,domain,boundaries):
    """
    Cartes des densites saisonnieres des trajectoires des cyclones sur toute la periode d'etude, sur fond de carte.
    in : df = dataframe des points des trajectoires des cyclones du format genere par Readfile, filename='nom du sous-repertoire de Maps'
    out : 4 cartes des densites saisonnieres des trajectoires des cyclones sur toute la periode d'etude., sauvegardees dans le repertoire Maps. L'unite de la densite depend de l'increment rentre dans la fonction du module de Densite.
    """
    
    #initialisation des parametres necessaires au calcul de la matrice de densite
    #    lon_min=-90
    #    lon_max=90
    #    lat_min=-90
    #    lat_max=90
    #    zradius=3.0e+5
    #    ires=4
    #resolution=1.5

    print("Generating seasonal map density...")

    #on s'assure  de l'existence du repertoire , sinon on le cree
    path=os.path.join('.',dirname)
    if not(os.path.isdir(path)) :
        os.mkdir(path)

    n_lon=int((domain['lon_max']-domain['lon_min'])/domain['resolution'])
    n_lat=int((domain['lat_max']-domain['lat_min'])/domain['resolution'])
    Longitudes=np.array([domain['lon_min'] + k*domain['resolution'] for k in range (0,n_lon)])
    Latitudes=np.array([domain['lat_min'] + k*domain['resolution'] for k in range (0,n_lat)])

    saisons = [[12,1,2],[3,4,5],[6,7,8],[9,10,11]]
    list_monthnames = ['DJF','MAM','JJA','SON']

    #Pour toutes les saisons de l'annee :
    for saison in range(4) :

        #selection des cyclones correspondant au mois traite
        df_saison = tracks_read.filter_seasonal(df,saisons[saison])

        #Calcul de la matrice de densite sur toute la periode d'etude, de la saison traitee.
        matrix_density = tracks_density.densitymatrix(df_saison,domain)

        try :
            #on genere un fond de carte
            #Boundaries = [-90,29, 30, 89]
            ax=map_background(boundaries)

            #On s'affranchit des valeurs nulles de densite. Celles-ci ne seront pas affichees sur la carte.
            thresh=0
            mask = np.abs(matrix_density) == thresh
            x_ma = np.ma.masked_where(mask, matrix_density)

            #trace des densites en 8 plages de couleurs differentes.
            cfset = ax.contourf(Longitudes,Latitudes,x_ma,8, cmap='rainbow')
            cset = ax.contour(Longitudes,Latitudes, x_ma,8, colors='k')

            #sauvegarde de la carte generee pour la saison traitee
            filename = os.path.join(path,"seasonal_density_"+list_monthnames[saison]+".png")
            if os.path.isfile(filename):
                os.remove(filename)

            plt.title("Cyclone Tracks Density for season "+list_monthnames[saison])
            plt.colorbar(cfset)
            plt.savefig(filename)
            plt.close()
            print("############## Generating density map "+list_monthnames[saison]+": OK ##############")
        #permet d'eviter les cas ou la mtrice de densite est vide, par exemple dans le cas ou le df fourni par l'utilisateur est vide sans le savoir.
        except ValueError:
            print('Error: density matrix is empty. Map cannot be generated. ')
        except :
            print('Unknown error. Map cannot be generated.')

    return None
