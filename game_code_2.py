import pygame as pg
import numpy as np

# parametros globales del juego
IMGS_PATH = 'imgs' # path de las imagenes 
VEL_H = 10 # velocidad horizontal del juego 
BG_V = 800 # tamano vertical de la ventana
BG_H = 700 # tamano horizontal de la ventana
FREQ_TUBERIAS = 50 # numero de fotogramas para generar una nueva tuberia 


# clase para dibujar jugador  
class Pajaro:
    FREQ_ACT = 5 # frecuencia con la que se actualizan los sprites de la clase
    GRAVEDAD = 1.5 # fuerza de gravedad
    VERT_VEL = -15 # velocidad horizontal al volar 

    def __init__(self, x=100, y=350):
        # elegimos un color aleatoriamente entre las 8 opciones
        ind_color = np.random.randint(1,9)
        
        # sprites del pajaro
        self.sprites = [pg.transform.scale(pg.image.load(f'{IMGS_PATH}/{img}.png'), (3*32, 3*21))
                        for img in [f'bird_{ind_color}1', f'bird_{ind_color}2', f'bird_{ind_color}3', f'bird_{ind_color}2']]

        # coordenadas rectangulares del objeto
        self.rect = self.sprites[0].get_rect()

        # actualizamos las coordenadas con la configuracion definida
        self.rect.x = x
        self.rect.y = y

        # indice del sprite inicial
        self.sprint_ind = 0

        # contador de fotogramas
        self.cont = 0

        # velocidad vertical inicial 
        self.v_vel = 0

        # bandera del estado del pajaro 
        self.vivo = True


    # metodo para reducir la velocidad vertical y dar el efecto de volar 
    def volar(self):
        # aumentamos velocidad vertical si el jugador no ha salido del borde superior
        if self.vivo and 0 < self.rect.top:
            self.v_vel += self.VERT_VEL


    # metodo para actualizar la configuracion del pajaro
    def actualizar(self):
        # anadimos uno al conteo de fotogramas
        self.cont += 1

        # actualizamos indice de sprite si el contador alcanza la frecuencia de actualizacion y el pajaro sigue vivo
        if self.cont % self.FREQ_ACT==0:
            self.sprint_ind += 1

            # si el indice a alcanzado el maximo entonces lo reiniciamos
            if self.sprint_ind == 4:
                self.sprint_ind = 0
        
        # actualizamos la dinamica vertical 
        self.v_vel += self.GRAVEDAD # incremento de velocidad 
        self.rect.y += self.v_vel # actualizacion de posicion vertical 

        # evitamos que el pajaro salga de pantalla al tocar el piso 
        self.rect.y = min([self.rect.y, BG_V-20])

        # actualizamos la dinamica horizontal para sacar el objeto de pantalla si ha muerto 
        if not self.vivo:
            self.rect.x -= VEL_H

    
    # metodo para dibujar el pajaro
    def dibujar(self, pantalla):
        # dibujamos fondos en pantalla
        pantalla.blit(self.sprites[self.sprint_ind], self.rect)
    
    
    # metodo para verificar si el pajaro no ha colisionado con el suelo o con tuberias
    def detectar_colisiones(self, list_tuberias):
        # actualizamos su estado si ha tocado el suelo
        if BG_V < self.rect.bottom:
            self.vivo = False
        
        # iteramos por tuberias
        for tuberias in list_tuberias:
            # acutualizamos su estado si hay colicion con la tuberias superior o inferior
            if self.rect.colliderect(tuberias.rect1) or self.rect.colliderect(tuberias.rect2):
                # actualizamos el estado del pajaro
                self.vivo = False

                # elimininamos velocidad horizontal si en pajaro esta volando
                if self.v_vel < 0:
                    self.v_vel = 0
                break


 
# clase para dibujar un par de tuberias
class Tuberias:
    # variables globales de la clase
    CENTRO_MIN = 220 # altura minima del centro de tuberias
    CENTRO_MAX = 580 # altura maxima del centro tuberias
    GAP = 250 # espacio entre tuberias
    VEL_V = 6 # velocidad vertical UPDATE

    def __init__(self, x=BG_H):
        # definimos las imagenes de las tuberias
        self.img1 = pg.transform.scale2x(pg.image.load(f"{IMGS_PATH}/pipe.png")) # tuberia inferior
        self.img2 = pg.transform.flip(self.img1, False, True) # tuberia superior (flip vertical de img1)

        # definimos coordenadas rectangulares de ambos objetos
        self.rect1 = self.img1.get_rect()
        self.rect2 = self.img2.get_rect()

        # posicionamos en coordenada horizontal
        self.rect1.x = x
        self.rect2.x = x

        # elegimos aleatoriamente una posicion vertical para el centro de las coordenadas
        centro = np.random.randint(self.CENTRO_MIN, self.CENTRO_MAX)

        # colocamos tuberias de acuerdo al centro
        self.rect1.top = centro + int(self.GAP/2)
        self.rect2.bottom = centro - int(self.GAP/2)

        # elegimos aleatoriamente el sentido de la velocidad vertical inicial UPDATE
        self.v_sentido = np.random.choice([-1,1])
    

    # metodo para actualizar los parametros de los objetos
    def actualizar(self):
        # actualizamos su posicion de acuerdo al movimiento de la escena
        self.rect1.x -= VEL_H
        self.rect2.x -= VEL_H

        # actualizamos la posicion vertical UPDATE
        self.rect1.y += self.v_sentido*self.VEL_V
        self.rect2.y += self.v_sentido*self.VEL_V

        # cambiamos el sentido de la tuberia en caso de que alguna tuberia salga de rango UPDATE
        if self.CENTRO_MAX + self.GAP/2 < self.rect1.top or self.rect2.bottom < self.CENTRO_MIN - self.GAP/2:
            self.v_sentido = -1*self.v_sentido
    

    # metodo para dibujar las tuberias
    def dibujar(self, pantalla):
        pantalla.blit(self.img1, self.rect1)
        pantalla.blit(self.img2, self.rect2)


    
# clase para controlar la escena del juego y sus objetos
class Escena:
    def __init__(self, pantalla):
        # deifnicion de parametros
        self.pantalla = pantalla # pantalla sobre la cual dibujar

        # contador de fotogramas 
        self.fotogramas = 0
        
        # creamos dos fondos para dibujar uno despues del otro
        self.fondo1 = pg.image.load(f"{IMGS_PATH}/background.png").convert() # imagen
        self.rect1 = self.fondo1.get_rect() # coordenadas
        self.fondo2 = pg.image.load(f"{IMGS_PATH}/background.png").convert() # imagen
        self.rect2 = self.fondo2.get_rect() # coordenadas

        # ancho de la imagen de fondo
        self.img_h = self.fondo1.get_width()

        # actualizamos posicion horizontal del segundo fondo despues del primero
        self.rect2.x = self.rect1.x + self.img_h

        # creamos los objetos del juego 
        self.pajaro = Pajaro(x=150) 
        self.list_tuberias = [] # lista de tuberias 

        # definimos fuente para mostrar la puntuacion 
        self.fuente = pg.font.SysFont('consolas', 60)

        # definimos variable para llevar la puntuacion 
        self.puntuacion = 0


    # metodo para actualizar las configuraciones de la escena
    def actualizar(self):
        # actualizamos la posicion de las imagenes de fondo
        self.rect1.x -= VEL_H
        self.rect2.x -= VEL_H

        # verificamos si las imagenes siguen en pantalla
        # de lo contrario colocamos la imagen fuera de pantalla al final de la otro imagen
        if self.rect1.x < -self.img_h:
            self.rect1.x = self.rect2.x + self.img_h
        if self.rect2.x < -self.img_h:
            self.rect2.x = self.rect1.x + self.img_h
        
        # verificamos si se debe agregar una tuberia 
        if self.fotogramas % FREQ_TUBERIAS == 0:
            self.list_tuberias.append(Tuberias())

        # conservamos unicamente las tuberias que no han salido de pantalla 
        self.list_tuberias = [tuberias for tuberias in self.list_tuberias if tuberias.rect1.right>0]

        # actualizamos la puntuacion considerando la frecuencia de aparicion de tuberias y si el jugador sigue vivo 
        if (self.fotogramas+1)%FREQ_TUBERIAS==0 and self.pajaro.vivo:
            self.puntuacion += 1

        # actualizamos el contador de fotogramas 
        self.fotogramas += 1

        # verificamos colisiones 
        self.pajaro.detectar_colisiones(self.list_tuberias)
        
        # actualizamos los objetos del juego 
        self.pajaro.actualizar() 
        for tuberias in self.list_tuberias:
            tuberias.actualizar()


    # metodo para dibujar la escena en la pantalla
    def dibujar(self):
        # dibujamos fondos en pantalla
        self.pantalla.blit(self.fondo1, self.rect1)
        self.pantalla.blit(self.fondo2, self.rect2)

        # dibujamos objetos del juego 
        self.pajaro.dibujar(self.pantalla) 
        for tuberias in self.list_tuberias:
            tuberias.dibujar(self.pantalla)
        
        # dibujamos puntuacion 
        texto_puntuacion = self.fuente.render(f"{self.puntuacion}", True, (255, 255, 255))
        self.pantalla.blit(texto_puntuacion, (BG_H-100, BG_V-80))


# inisializamos los modulos de pygame
pg.init()

# creamos una pantalla para dibujar
pantalla = pg.display.set_mode((BG_H, BG_V))

# creamos un reloj para controlar la actualizacion de fotogramas
reloj = pg.time.Clock()

# creamos la escena para controlar los objetos del juego 
escena = Escena(pantalla)

# creamos variable para mantener el bluque del juego en ejecucion
aux_val = True

# bucle de actualizacion del juego
while aux_val:
    # iteramos por todos los eventos identificados por pygame
    for evento in pg.event.get():
        # actualizamos la variable auxiliar para cerrar el juego
        if evento.type == pg.QUIT: 
            aux_val = False
        # ejecutamos la accion de volar si se presiona la tecla espacio 
        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
            escena.pajaro.volar()
        # reiniciamos la escena con la tecla r para reiniciar todo el juego 
        if evento.type == pg.KEYDOWN and evento.key == pg.K_r:
            # creamos un nuevo objeto escena
            escena = Escena(pantalla)
    
     # actualizamos configuraciones de objetos en la escena 
    escena.actualizar()

    # dibujamos los objetos con sus nuevas configuraciones 
    escena.dibujar()
            
    # actualizamos todos los cambios realizados a la pantalla
    pg.display.flip()

    # limitamos el reloj a 30 fotogramas por segundo
    reloj.tick(30)

# cerramos la aplicacion si se sale del bucle
pg.quit()