from dotenv import load_dotenv
import os
import requests
from requests_oauthlib import OAuth1
import pandas as pd
import re
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Cargar variables de entorno desde el archivo .env
load_dotenv('apis.env')

# Obtener las claves de API de las variables de entorno
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Configuración de autenticación
auth = OAuth1(api_key, api_key_secret, access_token, access_token_secret)

# Hacer la solicitud a la API de Twitter
url = 'https://api.twitter.com/1.1/search/tweets.json'
params = {'q': 'Colapinto', 'lang': 'es', 'count': 100}
response = requests.get(url, auth=auth, params=params)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    tweets = response.json()['statuses']
    tweets_list = [tweet['text'] for tweet in tweets]

    # Crear un DataFrame con los tweets
    df = pd.DataFrame(tweets_list, columns=['tweet'])

    # Función para limpiar el texto de los tweets
    def limpiar_texto(texto):
        texto = re.sub(r'http\S+', '', texto)  # Eliminar enlaces
        texto = re.sub(r'@\w+', '', texto)    # Eliminar menciones
        texto = re.sub(r'#\w+', '', texto)    # Eliminar hashtags
        texto = texto.lower()                 # Transformar a minúsculas
        return texto

    df['tweet_limpio'] = df['tweet'].apply(limpiar_texto)

    # Función para analizar el sentimiento
    def analizar_sentimiento(texto):
        analisis = TextBlob(texto)
        if analisis.sentiment.polarity > 0:
            return 'positivo'
        elif analisis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negativo'

    df['sentimiento'] = df['tweet_limpio'].apply(analizar_sentimiento)

    # Visualización de datos usando Seaborn y Matplotlib
    sns.countplot(df['sentimiento'])
    plt.title('Distribución de sentimientos sobre Colapinto')
    plt.show()

    # Dashboard interactivo con Streamlit
    st.title('Análisis de Sentimientos de Tweets sobre Colapinto')
    st.write('Este dashboard muestra el análisis de sentimientos de los tweets recopilados.')

    # Mostrar el DataFrame
    st.write(df)

    # Gráfico de barras
    st.bar_chart(df['sentimiento'].value_counts())

else:
    print(f"Error al recopilar tweets: {response.status_code}")
