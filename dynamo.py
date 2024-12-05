from dotenv import load_dotenv
import os
import boto3
import random
from datetime import datetime

data_list = []

latitude_min, latitude_max = -12.20, -11.90  # Latitudes de Lima
longitude_min, longitude_max = -77.10, -76.85  # Longitudes de Lima

for _ in range(1000):
    # Generar un DNI aleatorio de 8 dígitos
    dni = str(random.randint(10000000, 99999999))
    # Generar un timestamp o número aleatorio para 'dni-time'
    time_stamp = str(int(datetime.now().timestamp()))
    dni_time = f"{dni}-{time_stamp}"

    # Generar coordenadas aleatorias dentro de los límites de Lima Metropolitana
    latitude = f"{random.uniform(latitude_min, latitude_max):.6f}"
    longitude = f"{random.uniform(longitude_min, longitude_max):.6f}"

    data_item = {
        'dni-time': dni_time,
        'data': {
            'dni': dni,
            'latitude': latitude,
            'longitude': longitude
        }
    }
    data_list.append(data_item)

# Ejemplo de impresión de los primeros 5 objetos
for item in data_list[:5]:
    print(item)


load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('REGION_NAME'),
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY')
)

table = dynamodb.Table('cloud-chicho-dynamodb')

for item in data_list:
    table.put_item(Item=item)
    print(f"Item {item['dni-time']} agregado a la tabla")
