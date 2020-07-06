'''
Tarea 4
Estudiante: Emmanuel Chavarría Solís
Carnet: B51977
Correo: leuname592@hotmail.com
'''
# Se importan las librerias a utilizar
import numpy as np
import pandas as pd 
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt



'''
 1. Crear un esquema de modulación BPSK para los bits presentados.
'''
# Lectura de datos
df = pd.read_csv("bits10k.csv", header=None)
df = df.to_numpy()

# Frecuencia de operación
f = 5000 # 5 kHz

# Duración del período de cada onda
T = 1/f 

# Número de puntos de muestreo por período
p = 50 

# Puntos de muestreo para cada período
tp = np.linspace(0, T, p)

# Creación de la forma de onda
seno = np.sin(2*np.pi * f * tp)

# Visualización de la forma de onda de la portadora
plt.plot(tp*100, seno)
plt.ylabel('Amplitud')
plt.xlabel('Tiempo (ms)')
plt.title('Modulación')
plt.savefig('onda.png')

# Numero de datos
N=len(df)
# Frecuencia de muestreo
fs = p/T # 50 kHz

# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, N*T, N*p)

# Vector que va a contener la señal
senal = np.zeros(N*p)

# Modulación BPSK
for k, b in enumerate(df):
  senal[k*p:(k+1)*p] = (2*b-1) * seno
  
# Visualización de los primeros bits modulados
pb = 5
plt.figure()
plt.plot(senal[0:pb*p])
plt.xlabel('Puntos de muestreo')
plt.ylabel('Amplitud')
plt.title('Señal pura portadora de la información')
plt.savefig('PrimerosBits.png')



'''
2. Calcular la potencia promedio de la señal modulada generada
'''

# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)

# Imprimir Valores
print('\nTarea 4')
print('Estudiante: Emmanuel Chavarría Solís')
print('Carnet: B51977\n')
print("La potencia promedio es de: ", Ps)



'''
3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano).
'''

# Relación señal-a-ruido deseada en forma de vector
SNR = range(-11,-5)
sigma,ruido=[0]*6,[0]*6


for i in range(0,6):
    # Potencia del ruido para SNR y potencia de la señal dadas
    Pn = Ps / (10**(SNR[i] / 10))
    
    # Desviación estándar del ruido
    sigma[i] = np.sqrt(Pn)
    
    # Crear ruido sigma
    ruido[i] = np.random.normal(0, sigma[i], senal.shape)
    
# "El canal": señal recibida después del ruido para 6 valores de SNR
Rx6 = senal + ruido[0]
Rx5 = senal + ruido[1]
Rx4 = senal + ruido[2]
Rx3 = senal + ruido[3]
Rx2 = senal + ruido[4]
Rx1 = senal + ruido[5]
# Visualización de los pirmeros bits recibidos para la señal más ruidosa
pb = 5
plt.figure()
plt.plot(Rx6[0:pb*p])
plt.xlabel('Puntos de muestreo')
plt.ylabel('Amplitud')
plt.title('Señal con el ruido AWGN')
plt.savefig('PrimerosBitsRuidosos.png')



'''
4. Graficar la densidad espectral de potencia de la señal con el método de
 Welch (SciPy), antes y después del canal ruidoso.
'''

plt.figure()
fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.semilogy(fw , PSD)
plt.ylabel('Densidad de Potencia')
plt.xlabel('Frecuencia (Hz)')
plt.title('Densidad espectral de potencia antes del Ruido')
plt.savefig('PSDantes.png')

# Canal más ruidoso visualizado
plt.figure()
fw, PSD = signal.welch(Rx6, fs, nperseg=1024)
plt.semilogy(fw , PSD)
plt.ylabel('Densidad de Potencia')
plt.xlabel('Frecuencia (Hz)')
plt.title('Densidad espectral de potencia con el Ruido')
plt.savefig('PSDdespues.png')

'''
5. Demodular y decodificar la señal.
'''

# Decodificación de la señal por detección de energía
def Decodificar (ruidosa):
    # Inicialización del vector de bits recibidos
    bitsRx = np.zeros(df.shape)
    for k in range(N):
      E = np.sum(ruidosa[k*p:(k+1)*p] * seno)
      if E > 0:
        bitsRx[k] = 1
      else:
        bitsRx[k] = 0
    return bitsRx
decodificada1=Decodificar(Rx1)
decodificada2=Decodificar(Rx2)
decodificada3=Decodificar(Rx3)
decodificada4=Decodificar(Rx4)
decodificada5=Decodificar(Rx5)
decodificada6=Decodificar(Rx6)


# 5.b Hacer un conteo de BER para cada nivel SNR.

BER=[0]*6
# Contar errores
BER[5] = np.sum(np.abs(df - decodificada1))/N
BER[4] = np.sum(np.abs(df - decodificada2))/N
BER[3] = np.sum(np.abs(df - decodificada3))/N
BER[2] = np.sum(np.abs(df - decodificada4))/N
BER[1] = np.sum(np.abs(df - decodificada5))/N
BER[0] = np.sum(np.abs(df - decodificada6))/N

# Tasa de error de bits (BER, bit error rate)
print("\nLa tasa de errores es:", BER[5]," para un canal con un ruido de ",SNR[5],"dB")
print("La tasa de errores es:", BER[4]," para un canal con un ruido de ",SNR[4],"dB")
print("La tasa de errores es:", BER[3]," para un canal con un ruido de ",SNR[3],"dB")
print("La tasa de errores es:", BER[2]," para un canal con un ruido de ",SNR[2],"dB")
print("La tasa de errores es:", BER[1]," para un canal con un ruido de ",SNR[1],"dB")
print("La tasa de errores es:", BER[0]," para un canal con un ruido de ",SNR[0],"dB")



'''
6. Graficar BER versus SNR.
'''

plt.figure()
plt.semilogy(SNR , BER)
plt.xlabel('SNR (dB)')
plt.ylabel('BER')
plt.title('Tasa de errores en función del SNR')
plt.savefig('BERvsSNR.png')
