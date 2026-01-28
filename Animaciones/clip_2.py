import pygame as pg
import numpy as np

# parametros globales del juego
BG_V = 800 # tamano vertical de la ventana
BG_H = 700 # tamano horizontal de la ventana
IMGS_PATH = 'imgs' # path de imagenes UPDATE
VEL_H = 10 # velocidad horizontal del juego UPDATE


# UPDATE
# clase para controlar la escena del juego y sus objetos
class Escena:
    def __init__(self, pantalla):
        # pantalla para dibujar
        self.pantalla = pantalla 
        
        # fondos de pantalla y coordenadas verticales
        self.fondo1 = pg.image.load(f"{IMGS_PATH}/background.png").convert()
        self.rect1 = self.fondo1.get_rect()
        self.fondo2 = pg.image.load(f"{IMGS_PATH}/background.png").convert()
        self.rect2 = self.fondo2.get_rect()

        # ancho de la imagen de fondo
        self.img_h = self.fondo1.get_width()

        # colocamos segundo fondo despues del primero
        self.rect2.x = self.rect1.x + self.img_h


    # metodo para actualizar configuraciones
    def actualizar(self):
        # desplazamos imagenes de fondo
        self.rect1.x -= VEL_H
        self.rect2.x -= VEL_H

        # verificamos si las imagenes siguen en pantalla
        # de lo contrario colocamos la imagen fuera de pantalla al final de la otra
        if self.rect1.x < -self.img_h:
            self.rect1.x = self.rect2.x + self.img_h
        if self.rect2.x < -self.img_h:
            self.rect2.x = self.rect1.x + self.img_h
        

    # metodo para dibujar la escena en la pantalla
    def dibujar(self):
        # dibujamos fondos en pantalla
        self.pantalla.blit(self.fondo1, self.rect1)
        self.pantalla.blit(self.fondo2, self.rect2)



# inisializamos modulos
pg.init()

# creamos una pantalla
pantalla = pg.display.set_mode((BG_H, BG_V))

# creamos un reloj para controlar actualizaciones
reloj = pg.time.Clock()

# creacion de escena UPDATE
escena = Escena(pantalla)

# creamos variable para mantener el bluque del juego en ejecucion
aux_val = True

# bucle principal
while aux_val:
    # iteramos sobre eventos
    for evento in pg.event.get():
        # evento: cerrar
        if evento.type == pg.QUIT: 
            aux_val = False
        # evento: reiniciar UPDATE
        if evento.type == pg.KEYDOWN and evento.key == pg.K_r:
            # creamos escena nueva
            escena = Escena(pantalla)
        
    # actualizamos configuraciones y dibujamos objetos en la escena
    escena.actualizar() # UPDATE
    escena.dibujar() # UPDATE
    pg.display.flip()

    # limitamos reloj a 30 fotogramas por segundo
    reloj.tick(30)

# cerramos la aplicacion si se sale del bucle
pg.quit()