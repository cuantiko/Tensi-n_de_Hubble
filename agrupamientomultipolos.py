#Importamos los paquetes
import sys, platform, os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import camb
import healpy as hp
import math
plt.style.use('seaborn-v0_8-white')
from camb import model, initialpower
#Imprimimos que se está usando CAMB
print('Using CAMB %s installed at %s'%(camb.__version__,os.path.dirname(camb.__file__)))

#Establecemos los parámetros cosmológicos
pars1 = camb.set_params(H0=73.2, ombh2=0.02237, omch2=0.122, mnu=0.06, omk=0, tau=0.056,  As=2.1e-9, ns=0.965, halofit_version='mead',lmax=3000)

pars2 = camb.set_params(H0=67.4, ombh2=0.02237, omch2=0.122, mnu=0.06, omk=0, tau=0.056, As=2.1e-9, ns=0.965, halofit_version='mead', lmax=3000)

#Calculamos los resultados
results1 = camb.get_results(pars1)
results2 = camb.get_results(pars2)

#Obtenemos el espectro
powers1 =results1.get_cmb_power_spectra(pars1, CMB_unit='muK')
powers2 =results2.get_cmb_power_spectra(pars2, CMB_unit='muK')

#Guardamos el espectro
totCL1 = powers1['total']
totCL2 = powers2['total']

#Leemos los archivos y guardamos las variables correspondientes:
A=np.loadtxt('TT_Planck_binned.txt', skiprows=1)
B=np.loadtxt('TT_Planck.txt', skiprows=1)
ls=A[:,0]
error_Planck=A[:,2]
ls_bin=[]

# Convertir valores a enteros y almacenarlos en las listas
for i in range(len(ls)):
    ls_bin.append(int(ls[i]))

#Trabajaremos con:
Y_local=totCL1[:,0]
Y_temprano=totCL2[:,0]

#Cómo el archivo de las observaciones Planck no tiene los Dl correspondientes a ls=0,1, los añadimos y le asignamos el valor de 0
Y_Planck=np.concatenate((np.array([0, 0]),B[:,1]))
#Nótese que esto no lo hicimos anterioremente porque en las simulaciones los valores empiezan en ls=0

#Hacemos el programa para binning (agrupamiento de multipolos):
V=[Y_Planck, Y_local, Y_temprano]
Dl=[]

for k in range(0,3):
    Y=V[k]
    z=[]
    for i in range(len(ls_bin)):
        posicion=ls_bin[i]
        suma1=0 
        suma2=0

        for j in range(posicion-15,posicion-1):
            suma1+=Y[j]
        for j in range(posicion+15,posicion+1,-1):
            if j>(len(Y)-1):
                suma2=0
            else:
                suma2+=Y[j]
        z.append((suma1+suma2)/30)
    Dl.append(z)


#Graficamos:
fig, ax = plt.subplots(figsize=(160,150), layout='constrained')
ax.errorbar(ls_bin, Dl[0], color='green', yerr=error_Planck, fmt='-o', ecolor='black', markersize=9, capsize=3, label='Observaciones Planck',zorder=1)
ax.plot(ls_bin,Dl[1],'o', color='blue',label='$H_0$ local',zorder=2)
ax.plot(ls_bin,Dl[2], 'o',color='red',label='$H_0$ temprano',zorder=3)
ax.set_xlabel('$\ell$',fontsize=20)
ax.set_ylabel('$D_l\;(\mu K^2)$', fontsize=20)
ax.legend(fontsize=20)
ax.set_title('Anisotropía en (TT) con agrupamiento de multipolos', fontsize=20)
ax.set_xlim([25,2521])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()

##########################################################################################
#Hallamos chi2:
Dl_obs=Dl[0]
Dl_local=Dl[1]
Dl_temprano=Dl[2]
chicuad_1=0
chi1=[]


for i in range(len(ls_bin)):
    chicuad_1+=((Dl_obs[i]-Dl_local[i])/(error_Planck[i]))**2
    chi1.append((((Dl_obs[i]-Dl_local[i])/(error_Planck[i])))/(np.sqrt(82)))

chicuad_2=0
chi2=[]

for i in range(len(ls_bin)):
    chicuad_2+=((Dl_obs[i]-Dl_temprano[i])/(error_Planck[i]))**2
    chi2.append((((Dl_obs[i]-Dl_temprano[i])/(error_Planck[i])))/(np.sqrt(82)))


print('El valor de chi2 local para H0 local es:', chicuad_1)

print('El valor de chi2 temprano para H0 temprano es:', chicuad_2)

print('El valor de chi2 reducido local para H0 local es:', chicuad_1/82)

print('El valor de chi2  reducido temprano para H0 temprano es:', chicuad_2/82)

#Cálculo de la función verosimilitud
chi1=np.concatenate((-np.array(chi1),np.array(chi1)))
chi1.sort()
chi2=np.concatenate((-np.array(chi2),np.array(chi2)))
chi2.sort()
Gauss_local=np.exp((-1/2)*np.array(chi1)**2)
Gauss_temprano=np.exp((-1/2)*np.array(chi2)**2)

# Creamos una figura y dos subplots, uno al lado del otro
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160, 150), layout='constrained')

# Crear la primera gráfica en el primer subplot (izquierda)
ax1.plot(chi1, Gauss_local, color='blue', linewidth=2, label='Función verosimilitud local')
ax1.set_title('Función verosimilitud local', fontsize=20)
ax1.set_xlabel('$\chi_{local}$', fontsize=20)
ax1.set_ylabel('$e^{-(1/2)\chi_{local}^2}$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# Crear la segunda gráfica en el segundo subplot (derecha)
ax2.plot(chi2, Gauss_temprano, color='red', linewidth=2,label='Función verosimilitud temprano')
ax2.set_title('Función verosimilitud temprano', fontsize=20)
ax2.set_xlabel('$\chi_{temprano}$', fontsize=20)
ax2.set_ylabel('$e^{-(1/2)\chi_{temprano}^2}$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# Mostrar las gráficas
#plt.tight_layout()
#plt.show()

# Establecer la resolución del mapa
#nside = 35  # Puedes ajustar este valor

# Generar mapas a partir del espectro de potencias
#alm1 = hp.synalm(Y_local, lmax=3*nside-1, new=True)
#temperature_map1 = hp.alm2map(alm1, nside=nside, verbose=False)

#alm2 = hp.synalm(Y_temprano, lmax=3*nside-1, new=True)
#temperature_map2 = hp.alm2map(alm2, nside=nside, verbose=False)
 # Graficar los mapas de temperatura utilizando healpy

#hp.mollview(temperature_map1, title="Mapa de Temperatura $H_0$ local", unit="muK",cmap='viridis')
#hp.graticule()
#plt.show()

#hp.mollview(temperature_map2, title="Mapa de Temperatura $H_0$ temprano", unit="muK", cmap='viridis')
#hp.graticule()
#plt.show()


# Parámetros del mapa
nside = 512

# Generar los mapas usando hp.synfast
mapa1 = hp.synfast(Y_local, nside, new=True)
mapa2=  hp.synfast(Y_temprano, nside, new=True)

#Mapa1:
# Mostrar el mapa utilizando hp.mollview
hp.mollview(mapa1, title="Mapa de Temperatura para $H_0$ local", unit="μK", cmap='viridis', min=-25000, max=25000)

# Añadir graticulado para mejorar la visualización y modificar tamaño del título y nombres de los ejes
hp.graticule()
plt.title("Mapa de Temperatura para $H_0$ local", fontsize=20)  # Cambiar el tamaño del título
plt.xlabel("Longitud", fontsize=20)  # Cambiar el tamaño de la etiqueta del eje X
# Mostrar el gráfico
plt.show()

#Mapa2:
hp.mollview(mapa2, title="Mapa de Temperatura para $H_0$ temprano", unit="μK", cmap='viridis', min=-25000, max=25000)
hp.graticule()
plt.title("Mapa de Temperatura para $H_0$ temprano", fontsize=20)  # Cambiar el tamaño del título
plt.xlabel("Longitud", fontsize=20)  # Cambiar el tamaño de la etiqueta del eje X
plt.show()
