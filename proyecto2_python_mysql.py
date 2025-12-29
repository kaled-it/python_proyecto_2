import requests
from tabulate import tabulate
import mysql.connector

URL = 'https://restcountries.com/v3.1/region/America'

response = requests.get(URL)

if response.status_code == 200:
    print('Conexion API exitosa')
    data = response.json()
    rows = []
    for dic_pais in data: #RESTCOUNTRIES da el total de paises, no agrupados en un un diccionario como "results" de randomuser.
        nombre = dic_pais['name']['official']
        capital =  dic_pais['capital'][0]
        region = dic_pais['region']
        population = dic_pais['population']
        rows.append([nombre, capital, region, population])
        
    headers = ['Nombre','Capital','Región','Población']
    print(tabulate(rows,headers,tablefmt='grid'))
    
    connection = mysql.connector.connect(        #CONECTA A DB
        host = 'localhost',
        user = 'root',
        password = 'root',  #ES 'ROOT', NO 'ROOT2025'"
        database = 'db_g6'
    )
    if connection.is_connected():
        cursor = connection.cursor()
        
        #cursor.execute("DROP TABLE IF EXISTS paises") #descomentar para eliminar tabla existente
        
        cursor.execute(
            """
            CREATE TABLE IF NOT exists paises(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(225) not null,
            capital VARCHAR(225) not null,
            region varchar(225),
            population INT
            );
            """
        )

        for paises in rows:   #INSERT DATOS
            cursor.execute(
                """
                insert into paises (nombre, capital, region, population)
                values(%s,%s,%s,%s)
                """,
                paises
            )
        connection.commit()
        connection.close()
        print('Registros importados a la BD')
    else:
        print('Error al interntar conectarse a la BD')
else:
    print(f'error{response.status_code}')