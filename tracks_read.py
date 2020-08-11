
import pandas as pd
import numpy as np
import os

def readfile(path,filename):
	"""
	Lit un fichier tracks.txt, le decoupe sur la periode de reference selon le nom du fichier puis le convertit en dataframe des points des trajectoires des cyclones.
	Les longitudes sont converties pour etre contenues dans la fenetre (-180,+180).
	Ce dataframe est utilise par la suite dans la majorite des fonctions, celui-ci facilite le traitement d'operations ainsi que la visualisation en temps reel des donnees.
	in : _fichier 'tracks.txt' genere par le code de tracking.
	out : _df = dataframe avec pour colonnes  : 
	'ID'=numero du cyclone, 'Latitude'=latitude du point de la trajectoire du cylone, 'Longitude'=longitude du point de la trajectoire du cyclone,
	 'Pression' = minimum de pression au centre du cyclone, 'Vorticite' = maximum de tourbillon relatif au centre du cyclone, 'Heure' / 'Jour' /'Mois' / 'Annee' : date a laquelle correspondent les valeurs du point du cyclone
	"""

	#================== OUVERTURE DU FICHIER TRACKS GENERE =================================================

	#on lit les donnees dans un dataframe
	fichier=os.path.join(path,filename)
	df = pd.read_table(fichier,sep=" ",header=None)

	#on nomme les colonnes du dataframe
	df.columns=['ID','Latitude','Longitude','Vorticity','Pressure','Hour','Day','Month','Year']

	#on convertit les longitudes
	df.loc[df['Longitude']>180,'Longitude']-=360

	liste=[]
	g=df.groupby('ID')
	for id_cyclone in list(set(df.ID)):
		if g.get_group(id_cyclone).shape[0]>1 :
			liste.append(id_cyclone)

	df=df.loc[df['ID'].isin(liste),:]

	return df

def filter_lowerbound(df,Variable,threshold):
	"""
	Fonction de filtrage par seuil.
	Selection des cyclones qui ont au moins un point de leur trajectoire dont la valeur de la variable choisie par l'utilisateur est superieure ou egale a un certain seuil.
	in : _df =dataframe des points des trajectoires des cyclones, Variable='colonne a laquelle on s'interesse', threshold=float(valeur du seuil)
	out : _df_new = dataframe des cyclones qui respectent la condition imposee.
	"""
	#selection des numeros des cyclones respectant la condition
	filter = df.loc[df[Variable]>=threshold,:]
	listfilter=list(set(filter.ID))

	#selection des lignes associees a ces numeros de cyclones
	df_new=df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_new.reset_index(drop=True,inplace=True)
	return df_new

def filter_upperbound(df,Variable,threshold):
	"""
	Fonction de filtrage par seuil.
	Selection des cyclones qui ont au moins un point de leur trajectoire dont la valeur de la variable choisie par l'utilisateur est inferieure ou egale a un certain seuil.
	in : _df =dataframe des points des trajectoires des cyclones, Variable='colonne a laquelle on s'interesse', threshold=float(valeur du seuil)
	out : _df_new = dataframe des cyclones qui respectent la condition imposee.
	"""
	#selection des numeros des cyclones respectant la condition
	filter = df.loc[df[Variable]<=threshold,:]
	listfilter=list(set(filter.ID))

	#selection des lignes associees a ces numeros de cyclones
	df_new = df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_new.reset_index(drop=True,inplace=True)
	return df_new

def filter_strictlowerbound(df,Variable,threshold):
	"""
	Fonction de filtrage par seuil.
	Condition de seuil : la valeur de la variable choisie par l'utilisateur est superieure ou egale a un certain seuil.
	Selection des cyclones dont tous les points de leur trajectoire respectent la condition de seuil.
	in : _df =dataframe des points des trajectoires des cyclones, Variable='colonne a laquelle on s'interesse', threshold=float(valeur du seuil)
	out : _df_new = dataframe des cyclones qui respectent la condition imposee.
	"""

	listfilter=[]
	g=df.groupby('ID')

	#selection des numeros des cyclones respectant la condition
	for id_cyclone in list(set(df.ID)) :
		#Selection du morceau, qui correspond a un unique cyclone, de la colonne associee a la variable
		Tab=g.get_group(id_cyclone)[Variable]
		taille=Tab.shape[0]
		#toutes la valeurs de ce morceau sont superieures ou egales au seuil
		if (sum(Tab>=threshold) == taille) :
			listfilter.append(id_cyclone)
	listfilter = list(set(listfilter))
	
	#selection des lignes associees a ces numeros de cyclones
	df_new = df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_new.reset_index(drop=True,inplace=True)

	return df_new

def filter_strictexcludinglowerbound(df,Variable,threshold):
	"""
	Fonction de filtrage par seuil.
	Condition de seuil : la valeur de la variable choisie par l'utilisateur est strictement superieure a un certain seuil.
	Selection des cyclones dont tous les points de leur trajectoire respectent la condition de seuil.
	in : _df =dataframe des points des trajectoires des cyclones, Variable='colonne a laquelle on s'interesse', threshold=float(valeur du seuil)
	out : _df_new = dataframe des cyclones qui respectent la condition imposee.
	"""
	listfilter=[]
	g=df.groupby('ID')

	#selection des numeros des cyclones respectant la condition
	for id_cyclone in list(set(df.ID)) :
		#Selection du morceau, qui correspond a un unique cyclone, de la colonne associee a la variable
		Tab=g.get_group(id_cyclone)[Variable]
		taille=Tab.shape[0]
		#toutes la valeurs de ce morceau sont strictement superieures au seuil
		if (sum(Tab>threshold) == taille) :
			listfilter.append(id_cyclone)
	listfilter = list(set(listfilter))

	#selection des lignes associees a ces numeros de cyclones
	df_new = df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_new.reset_index(drop=True,inplace=True)

	return df_new

def filter_strictupperbound(df,Variable,threshold):
	"""
	Fonction de filtrage par seuil.
	Condition de seuil : la valeur de la variable choisie par l'utilisateur est inferieure ou egale a un certain seuil.
	Selection des cyclones dont tous les points de leur trajectoire respectent la condition de seuil.
	in : _df =dataframe des points des trajectoires des cyclones, Variable='colonne a laquelle on s'interesse', threshold=float(valeur du seuil)
	out : _df_new = dataframe des cyclones qui respectent la condition imposee.
	"""
	listfilter=[]
	g=df.groupby('ID')

	#selection des numeros des cyclones respectant la condition
	for id_cyclone in list(set(df.ID)) :
		Tab=g.get_group(id_cyclone)[Variable]
		taille=Tab.shape[0]
		#ajoute les numeros des cyclones dont toutes la valeurs sont inferieures ou egales au seuil
		if (sum(Tab<=threshold) == taille) :
			listfilter.append(id_cyclone)
	listfilter = list(set(listfilter))

	#selection des lignes associees a ces numeros de cyclones
	df_new= df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_new.reset_index(drop=True,inplace=True)

	return df_new

def filter_strictequality(df,Variable,threshold):
	"""
	Fonction de filtrage par seuil.
	Condition de seuil : la valeur de la variable choisie par l'utilisateur est egale a un certain seuil.
	Selection des cyclones dont tous les points de leur trajectoire respectent la condition de seuil.
	in : _df =dataframe des points des trajectoires des cyclones, Variable='colonne a laquelle on s'interesse', threshold=float(valeur du seuil)
	out : _df_new = dataframe des cyclones qui respectent la condition imposee.
	"""

	listfilter=[]
	g=df.groupby('ID')

	#selection des numeros des cyclones respectant la condition
	for id_cyclone in list(set(df.ID)) :
		Tab=g.get_group(id_cyclone)[Variable]
		taille=Tab.shape[0]
		#ajoute les numeros des cyclones dont toutes la valeurs sont egales au seuil
		if (sum(Tab==threshold) == taille) :
			listfilter.append(id_cyclone)
	listfilter = list(set(listfilter))
	
	#selection des lignes associees a ces numeros de cyclones
	df_new = df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_new.reset_index(drop=True,inplace=True)

	return df_new

def filter_seasonal(df,listmonths):
	"""
	Fonction de filtrage des cyclones selon la saison a laquelle ils appartiennent et la saison demandee par l'utilisateur.
	in : _df = dataframe des points des trajectoires des cyclones,
	 liste_3mois = saison choisie par l'utilisateur : pour l'hiver(DJF) liste_3mois=[12,1,2], pour le printemps(MAM) liste_3mois=[3,4,5], pour l'ete(JJA) liste_3mois=[6,7,8] et pour l'automne(SON) liste_3mois=[9,10,11]
	 out : _df_saison = dataframe des points des trajectoires des cyclones qui appartiennent a la saison demandee.
	"""
	listfilter=[]
	g=df.groupby('ID')

	#selection des numeros des cyclones respectant la condition
	for id_cyclone in list(set(df.ID)) :
		Tab=g.get_group(id_cyclone)['Month']
		taille=Tab.shape[0]
		#ajoute le numero du cyclone a la liste si plus de la moitie des points de sa trajectoire se trouve dans un des 3 mois de la saison
		if ((sum(Tab==listmonths[0]) >= taille/2) or (sum(Tab==listmonths[1]) >= taille/2) or (sum(Tab==listmonths[2]) >= taille/2)):
			listfilter.append(id_cyclone)

	listfilter = list(set(listfilter))

	#selection des lignes associees a ces numeros de cyclones
	df_season = df.loc[df['ID'].isin(listfilter),:]

	#reindexation du dataframe apres decoupage
	df_season.reset_index(drop=True,inplace=True)

	return df_season

def quantiles(df):
	"""
	Fonction de classement des cyclones d'apres leur intensite.
	Cette fonction genere 3 dataframes, des cyclones consisederes comme de forte, faible ou d'extreme intensite.
	in : _df = dataframe des points des trajectoires des cyclones
	out : _df= StrongCyclones, WeakCyclones, ExtremeCyclones : dataframes des points des trajectoires des cyclones consideres respectivement comme intenses faibles ou extremes.
	"""

	#Calcul des quantiles necessaires au classement
	P_001= np.quantile(df.Pressure,0.01)
	P_025= np.quantile(df.Pressure,0.25)
	P_075= np.quantile(df.Pressure,0.75)
	V_025= np.quantile(df.Vorticity,0.25)
	V_075= np.quantile(df.Vorticity,0.75)
	V_099= np.quantile(df.Vorticity,0.99)
	
	STRONGCyclonesList, WEAKCyclonesList, EXTREMECyclonesList=[], [], []
	g=df.groupby('ID')

	#selection des numeros des cyclones respectant l'une des 3 conditions
	for id_cyclone in list(set(df.ID)) :
		MinPressure, MaxVorticity = g.get_group(id_cyclone)['Pressure'].min(), g.get_group(id_cyclone)['Vorticity'].max()
		#selection des cyclones d'intensite extreme
		if ((MinPressure <= P_001) and (MaxVorticity >= V_099)):
			EXTREMECyclonesList.append(id_cyclone)
		#selection des cyclones de forte intensite
		if ((MinPressure <= P_025) and (MaxVorticity >= V_075)):
			STRONGCyclonesList.append(id_cyclone)
		#selection des cyclones de faible intensite
		elif ((MinPressure >= P_075) and (MaxVorticity <= V_025)):
			WEAKCyclonesList.append(id_cyclone)
	
	#selection des lignes associees a ces numeros de cyclones
	StrongCyclones = df.loc[df['ID'].isin(STRONGCyclonesList),:]
	WeakCyclones = df.loc[df['ID'].isin(WEAKCyclonesList),:]
	ExtremeCyclones = df.loc[df['ID'].isin(EXTREMECyclonesList),:]

	#reindexation des dataframes apres decoupage
	StrongCyclones.reset_index(drop=True,inplace=True)
	WeakCyclones.reset_index(drop=True,inplace=True)
	ExtremeCyclones.reset_index(drop=True,inplace=True)

	return StrongCyclones, WeakCyclones, ExtremeCyclones
