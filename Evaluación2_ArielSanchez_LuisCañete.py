import urllib.parse
import requests

# Endpoints oficiales de Graphhopper
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

# Ingresa tu clave de API de Graphhopper dentro de las comillas
API_KEY = " TU-API-KEY-VA-AQUI "



def obtener_geolocalizacion(ubicacion, key):
    while ubicacion == "":
        ubicacion = input("Ingrese una ubicación válida: ")
    
    url = GEOCODE_URL + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": key, "locale": "es"})
    respuesta = requests.get(url)
    estado = respuesta.status_code
    datos_json = respuesta.json()
    
    if estado == 200 and len(datos_json["hits"]) != 0:
        lat = datos_json["hits"][0]["point"]["lat"]
        lng = datos_json["hits"][0]["point"]["lng"]
        nombre = datos_json["hits"][0]["name"]
        valor_pais = datos_json["hits"][0].get("country", "")
        valor_estado = datos_json["hits"][0].get("state", "")
        
        nueva_ubicacion = nombre
        if valor_estado:
            nueva_ubicacion += f", {valor_estado}"
        if valor_pais:
            nueva_ubicacion += f", {valor_pais}"
            
        print(f"URL de Geocodificación para {nueva_ubicacion} (Latitud: {lat:.2f}, Longitud: {lng:.2f}):\n{url}")
        return estado, lat, lng, nueva_ubicacion
    else:
        print(f"Estado de la API de Geocodificación: {estado}\nMensaje de error: {datos_json.get('message', 'Sin resultados')}")
        return estado, "null", "null", ubicacion

def main():
    while True:
        print("\n==================================================")
        print(" Sistema de Rutas y Navegación - Biblioteca Nacional ")
        print("==================================================")
        loc1 = input("Ingrese el punto de origen (o escriba 's' / 'salir' para terminar): ").strip()
        if loc1.lower() in ["s", "salir"]:
            print("Cerrando la aplicación. ¡Buen viaje!")
            break

        orig = obtener_geolocalizacion(loc1, API_KEY)
        if orig[0] != 200:
            continue

        loc2 = input("Ingrese el punto de destino (o escriba 's' / 'salir' para terminar): ").strip()
        if loc2.lower() in ["s", "salir"]:
            print("Cerrando la aplicación. ¡Buen viaje!")
            break

        dest = obtener_geolocalizacion(loc2, API_KEY)
        if dest[0] != 200:
            continue

        print("\n==================================================")
        print(f"Calculando itinerario desde: {orig[3]} hasta: {dest[3]}")
        print("==================================================")

        punto_orig = f"&point={orig[1]}%2C{orig[2]}"
        punto_dest = f"&point={dest[1]}%2C{dest[2]}"
        # Se incluye locale=es para obtener las instrucciones narradas en español nativo desde la API
        url_ruta = ROUTE_URL + urllib.parse.urlencode({"key": API_KEY, "locale": "es"}) + punto_orig + punto_dest
        
        resp_ruta = requests.get(url_ruta)
        estado_ruta = resp_ruta.status_code
        datos_ruta = resp_ruta.json()

        print(f"Estado de la API de Rutas: {estado_ruta}")
        
        if estado_ruta == 200:
            camino = datos_ruta["paths"][0]
            distancia_km = camino["distance"] / 1000
            distancia_millas = distancia_km / 1.60934
            duracion_segundos = camino["time"] / 1000
            duracion_minutos = duracion_segundos / 60
            duracion_horas = duracion_segundos / 3600

            print(f"Distancia total recorrida: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
            print(f"Tiempo estimado de viaje: {duracion_horas:.2f} horas ({duracion_minutos:.2f} minutos)")
            print("==================================================")
            print("Instrucciones paso a paso del viaje:")
            print("--------------------------------------------------")
            
            for maniobra in camino["instructions"]:
                texto = maniobra["text"]
                dist_paso = maniobra["distance"] / 1000
                print(f"• {texto} (durante {dist_paso:.2f} km)")
            print("==================================================")
        else:
            print(f"Error al calcular la ruta: {datos_ruta.get('message', 'Verifique los parámetros ingresados.')}")

if __name__ == "__main__":
    main()
