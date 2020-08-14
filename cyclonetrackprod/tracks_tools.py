
import numpy as np
import pandas as pd

def distance2pts(Latitude1,Longitude1,Latitude2,Longitude2):
	"""
	Fonction de calcul de la distance entre 2 points 1 et 2.
	in : _coordonnees en degres des deux points 1 et 2. (float)
	out : _distance en km (float)
	"""
	#Rayon de la Terre
	R = 6.371e+6
	Distance = 0.
	if ((Latitude1 != Latitude2) and (Longitude1 != Longitude2)):

		#Conversion des latitudes et longitudes (donnees en degres) en radians
		Latitude1 = Latitude1 * (np.pi / 180.0)
		Longitude1 = Longitude1 * (np.pi /180.0)
		Latitude2 = Latitude2 * (np.pi / 180.0)
		Longitude2 = Longitude2 * (np.pi /180.0)
		#Calcul de la distance
		Distance = np.arccos(np.cos(Latitude1)*np.cos(Latitude2)*np.cos(Longitude2-Longitude1)+np.sin(Latitude1)*np.sin(Latitude2))*R

		#conversion en km
		Distance = float( Distance /1000.0 )

	return Distance


def distancecyclone(Latitudes,Longitudes):
	"""
	Fonction de calcul des distances parcourues par un cyclone entre les points de sa trajectoire.
	in : _Latitudes/Longitudes : colonne des Latitudes/Longitudes correspondant a ce cyclone du dataframe df  / fonctionne aussi avec le format en vecteurs
	out : _Distance = vecteur des distances entre les points de la trajectoire du cyclone
	"""

	Distance = np.zeros(Latitudes.shape[0]-1)
	j=0
	for i in Latitudes.index[0:-1] :
		#distance entre 2 points consecutifs dans l'ordre chronologique
		Distance[j]=distance2pts(Latitudes[i],Longitudes[i],Latitudes[i+1],Longitudes[i+1])
		j+=1
	return Distance


def velocitycyclone(Latitudes,Longitudes,hour,day):
	"""
	Fonction de calcul des vitesses atteintes par un cyclone entre les points de sa trajectoire.
	in : _Latitudes/Longitudes/Heure/Jour: colonne des Latitudes/Longitudes/Heure/Jour correspondant à ce cyclone du dataframe df  / fonctionne aussi avec le format en vecteurs
	out : _Vitesse = vecteur des vitesses entre les points de la trajectoire du cyclone
	"""

	Velocity=np.zeros(Latitudes.shape[0]-1)
	j=0
	for i in Latitudes.index[0:-1]:
		if day[i+1] == day[i]:
			dt = hour[i+1] - hour[i]
		else :
			dt = hour[i+1] + (24 - hour[i])
		if (dt > 0.) :
			#Calcul de la vitesse
			Velocity[j] = Distance2Points(Latitudes[i],Longitudes[i],Latitudes[i+1],Longitudes[i+1]) / dt	
		j+=1

	return Velocity


def Tendency1Cyclone(Variable,hours,days):
	"""
	Fonction de calcul de la tendance d'une variable le long de la trajectoire d'un cyclone.
	in : _Variable/Heures/Jours: colonne des Variable/Heure/Jour correspondant à ce cyclone du dataframe df  / fonctionne aussi avec le format en vecteurs
	out : _Tendance = vecteur des tendances de la variable entre les points de la trajectoire du cyclone
	"""

	Tendance=np.zeros(Variable.shape[0]-1)
	j=0
	for i in Variable.index[0:-1]:
		if days[i+1] == days[i]:
			dt = hours[i+1] - hours[i]
		else :
			dt = hours[i+1] + (24.0 - hours[i])
		if (dt > 0.) :
			#Calcul de la tendance de la variable
			Tendance[j] = (Variable[i+1] - Variable[i]) / dt
		j+=1

	return Tendance


def Duration(df):
	"""
	Fonction qui calcule la duree de vie des cyclones pour des donnees journalieres (nombre de points), pour tous les cyclones du dataframe donné en argument.
	Elle met toutes ces informations sous forme d'un meme dataframe de colonnes :'ID','Duree'
	in : _df=dataframe des donnees
	out : _data=nouveau dataframe cree avec les informations calculees.
	"""

	nbCyclones = len(list(set(df.ID)))
	Duree = [0]*nbCyclones
	j=0
	g=df.groupby('ID')

	#Pour chaque cyclone :
	for id_cyclone in list(set(df.ID)):

		#Duree de vie = nombre de points (donnees journalieres)
		Duree[j]=g.get_group(id_cyclone).shape[0]
		j+=1

	#mise en forme
	ID = np.array(list(set(df.ID)))
	data= pd.DataFrame({'ID': ID, 'Duration of Cyclone': Duree})

	return data

#------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                                                   MISE EN FORME ET CONDENSATION DES INFORMATIONS CALCULEES
#
#------------------------------------------------------------------------------------------------------------------------------------------------

def Data(df):

	"""
	Fonction qui calcule la distance parcourue, la vitesse et la tendance de pression pour tous les cyclones du dataframe donne en argument.
	Elle met toutes ces informations sous forme d'un meme dataframe de colonnes :'ID','Distance','Vitesse','Tendance' , afin de synthetiser les informations et de mieux les visualiser.
	in : _df=dataframe des donnees
	out : _new_df=nouveau dataframe cree avec les informations calculees.
	"""

	g=df.groupby('ID')

	Data=pd.DataFrame({})

	#Pour tous les cyclones :
	for id_cyclone in list(set(df.ID)):

		groupe = g.get_group(id_cyclone)

		#Calcul de la distance entre les points
		distance = distancecyclone(groupe['Latitude'],groupe['Longitude'])
		#Calcul de la vitesse entre les points
		speed = velocitycyclone(groupe['Latitude'],groupe['Longitude'],groupe['Hour'],groupe['Day'])
		#Calcul de la tendance de pression entre les points
		tendency = tendencycyclone(groupe['Pressure'],groupe['Hour'],groupe['Day'])
		#Colonne des numeros de cyclones
		ID = np.array(groupe['ID'][0:-1])

		#mise en forme
		data1cyclone= pd.DataFrame({'ID': ID, 'Distance': distance, 'Speed': speed, 'Tendency': tendency})
		Data=pd.concat([Data,data1cyclone],axis=0,ignore_index=True,levels=None,names=None)
		

	return Data

def sumdistances(Data):
	"""
	Fonction qui calcule la distance totale parcourue, pour tous les cyclones du dataframe donne en argument.
	Elle somme toutes les distances calculees pour chaque cyclone.
	Elle met toutes ces informations sous forme d'un meme dataframe de colonnes :'ID','Distance'
	in : _df=dataframe des donnees
	out : _data=nouveau dataframe cree avec les informations calculees.
	"""
	g=Data.groupby('ID')

	nbCyclones = len(list(set(Data.ID)))
	distance = [0]*nbCyclones
	j=0

	#Pour chaque cyclone :
	for id_cyclone in list(set(Data.ID)):
		groupe = g.get_group(id_cyclone)

		#Somme de toutes les distances calculees pour un cyclone
		distance[j] = groupe['Distance'].sum()
		j+=1
	#mise en forme
	ID = np.array(list(set(Data.ID)))
	data= pd.DataFrame({'ID': ID, 'Total Distance': distance})
	return data

