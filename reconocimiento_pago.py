import cv2
import face_recognition
import pickle
import json
import time

def cargar_rostros():
    rostros = {}
    try:
        with open("caras_registradas.pkl", "rb") as f:
            while True:
                data = pickle.load(f)
                rostros.update(data)
    except EOFError:
        pass
    return rostros

def pagar(nombre, monto):
    import os
    print("📄 Ruta completa a cuentas.json:", os.path.abspath("cuentas.json"))
    with open("cuentas.json", "r") as f:
        contenido = f.read().strip()
        print("🔍 Contenido leído de cuentas.json:", repr(contenido))
        if not contenido:
            print("⚠️ El archivo está vacío en tiempo de ejecución.")
            return
        cuentas = json.loads(contenido)

    if nombre not in cuentas:
        print("❌ Cuenta no encontrada.")
        return

    if cuentas[nombre]["saldo"] < monto:
        print("❌ Fondos insuficientes.")
        return

    cuentas[nombre]["saldo"] -= monto

    import tempfile
    import shutil

    with tempfile.NamedTemporaryFile("w", delete=False, dir=".", suffix=".json") as tmp:
        json.dump(cuentas, tmp, indent=4)
        temp_name = tmp.name

    shutil.move(temp_name, "cuentas.json")

    print(f"✅ Pago de ${monto} realizado. Nuevo saldo: ${cuentas[nombre]['saldo']}")

def escanear_y_pagar(monto):
    rostros = cargar_rostros()

    video = cv2.VideoCapture(0)
    print("📷 Escaneando rostro... Presiona 'q' para salir.")

    rostro_reconocido = False
    nombre_reconocido = None

    while True:
        ret, frame = video.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ubicaciones = face_recognition.face_locations(rgb)
        codificaciones = face_recognition.face_encodings(rgb, ubicaciones)

        for codificacion in codificaciones:
            for nombre, encoding_guardado in rostros.items():
                match = face_recognition.compare_faces([encoding_guardado], codificacion)[0]
                if match:
                    print(f"✅ Rostro reconocido: {nombre}")
                    rostro_reconocido = True
                    nombre_reconocido = nombre
                    break
            if rostro_reconocido:
                break
        if rostro_reconocido:
            break

        cv2.imshow("Reconocimiento Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    time.sleep(0.5)

    if rostro_reconocido:
        pagar(nombre_reconocido, monto)
    return