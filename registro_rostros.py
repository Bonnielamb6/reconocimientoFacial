import face_recognition
import os
import pickle

def registrar_persona(nombre, ruta_imagen):
    imagen = face_recognition.load_image_file(ruta_imagen)
    codificaciones = face_recognition.face_encodings(imagen)

    if not codificaciones:
        print("❌ No se detectó rostro en la imagen.")
        return

    with open("caras_registradas.pkl", "ab") as f:
        pickle.dump({nombre: codificaciones[0]}, f)

    print(f"✅ Rostro de {nombre} registrado con éxito.")