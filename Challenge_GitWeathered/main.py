import argparse
import requests
import json
import csv
import sys

# Definir la función para consultar la API del clima
def get_weather_data(location):
    API_KEY = 'TU_API_KEY'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Detectar errores en la solicitud
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Error en la solicitud: {err}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión: {e}")
        sys.exit(1)

# Función para imprimir en formato JSON
def print_json(data):
    print(json.dumps(data, indent=4))

# Función para imprimir en formato CSV
def print_csv(data):
    weather = data.get('weather', [{}])[0].get('description', 'N/A')
    temperature = data.get('main', {}).get('temp', 'N/A')
    fieldnames = ['Location', 'Weather', 'Temperature']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
        'Location': f"{data.get('name')}, {data.get('sys', {}).get('country')}",
        'Weather': weather,
        'Temperature': temperature
    })

# Función para imprimir en texto plano
def print_text(data):
    location = f"{data.get('name')}, {data.get('sys', {}).get('country')}"
    weather = data.get('weather', [{}])[0].get('description', 'N/A')
    temperature = data.get('main', {}).get('temp', 'N/A')
    print(f"Ubicación: {location}\nClima: {weather}\nTemperatura: {temperature}°C")

# Función principal para procesar los argumentos de la CLI
def main():
    parser = argparse.ArgumentParser(description="Aplicación CLI para obtener el clima")
    parser.add_argument('location', type=str, help='Nombre de la ciudad y país (ejemplo: "Asuncion, PY")')
    parser.add_argument('--format', type=str, choices=['json', 'csv', 'text'], default='text', help='Formato de salida (json, csv, text)')
    
    args = parser.parse_args()
    data = get_weather_data(args.location)

    if args.format == 'json':
        print_json(data)
    elif args.format == 'csv':
        print_csv(data)
    else:
        print_text(data)

if __name__ == '__main__':
    main()
