import os
import pandas as pd


print(os.getcwd())

os.chdir(r'C:\Users\Cristian\Documents')

#Imprimo serie#

serie = pd.Series([10, 20, 30, 40])
print(serie)

#Imprimo matriz#

data = {
    'Nombre': ['Juan', 'Ana', 'Pedro'],
    'Edad': [25, 30, 35],
    'Ciudad': ['Madrid', 'Barcelona', 'Sevilla']
}
df = pd.DataFrame(data)


# Guardar el archivo CSV
df.to_csv('archivo.csv', index=False)

# Leer el archivo CSV
df_leido = pd.read_csv('archivo.csv')
print(df_leido)


print(df)

print(df.info())

print(df[df['Edad'] > 30])

print(df.groupby('Ciudad')['Edad'].mean())

df['Salario'] = [30000, 40000, 50000]

print(df.groupby('Nombre')['Salario'].mean())

print(df.head())

#Leo el archivo .csv#


df = pd.read_csv('archivo.csv')


#df = pd.read_excel('archivo.xlsx')

