import cv2
import numpy as np
from detectorVehiculo import DetectorVehiculos
from time import sleep
from config import *

cap = cv2.VideoCapture(ruta_video)
deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)
dV = DetectorVehiculos()

while True:
    ret, frame = cap.read()

    if not ret: break

    key = cv2.waitKey(5)
    if key == 27: break

    frame = cv2.resize(frame, (1280, 720))

    tiempo = float(1 / 180)
    sleep(tiempo)

    zona = frame[zona_y1:zona_y2, zona_x1:zona_x2]

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    desenfoque = cv2.GaussianBlur(gris, (3, 3), 5)
    img_sub = deteccion.apply(desenfoque)
    dilatacion = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilatacion, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    contornos, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (25, dV.posicion_linea), (1200, dV.posicion_linea), (255, 127, 0), 3)
    #Linea para video2.avi
    #cv2.line(frame, (0, dV.posicion_linea), (1280, dV.posicion_linea), (255, 127, 0), 3)
    for (i, c) in enumerate(contornos):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= dV.ancho_minimo) and (h >= dV.alto_minimo)
        if not validar_contorno: continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, str(dV.carros), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        centro = dV.obtener_centro(x, y, w, h)
        dV.detecciones.append(centro)
        cv2.circle(frame, centro, 4, (0, 0, 255), -1)

    dV.establecer_informacion(frame)
    dV.mostrar_informacion(zona, frame, dilatada)

cap.release()
cv2.destroyAllWindows()
