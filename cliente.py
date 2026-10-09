import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def mostrar_menu():
    print("\n" + "="*30)
    print("      GESTOR DE TAREAS API")
    print("="*30)
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Ver mis tareas (Requiere Login)")
    print("4. Salir")
    print("="*30)

def main():
    # sesión para persistir las cookies de autenticación
    client = requests.Session()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == '1':
            usuario = input("Ingresa tu nombre de usuario: ")
            password = input("Ingresa tu contraseña: ")
            payload = {"usuario": usuario, "contraseña": password}
            
            try:
                response = client.post(f"{BASE_URL}/registro", json=payload)
                print("\n[Respuesta del Servidor]:", response.json())
            except requests.exceptions.ConnectionError:
                print("\n[Error]: No se pudo conectar. ¿El servidor está encendido?")

        elif opcion == '2':
            usuario = input("Ingresa tu nombre de usuario: ")
            password = input("Ingresa tu contraseña: ")
            payload = {"usuario": usuario, "contraseña": password}
            
            try:
                response = client.post(f"{BASE_URL}/login", json=payload)
                print("\n[Respuesta del Servidor]:", response.json())
            except requests.exceptions.ConnectionError:
                print("\n[Error]: No se pudo conectar al servidor.")

        elif opcion == '3':
            try:
                response = client.get(f"{BASE_URL}/tareas")
                if response.status_code == 200:
                    print("\n[HTML Recibido del Servidor]:")
                    print("-" * 40)
                    print(response.text)
                    print("-" * 40)
                else:
                    
                    print("\n[Acceso Denegado]:", response.json())
            except requests.exceptions.ConnectionError:
                print("\n[Error]: No se pudo conectar al servidor.")

        elif opcion == '4':
            print("\nCerrando aplicación. ¡Hasta luego!")
            sys.exit(0)
            
        else:
            print("\nOpción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()