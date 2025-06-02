from registro_rostros import registrar_persona
from reconocimiento_pago import escanear_y_pagar

def menu():
    while True:
        print("\n=== SISTEMA DE PAGO CON ROSTRO ===")
        print("1. Registrar nuevo usuario")
        print("2. Realizar pago")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre completo: ")
            ruta = input("Ruta de imagen: ")  # Ej: imagenes/juan.jpg
            registrar_persona(nombre, ruta)
        elif opcion == "2":
            monto = float(input("Monto a pagar: $"))
            escanear_y_pagar(monto)
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()