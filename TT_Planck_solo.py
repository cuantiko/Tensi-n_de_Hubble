import sys, platform, os  # Importa módulos del sistema operativo (no utilizados en este script)
import matplotlib
from matplotlib import pyplot as plt  # Importa funciones de matplotlib para la creación de gráficos
import numpy as np  # Importa numpy para el manejo de arrays y funciones matemáticas
import camb  # Importa CAMB, una biblioteca para cálculos cosmológicos (no utilizada en este script)
plt.style.use('seaborn-v0_8-white')  # Configura el estilo de los gráficos

# Carga los datos del archivo 'TT_Planck_binned.txt', omitiendo la primera fila
A = np.loadtxt('TT_Planck_binned.txt', skiprows=1)
X = A[:,0]  # Columna de datos en el eje X (multipolo l)
Y = A[:,1]  # Columna de datos en el eje Y (D_l)
lower_error = A[:,2]  # Error inferior
upper_error = A[:,3]  # Error superior
asymmetric_error = [lower_error, upper_error]  # Errores asimétricos para el gráfico

# Crea una figura y un eje con tamaño especificado y diseño ajustado
fig, ax = plt.subplots(figsize=(160, 150), layout='constrained')

# Grafica los datos con barras de error
ax.errorbar(X, Y, color='green', yerr=asymmetric_error, marker='o', capsize=2, ecolor='black')
ax.set_xlabel('$\ell$', fontsize=20)  # Etiqueta del eje X con formato LaTeX
ax.set_ylabel('$D_{\ell}\;(\mu K^2)$', fontsize=20)  # Etiqueta del eje Y con formato LaTeX
ax.set_title('Espectro angular de potencias en (TT)', fontsize=30)  # Título del gráfico
ax.set_xlim([50, 2500])  # Límites del eje X
plt.show()  # Muestra el gráfico
