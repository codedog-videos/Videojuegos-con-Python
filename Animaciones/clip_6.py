import pygame as pg
import numpy as np

# parametros globales del juego
BG_V = 800 # tamano vertical de la ventana
BG_H = 700 # tamano horizontal de la ventana
IMGS_PATH = 'imgs' # path de imagenes
VEL_H = 10 # velocidad horizontal del juego
FREQ_TUBERIAS = 50 # numero de fotogramas para generar una nueva tuberia UPDATE


# clase para controlar la escena del juego y sus objetos
class Escena:
    def __init__(self, pantalla):
        # pantalla para dibujar
        self.pantalla = pantalla 

        # contador de fotogramas UPDATE
        self.fotogramas = 0
        
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
        #self.pajaro = Pajaro(x=150) # jugador UPDATE
        self.list_tuberias = [] # lista de tuberias UPDATE


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

        # verificamos si se debe agregar una tuberia UPDATE
        if self.fotogramas % FREQ_TUBERIAS == 0:
            self.list_tuberias.append(Tuberias())
        
        # conservamos las tuberias que no han salido de pantalla UPDATE
        self.list_tuberias = [tuberias for tuberias in self.list_tuberias if tuberias.rect1.right>0]
        
        # actualizamos el contador de fotogramas UPDATE
        self.fotogramas += 1

        # actualizamos los objetos del juego
        #self.pajaro.actualizar() # UPDATE
         # UPDATE
        for tuberias in self.list_tuberias:
            tuberias.actualizar()
        

    # metodo para dibujar la escena en la pantalla
    def dibujar(self):
        # dibujamos fondos en pantalla
        self.pantalla.blit(self.fondo1, self.rect1)
        self.pantalla.blit(self.fondo2, self.rect2)

        # dibujamos objetos del juego
        #self.pajaro.dibujar(self.pantalla) # UPDATE
        # UPDATE
        for tuberias in self.list_tuberias:
            tuberias.dibujar(self.pantalla)



# clase Pajaro
class Pajaro:
    FREQ_ACT = 5 # frecuencia de actualizacion de sprites
    GRAVEDAD = 1.5 # gravedad
    VERT_VEL = -15 # velocidad vertical

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

        # velocidad vertical inicial
        self.v_vel = 0

    
    # metodo para el evento de volar
    def volar(self):
        # verificamos que el jugador no ha salido de pantalla
        if 0 < self.rect.top:
            # incrementamos velocidad vertical
            self.v_vel += self.VERT_VEL


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
        
        # actualizamos la dinamica vertical
        self.v_vel += self.GRAVEDAD 
        self.rect.y += self.v_vel

    
    # metodo para dibujar al jugador
    def dibujar(self, pantalla):
        pantalla.blit(self.sprites[self.sprint_ind], self.rect)



# clase para dibujar tuberias UPDATE
class Tuberias:
    # alturas permitidas para el centro de tuberias
    CENTRO_MIN = 220
    CENTRO_MAX = 580
    GAP = 250 # espacio entre tuberias

    def __init__(self, x=BG_H):
        # definimos las imagenes de las tuberias
        self.img1 = pg.transform.scale2x(pg.image.load(f"{IMGS_PATH}/pipe.png")) # inferior
        self.img2 = pg.transform.flip(self.img1, False, True) # superior

        # coordenadas rectangulares
        self.rect1 = self.img1.get_rect()
        self.rect2 = self.img2.get_rect()

        # posicionamos en coordenada horizontal
        self.rect1.x = x
        self.rect2.x = x

        # elegimos aleatoriamente altura del centro de las coordenadas
        centro = np.random.randint(self.CENTRO_MIN, self.CENTRO_MAX)

        # colocamos tuberias
        self.rect1.top = centro + int(self.GAP/2)
        self.rect2.bottom = centro - int(self.GAP/2)
    

    # metodo para actualizar los objetos
    def actualizar(self):
        self.rect1.x -= VEL_H
        self.rect2.x -= VEL_H
    

    # metodo para dibujar las tuberias
    def dibujar(self, pantalla):
        pantalla.blit(self.img1, self.rect1)
        pantalla.blit(self.img2, self.rect2)



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
        # evento: volar
        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
            escena.pajaro.volar()
        
    # actualizamos configuraciones y dibujamos objetos en la escena
    escena.actualizar()
    escena.dibujar()
    pg.display.flip()

    # limitamos reloj a 30 fotogramas por segundo
    reloj.tick(30)

# cerramos la aplicacion si se sale del bucle
pg.quit()