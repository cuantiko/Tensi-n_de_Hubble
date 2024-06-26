#Importamos los paquetes
import sys, platform, os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import camb
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

#Usamos un método para obtener el espectro
powers1 =results1.get_cmb_power_spectra(pars1, CMB_unit='muK')
powers2 =results2.get_cmb_power_spectra(pars2, CMB_unit='muK')

#Guardamos el espectro con efecto lente (total) 
totCL1 = powers1['total']
totCL2 = powers2['total']

#Generamos el eje de abcisas de los Dl simulados
ls = np.arange(totCL1.shape[0])

#Leemos el archivo de observaciones Planck
A=np.loadtxt('TT_Planck.txt', skiprows=1)
X=A[:,0]
Y=A[:,1]
lower_error = A[:,2]
upper_error = A[:,3]

#Representamos todas las funciones
fig, ax = plt.subplots(figsize=(160,150), layout='constrained')

ax.plot(X,Y+upper_error, alpha=0.9, color='black')
ax.plot(X,Y-lower_error, alpha=0.9, color='black')
ax.plot(X,Y, color='green', alpha=0.8, label='Observaciones Planck')
ax.plot(ls,totCL1[:,0], color='deepskyblue', label='$H_0$ local', linewidth=3)
ax.plot(ls,totCL2[:,0], color='red', label='$H_0$ temprano',linewidth=3)
ax.set_xlabel('$\ell$', fontsize=20)
ax.set_ylabel('$D_{\ell}\;(\mu K^2)$',fontsize=20)
ax.legend(fontsize=20)
ax.set_title('Anisotropía en (TT) para $H_0$ simulada junto con observaciones Planck', fontsize=20)
ax.set_xlim([1,2500])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()
