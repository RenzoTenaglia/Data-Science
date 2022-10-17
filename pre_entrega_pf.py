# -*- coding: utf-8 -*-
"""Pre-entrega PF

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rNUrh4q_2ryOza4u-mcamf-y6MXkZydN

# 1.Definicion de objetivo

Nuestro objetivo es en base a datos bancarios y de default estimar un modelo que permita predecir segun las caracteristicas de un invidio si este incurrira o no en un defaul crediticio.

# 2.Contexto comercial

Nos encontramos dentro del equipo de Data Science del banco "Amigos contra la inflacion". Su objetivo es dar resguardo a a los ahorradores argentinos frente a la inflacion,proporcionando plazos fijos con tasas de interes reales positivas. 
En base a los depositos  se otorgan prestamos al publico en general. Es importante conocer previamente las  caracteristicas del individio a quien se le orotoga el prestamo para reducir la probabilidad de defaul y poder cumplir con nuestros depositantes.

# 3.Problema comercial

Cuando  un individuo X solicita un prestamos. Si el banco no cuenta con informacion crediticia previa de este cliente se arriesga a otorgarle  dinero a un individuo que quiza no lo devuelva. 

En base a este problema planteamos la pregunta guia de este trabajo ¿ Que variables son relevantes para saber conocer previamente si el individuo incurre en difault o no? 
¿Que valores de estas variables clave separan a los clientes morosos de los no morosos?

# 4.Data Adquisicion

**Datos**


*Credit record: ID: Número de cliente (Cualitativa normal) Months Balance: El mes de los datos extraídos es el punto de partida, al revés, 0 es el mes actual, -1 es el mes anterior, etc. (Cuantitativa discreta) Status: Indica el estado del cliente (Cuantitativa discreta) 0 = 1-29 dias de atraso en el pago de la deuda 1= 30-59 días de atraso en el pago de la deuda 2=60-89 días de atraso en el pago de la deuda 3=90-119 días de atraso en el pago de la deuda 4=120-140 días de atraso en el pago de la deuda 5= Deudas atrasadas o incobrables (más de 150 días de atraso) C= pagado este mes X=no hay préstamo este mes

*Application record: Contiene las características del cliente ID: Número de cliente (Cuantitativa discreta) code gender: Género (Cualitativa Normal) Flag own car: ¿Hay un auto? (Cualitativa Normal) Flag own reality:¿Hay una propiedad? (Cualitativa Normal) cnt children: Número de hijos (Cuantitativa discreta) amt income total : Ingresos anuales (Cuantitativa continua) name income type: Categoría de ingresos (Cuantitativa Ordinal) name education type: Nivel de educación (Cuantitativa Ordinal) name family status: Estado civil (Cualitativa Normal) name housing type: Modo de vivir (Cualitativa Normal) Days Birthday: Días para el cumpleaños. Cuenta hacia atrás, -1 significa ayer. (Cuantitativa continua) Flag Móvil: ¿Hay algun telefono movil? (Cualitativa Normal) Flag_email: ¿Tiene email? (Cualitativa Normal) Occupation Type: Ocupación (Cuantitativa Ordinal) cnt fam members: Tamaño de la familia (Cuantitativa discreta)
"""

pip install pyxlsb

import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
import numpy as np

url_credito= "https://github.com/RenzoTenaglia/Data-Science/blob/main/credit_record.csv?raw=true"
url_caract="https://github.com/RenzoTenaglia/Data-Science/blob/main/caracteristicas%20binario.xlsb?raw=true"
caract=pd.read_excel(url_caract)
credito=pd.read_csv(url_credito)
data=pd.merge(caract,credito, how= "inner")

data.head()

#Nuesta data esta contaminada por datos duplicados procedemos a eliminarlos 
data=data.drop_duplicates("ID")

"""  # 5.EDA ( Analisis exploratorio de datos)**  


"""

import seaborn as sns 
import matplotlib.pyplot as plt
import numpy as np

data.isnull().sum()

data["OCCUPATION_TYPE"]=data["OCCUPATION_TYPE"].fillna("Sin ocupacion")

cuantitativa=["CNT_CHILDREN","AMT_INCOME_TOTAL","DAYS_EMPLOYED","CNT_FAM_MEMBERS"]
cualitativa=["NAME_INCOME_TYPE","NAME_EDUCATION_TYPE","NAME_FAMILY_STATUS","NAME_HOUSING_TYPE","OCCUPATION_TYPE"]
bolaneas=["CODE_GENDER","FLAG_OWN_CAR","FLAG_OWN_REALTY","FLAG_MOBIL","FLAG_WORK_PHONE","FLAG_PHONE","FLAG_EMAIL"]

sns.set_theme(style="darkgrid")

#Cualitativas
fig, axes = plt.subplots(2, 3, figsize=(30,20))

sns.kdeplot(data=data,x="CNT_CHILDREN",hue="STATUS",ax = axes[0,0],title="Densidad del numero de hijos",xlabel="Cantidad de hijos")
plt.xlabel("Cantidad de hijos")
plt.title("Densidad del numero de hijos")

sns.kdeplot(data=data,x="AMT_INCOME_TOTAL",hue="STATUS", ax = axes[0,1])
plt.xlabel("Ingreso")
plt.title("Densidad del ingreso")

sns.kdeplot(data=data,x="DAYS_EMPLOYED",hue="STATUS", ax = axes[0,2])
plt.xlabel("Dias empleados ")
plt.title("Densidad de los dias empleados ")

sns.scatterplot(data=data,x="CNT_CHILDREN",y="AMT_INCOME_TOTAL",hue="STATUS",ax = axes[1,0])
plt.xlabel("Cantidad de hijos")
plt.ylabel("Ingreso")
plt.title("Ingreso vs cantidad de hijos")
sns.scatterplot(data=data,x="CNT_CHILDREN",y="DAYS_EMPLOYED",hue="STATUS",ax = axes[1,1])
plt.xlabel("Cantidad de hijos")
plt.ylabel("Dias empleados")
plt.title("Cantidad de hijos vs dias empleados")
sns.scatterplot(data=data,x="DAYS_EMPLOYED",y="AMT_INCOME_TOTAL",hue="STATUS",ax = axes[1,2])
plt.xlabel("Dias empleado")
plt.ylabel("Ingreso")
plt.title("Ingreso vs dias empleados")

plt.show()

#Cuantitativas
fig, axes = plt.subplots(2, 2, figsize=(30,20))

sns.countplot(x = 'NAME_INCOME_TYPE', palette='rocket',order = data['NAME_INCOME_TYPE'].value_counts().index, data = data, ax = axes[0,0])
plt.xlabel("Tipo de ingreso")
sns.countplot(x = 'NAME_EDUCATION_TYPE', palette='Set2',order = data['NAME_EDUCATION_TYPE'].value_counts().index, data = data, ax = axes[0,1])
plt.xlabel("Nivel de educacion")
sns.countplot(x = 'NAME_FAMILY_STATUS', palette="Paired",order = data['NAME_FAMILY_STATUS'].value_counts().index, data = data, ax = axes[1,0])
plt.xlabel("Estado familiar")
sns.countplot(x = 'NAME_HOUSING_TYPE', palette="crest",  order = data['NAME_HOUSING_TYPE'].value_counts().index,data = data, ax = axes[1,1])
plt.xlabel("Donde viven")

plt.figure(figsize=(30,5))
sns.countplot(x = 'OCCUPATION_TYPE', palette="BrBG",order = data['OCCUPATION_TYPE'].value_counts().index, data = data)

fig, axes = plt.subplots(2, 3, figsize=(25,15))

sns.countplot(x = 'CODE_GENDER', palette='rocket', data = data, ax = axes[0,0],hue="STATUS")
sns.countplot(x = 'FLAG_OWN_CAR', palette='Set2', data = data, ax = axes[0,1],hue="STATUS")
sns.countplot(x = 'FLAG_OWN_REALTY', palette="Paired", data = data, ax = axes[0,2],hue="STATUS")
sns.countplot(x = 'FLAG_MOBIL', palette="crest", data = data, ax = axes[1,0],hue="STATUS")
sns.countplot(x = 'FLAG_PHONE', palette="BrBG", data = data, ax = axes[1,1],hue="STATUS")
sns.countplot(x = 'FLAG_EMAIL', palette="BrBG", data = data, ax = axes[1,2],hue="STATUS")

""" # 6 . Data Wrangling """

data=data.replace(["Y","N"],[1,0])
data=data.replace(["M","F"],[1,0])
data["OCCUPATION_TYPE"]=data["OCCUPATION_TYPE"].fillna("Sin ocupacion")

#One hot coding 
data["SECUNDARIA"]=np.where(data["NAME_EDUCATION_TYPE"] == "Secondary / secondary special",1,0 )
data["PRIMARIA"]=np.where(data["NAME_EDUCATION_TYPE"] == "Lower secondary",1,0 )
data["SUPERIOR"]=np.where(data["NAME_EDUCATION_TYPE"] == "Higher education",1,0 )
data["SUPERIOR_INCOMPLETO"]=np.where(data["NAME_EDUCATION_TYPE"] == "Incomplete higher",1,0 )
data["ACADEMICO"]=np.where(data["NAME_EDUCATION_TYPE"] == "Academic degree",1,0 )

#Label encoder
from sklearn.preprocessing import LabelEncoder

labelencoder = LabelEncoder()
data["TRABAJO"]=labelencoder.fit_transform(data["NAME_INCOME_TYPE"])
data["TIPO_DE_TRABAJO"]=labelencoder.fit_transform(data["OCCUPATION_TYPE"])
data["SITUACION_CIVIL"]=labelencoder.fit_transform(data["NAME_FAMILY_STATUS"])
data["DONDE_VIVEN"]=labelencoder.fit_transform(data["NAME_HOUSING_TYPE"])
data["SITUACION"]=labelencoder.fit_transform(data["STATUS"])

#Creamos un nuevo data frame que contiene solo las variables numericas
df=data.drop(["NAME_INCOME_TYPE","OCCUPATION_TYPE","NAME_FAMILY_STATUS","NAME_HOUSING_TYPE","NAME_EDUCATION_TYPE","STATUS"],axis=1)

plt.figure(figsize=(5,5))
df.SITUACION.plot(kind="density",color="ko")
plt.xlabel("Situacion")
plt.title("Densidad de Situacion")

#Hacer scatterplot entre ingreso y situacion

import matplotlib.pyplot as plt
import numpy as np

fig = pl.figure()
ax = fig.add_subplot(111)

#plt.figure(figsize=(5,5))
df.SITUACION.plot(kind="density")
plt.xlabel("Situacion")
plt.title("Densidad de Situacion")
ax.set_xlim([0, 7])

#Hacer scatterplot entre ingreso y situacion

import matplotlib.pyplot as pl
from matplotlib.ticker import ScalarFormatter


fig = pl.figure()
ax = fig.add_subplot(111)

df.SITUACION.plot(kind="density")

plt.title("Densidad de Situacion en escala logaritmica")
ax.plot(color='red', lw=2)
ax.set_yscale('log')
ax.set_yticks([0,0.001, 0.005, 0.025,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7])
ax.get_yaxis().set_major_formatter(ScalarFormatter())
ax.set_ylim([0.0001, 0.8])
ax.set_xlim([0, 7])

import matplotlib.pyplot as plt
import numpy as np

fig = pl.figure()
ax = fig.add_subplot(111)

#plt.figure(figsize=(5,5))
df.SITUACION.plot(kind="density")
plt.xlabel("Situacion")
plt.title("Densidad de Situacion")
ax.set_xlim([0, 7])

#Hacer scatterplot entre ingreso y situacion

import matplotlib.pyplot as pl
from matplotlib.ticker import ScalarFormatter


fig = pl.figure()
ax = fig.add_subplot(111)

df.SITUACION.plot(kind="density")

plt.title("Densidad de Situacion en escala logaritmica")
ax.plot(color='red', lw=2)
ax.set_yscale('log')
ax.set_yticks([0,0.001, 0.005, 0.025,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7])
ax.get_yaxis().set_major_formatter(ScalarFormatter())
ax.set_ylim([0.0001, 0.8])
ax.set_xlim([0, 7])

alpha = df["SITUACION"]
beta=[]

for x in alpha:
  if x > 1 and x <6:
    beta.append(x)

  else:
    pass

print(beta)

fig = pl.figure()
ax = fig.add_subplot(111)

gamma = pd.DataFrame (beta, columns = ['beta'])

gamma.beta.plot(kind="density")

plt.title("Densidad de Situacion en el rango 2 hasta 5")
ax.set_xticks([2, 3, 4, 5])
ax.plot(color='red', lw=2)
ax.set_xlim([2, 5])

"""# 7.Seleccion del algoritmo

Utilizaremos un algoritmo de  aprendizaje  supervisado. A pesar de que nuestra variable Target es de tipo numerica, cada numero representa una categoria por lo que nos parece correcto usar un algortimo de clasificacion para resolver nuestro problema de clasificacion multiclase.
"""

columnas=list(df.columns)
columnas

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler

#knn
X= df.drop(["ID","DAYS_BIRTH","MONTHS_BALANCE","SITUACION","FLAG_MOBIL"],axis=1)
y= df.SITUACION

scaler=MinMaxScaler()
X_test , X_train, y_test, y_train = train_test_split(X,y,test_size=0.3,random_state=44)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

n=10

knn=KNeighborsClassifier(n)
model=knn.fit(X_train,y_train)
pred=model.predict(X_test)

print(metrics.classification_report(y_test,pred))

from sklearn import tree

X= df.drop(["ID","DAYS_BIRTH","MONTHS_BALANCE","SITUACION","FLAG_MOBIL"],axis=1)
y= df.SITUACION

X_test , X_train, y_test, y_train = train_test_split(X,y,test_size=0.3,random_state=44)

clf=DecisionTreeClassifier(random_state=0,max_depth= 50)
model=clf.fit(X_train,y_train)
pred=model.predict(X_test)

print(metrics.classification_report(y_test,pred))

X=df.drop(["SITUACION","MONTHS_BALANCE","DAYS_BIRTH","ID","FLAG_MOBIL"],axis=1)
y=df.SITUACION

X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.3,random_state=44)

#clf=DecisionTreeClassifier(max_depth=30,random_state=87,min_samples_leaf=15)
clf=RandomForestClassifier(random_state=0)
model=clf.fit(X_train,y_train)
predictions1 = model.predict(X_test)



print(metrics.classification_report(y_test,predictions1))

import time 

variables=X.columns
start_time=time.time()
importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
elapsed_time = time.time() - start_time

forest_importances = pd.Series(importances, index=variables)

fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=std, ax=ax)
ax.set_title("Feature importances using MDI")
ax.set_ylabel("Mean decrease in impurity")
fig.tight_layout()