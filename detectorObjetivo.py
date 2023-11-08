import cv2
from config import *

class DetectorObjetivo:
    def __init__(self):
        self.ancho_minimo = ancho_minimo
        self.alto_minimo = alto_minimo
        self.offset = offset
        self.posicion_linea = posicion_linea
        self.detecciones = []
        self.carros = 0

    def obtener_centro(self, x, y, ancho, alto):
        x1 = ancho // 2
        y1 = alto // 2
        cx = x + x1
        cy = y + y1
        return cx, cy

    def establecer_informacion(self, frame):
        for (x, y) in self.detecciones:
            if (self.posicion_linea + self.offset) > y > (self.posicion_linea - self.offset):
                self.carros += 1
                cv2.line(frame, (25, self.posicion_linea), (1200, self.posicion_linea), (0, 127, 255), 3)
                #cv2.line(frame, (0, self.posicion_linea), (1280, self.posicion_linea), (0, 127, 255), 3)
                self.detecciones.remove((x, y))
                print("Objetivos detectados hasta el momento: " + str(self.carros))

    def mostrar_informacion(self, zona, frame, mascara):
        cv2.imshow("Máscara", mascara)
        cv2.imshow("Carretera", frame)
        cv2.imshow("Zona de interés", zona)
