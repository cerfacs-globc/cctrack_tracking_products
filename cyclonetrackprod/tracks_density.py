
import numpy as np
import matplotlib.pyplot as plt

def density(tab_lon,tab_lat,domain):         #Rajouter une dimension temps
    N_ech=len(tab_lat)
    n_lon=int((domain['lon_max']-domain['lon_min'])/domain['resolution']) #+1 ? Reste de la div.
    n_lat=int((domain['lat_max']-domain['lat_min'])/domain['resolution'])
    pt_lon=np.array([domain['lon_min'] + k*domain['resolution'] for k in range (0,n_lon)])
    pt_lat=np.array([domain['lat_min'] + k*domain['resolution'] for k in range (0,n_lat)])
    flag=np.ones((n_lon,n_lat))
    rden=np.zeros((n_lon,n_lat))
    rfin=np.zeros((n_lon,n_lat))
    rall=np.zeros((n_lon,n_lat))
    rgen=np.zeros((n_lon,n_lat))
    for compteur_point in range (0,N_ech):
        if compteur_point % 100 == 0:
            print("Number of tracks processed:" ,compteur_point)
        longitude_cyclone=tab_lon[compteur_point]
        latitude_cyclone=tab_lat[compteur_point]
        ilon=nearest_indice(longitude_cyclone,pt_lon,n_lon)
        jlat=nearest_indice(latitude_cyclone,pt_lat,n_lat)
        for j in range (jlat-domain['ires'],jlat+domain['ires']):
	    #attention i et j doivent etre compris entre 1 et nlat (respectivement nlon)
            for i in range (ilon-domain['ires'],ilon+domain['ires']):
                test1= ((i>=1) and (i<n_lon))
                test2= ((j>=1) and (j<n_lat))
                if (test1==True) and (test2==True):
                    zdist=pdist(pt_lon[ilon],pt_lat[jlat],pt_lon[i],pt_lat[j])
                    # calcul de la distance en coordonnees polaires
                    if zdist<domain['zradius']:
                        #si le point du cyclone est inferieur au rayon de resolution , on effectue :
                        if compteur_point == 1:
                            rgen[i,j]=rgen[i,j]+gauss_kernel((3.1415*domain['zradius']**2.)**-1,zdist,domain['zradius'])
                            #on stocke la valeur dans le tableau de densite initial 
                            #rgen[i,j]=rgen[i,j]+gauss_kernel(1,zdist,domain['zradius'])
                        elif compteur_point == N_ech :
                            #s'il s'agit du dernier indice, alors:
                            rfin[i,j]=rfin[i,j]+gauss_kernel((3.1415*domain['zradius']**2.)**-1,zdist,domain['zradius'])
                            #On stocke la valeur dans le tableau de densite final
                            #rfin[i,j]=rfin[i,j]+gauss_kernel(1,zdist,domain['zradius'])  
                        rden[i,j]=rden[i,j]+flag[i,j]*gauss_kernel((3.1415*domain['zradius']**2.)**-1,zdist,domain['zradius'])
                        #Au final c'est le tableau de densite "sans bords" qui est incremente
                        rall[i,j]=rall[i,j]+gauss_kernel((3.1415*domain['zradius']**2.)**-1,zdist,domain['zradius'])                
                        #rden[i,j]=rden[i,j]+flag[i,j]*gauss_kernel(1,zdist,domain['zradius']) 
                        #rall[i,j]=rall[i,j]+gauss_kernel(1,zdist,domain['zradius'])
                    flag[i,j]=0
    print("Density processing OK")
    return rall


def nearest_indice(xind,xtab,n):
	xmin=1.e+10
	for i in range (1,n):
		xx=abs(xind-xtab[i])
		if (xx< xmin):
			xmin=xx
			nearest_indice=i
	return nearest_indice

    
def pdist(po1,pa1,po2,pa2):
	R=6.371e+6
	pi=4*np.arctan(1.)
	conv=2.*np.pi/360.
	pro1=conv*po1
	pra1=conv*pa1
	pro2=conv*po2
	pra2=conv*pa2
	if ((pro1==pro2) and (pra1==pra2)):
		pdist=0.
	else:
		pdist=np.arccos(np.cos(pra1)*np.cos(pra2)*np.cos(pro2-pro1)+np.sin(pra1)*np.sin(pra2))*R
	return pdist



def gauss_kernel(x,pdist,sigma):
	ratio=pdist/sigma
	wght=np.exp(-0.5*ratio**2)
	Gauss_kernel=x*wght
	return Gauss_kernel

def densitymatrix(df,domain):
    """
    Fonction qui rajoute des points entre 2 points consecutifs de la trajectoire d'un cyclone, pour tous les cyclones.
    Elle a pour effet de lisser les densites de trajectoires.
    in : _df=dataframe des points des trajcetoires des cyclones; 
    lat_min,lon_max,lon_min = domaine de la grille, domain['zradius'] = rayon de detection, resolution = resolution de la grille
    out : _matrice de densite
    """

    tab_lat=[]
    tab_lon=[]
    lontemp,lattemp=[],[]

    #Pour chaque cyclone :
    h=df.groupby('ID')
    for id_cyclone in list(set(df.ID)) :
        Latitudes = h.get_group(id_cyclone)['Latitude']
        Longitudes = h.get_group(id_cyclone)['Longitude']

        #rajout de points entre 2 points consecutifs d'une meme trajectoire
        for x in Latitudes.index[0:-1]:
            lattemp=np.linspace(Latitudes[x],Latitudes[x+1], num=2, endpoint=True)
            tab_lat=np.concatenate((tab_lat,lattemp))
        for y in Longitudes.index[0:-1]:
            lontemp=np.linspace(Longitudes[y],Longitudes[y+1], num=2, endpoint=True)
            tab_lon=np.concatenate((tab_lon,lontemp))

    #creation de la matrice de densite a partir de ces trajectoires auxquelles on a rajoute des points
    matrice_densite=density(tab_lon,tab_lat,domain)
    matrice_densite=np.transpose(matrice_densite)

    return matrice_densite

