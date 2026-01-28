import pygame as pg
import numpy as np

# parametros globales del juego
BG_V = 800 # tamano vertical de la ventana
BG_H = 700 # tamano horizontal de la ventana



# inisializamos modulos
pg.init()

# creamos una pantalla
pantalla = pg.display.set_mode((BG_H, BG_V))

# creamos un reloj para controlar actualizaciones
reloj = pg.time.Clock()

# creamos variable para mantener el bluque del juego en ejecucion
aux_val = True

# bucle principal
while aux_val:
    # iteramos sobre eventos
    for evento in pg.event.get():
        # evento: cerrar
        if evento.type == pg.QUIT: 
            aux_val = False
        
    # actualizamos configuraciones y dibujamos objetos en la escena
    pg.display.flip()

    # limitamos reloj a 30 fotogramas por segundo
    reloj.tick(30)

# cerramos la aplicacion si se sale del bucle
pg.quit()