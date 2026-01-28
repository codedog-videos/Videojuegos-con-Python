import pygame as pg
import numpy as np

# parametros globales del juego
BG_V = 800 # tamano vertical de la ventana
BG_H = 700 # tamano horizontal de la ventana
IMGS_PATH = 'imgs' # path de imagenes
VEL_H = 10 # velocidad horizontal del juego


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

        # creamos los objetos del juego
        self.pajaro = Pajaro(x=150) # jugador


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
        
        # actualizamos los objetos del juego
        self.pajaro.actualizar() 
        

    # metodo para dibujar la escena en la pantalla
    def dibujar(self):
        # dibujamos fondos en pantalla
        self.pantalla.blit(self.fondo1, self.rect1)
        self.pantalla.blit(self.fondo2, self.rect2)

        # dibujamos objetos del juego
        self.pajaro.dibujar(self.pantalla) 



# clase Pajaro
class Pajaro:
    FREQ_ACT = 5 # frecuencia de actualizacion de sprites
    GRAVEDAD = 1.5 # gravedad UPDATE

    def __init__(self, x=100, y=350):
        # elegimos un color aleatoriamente
        ind_color = np.random.randint(1,9)
        
        # sprites del pajaro
        self.sprites = [pg.transform.scale(pg.image.load(f'{IMGS_PATH}/{img}.png'), (3*32, 3*21))
                        for img in [f'bird_{ind_color}1', f'bird_{ind_color}2', f'bird_{ind_color}3', f'bird_{ind_color}2']]

        # coordenadas rectangulares
        self.rect = self.sprites[0].get_rect()

        # actualizamos coordenadas
        self.rect.x = x
        self.rect.y = y

        # indice del sprite inicial
        self.sprint_ind = 0

        # contador de fotogramas
        self.cont = 0

        # velocidad vertical inicial UPDATE
        self.v_vel = 0


    # metodo para actualizar configuracion
    def actualizar(self):
        # incrementamos conteo de fotogramas
        self.cont += 1

        # verificamos si es necesario actualizar el sprite del jugador
        if self.cont % self.FREQ_ACT==0:
            # incrementamos el indice 
            self.sprint_ind += 1

            # reiniciamos indice de ser necesario
            if self.sprint_ind == 4:
                self.sprint_ind = 0
        
        # actualizamos la dinamica vertical UPDATE
        self.v_vel += self.GRAVEDAD 
        self.rect.y += self.v_vel

    
    # metodo para dibujar al jugador
    def dibujar(self, pantalla):
        pantalla.blit(self.sprites[self.sprint_ind], self.rect)



# inisializamos modulos
pg.init()

# creamos una pantalla
pantalla = pg.display.set_mode((BG_H, BG_V))

# creamos un reloj para controlar actualizaciones
reloj = pg.time.Clock()

# creacion de escena
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
        # evento: reiniciar
        if evento.type == pg.KEYDOWN and evento.key == pg.K_r:
            # creamos escena nueva
            escena = Escena(pantalla)
        
    # actualizamos configuraciones y dibujamos objetos en la escena
    escena.actualizar()
    escena.dibujar()
    pg.display.flip()

    # limitamos reloj a 30 fotogramas por segundo
    reloj.tick(30)

# cerramos la aplicacion si se sale del bucle
pg.quit()