
import numpy as np
import pandas as pd
import tracks_density
import tracks_read

def stddev_interannual(df,domain):
    """
    Fonction de calcul de l'ecart-type inter-annuel de la densite de trajectoires des cyclones d'un jeu de donnees.
    L'ecart-type est calcule en chaque point de grille. On obtient donc une matrice d'ecarts-type inter-annuels.
    in : _df= dataframe des points des trajectoires des cyclones ; lat_max,lat_min,lon_max,lon_min,zradius,resolution,ires : parametres necessaires au calcul de la matrice de densite
    out : _ecart-type = matrice des ecarts-types inter-annuels de la densite, de meme dimension que la matrice de densite a partir de laquelle elle est calculee.
    """

    #Pour chaque annee :
    for annee in range(min(df['Year']),max(df['Year'])+1,1):
        print('Current year:',annee)

        #selection des cyclones de l'annee traitee
        df_annee = tracks_read.strictequality(df,'Year',annee)

        #Calcul de la matrice de densite associee a l'annee traitee
        matrix_density=tracks_density.densitymatrix(df_annee,domain)

        #Stockage de toutes les matrices de densite sous forme de vecteurs
        lon=matrix_density.shape[0]
        lat=matrix_density.shape[1]
        vecteur=matrix_density.reshape(1,lon*lat)

        if annee==min(df['Year']) :
            big_matrice = vecteur
        else :
            big_matrice = np.concatenate((big_matrice,vecteur),axis=0)
    #Calcul de la matrice d'ecarts-type calcules en chaque point de grille
    std_dev=np.std(big_matrice,axis=0)
    std_dev=std_dev.reshape(lon,lat)

    return std_dev


def stddev_interseasonal(df,seasons,domain):
    """
    Fonction de calcul de l'ecart-type inter-saisonnier de la densite de trajectoires des cyclones d'un jeu de donnees.
    L'ecart-type est calcule en chaque point de grille. On obtient donc une matrice d'ecarts-type inter-saisonniers.
    in : _df= dataframe des points des trajectoires des cyclones ; saisons=liste des saisons a traiter exemple pour ete et hiver : saisons = [[12,1,2],[6,7,8]]
     lat_max,lat_min,lon_max,lon_min,zradius,resolution,ires : parametres necessaires au calcul de la matrice de densite
    out : _ecart-type = matrice des ecarts-types inter-saisonniers de la densite, de meme dimension que la matrice de densite a partir de laquelle elle est calculee.
    """
    
    #Pour chaque saison :
    for season in range(len(seasons)) :

        #selection des cyclones de la saison traitee
        df_season = R.seasonal(df,seasons[season])

        #Calcul de la matrice de densite associee a la saison traitee
        matrix_density = density.densitymatrix(df_season,domain)

        #stockage de toutes les matrices de densite sous forme de vecteurs
        lon=matrix_density.shape[0]
        lat=matrix_density.shape[1]
        vecteur=matrix_density.reshape(1,lon*lat)

        if season==0 :
            big_matrice = vecteur
        else :
            big_matrice = np.concatenate((big_matrice,vecteur),axis=0)

    #Calcul de la matrice des ecarts-type calcules en chaque point de  grille
    std_dev=np.std(big_matrice,axis=0)
    std_dev=std_dev.reshape(lon,lat)

    return std_dev
