## Librerias Usadas

- sys
- os.path
- PyQt.QtCore
- PyQt.Qt
- PyQt.QtGui
- PyQt.QtWidgets
- threading
- math
- random
- time
- abc


## A Considerar

- Aparecerán muchos errores fatales si no se realiza el pequeño cambio variable siguiente:
	. BackEnd.py línea 170 "alive_score = Thread(target=self.time_score, daemon=True)" cambiar "self.time_score" por "self.alive_score"
	. BackEnd.py línea 203 "alive_score = Thread(target=self.time_score, daemon=True)" cambiar "self.time_score" por "self.alive_score"
  Porfavor realizar este cambio, es enanooo u.u.

- Las colisiones entre enemigos, personaje, bombas, y todo tipo de objetos son del tipo "trigger" por lo que pueden pasar por encima de cada uno. Cabe destacar, que la
  colisión con los bordes no es de este tipo. Lo anterior fue con el propósito de no saturar el programa (no fue bien logrado).

- Los enemigos no tienen el sentido de su sprite bien coordinado con la dirección de movimiento, por lo que puede que apunten hacia otro lado mientras caminan.

- Los sprites y las posiciones de los objetos del juego no están bien coordinadas, ya que sus (x, y) estan vinculados a la esquina superior izquierda, por lo que si no
  se detecta una colisión es porque no fue con esa esquina (no es tan lejos, es en la esquina del sprite, ups).

- Para que un enemigo empiece a recibir daño del personaje principal, y este último también, estos tienen que estar tocándose. Si el jugador principal permanece en un (x, y)
  mientras ataca a un enemigo, ambos se harán daño sin moverse. (Recomiendo fuertemente atacar asi, y a los chicos arrinconarlos a alguna esquina, menos la inferior derecha
  por el tema de los (x, y) desfazados jajaja).

- Al cambiar de central widget (etapa o main menu), aparecen muchos errores de index_error que son obviados con try/except.

- Al volver al main menu, y querer volver a jugar queda la "cagada" jajajajajaja, no logré resolver ese detalle.

- El ranking no es mostrado correctamente, pero la forma de obtener los 10 mejores es la correcta. Ver métodos de GameWidget(QWidget) en FrontEnd "ask_for_name(self, score)",
  save_scores(self), e is_high_score(row) para ver que se guardan por orden de puntaje, y ver el método de PreGameWidget(QWidget) en FrontEnd llamado show_ranking(self) que
  alcanza a mostrar los 10 primeros en caso de que al lado del "if i != 0:" se pusiera un " and i < 11" entre el "0" y ":". De igual modo, no se muestra asique da igual jaja.

- El inventory parte con esas estrellas pa hacerlo más bkn! jajajja, para comprar items en la tienda si funciona el método de Drag & Drop. Sin embargo, al reemplazar un item
  el eliminado "se conservará" en términos de "stats" ya que no logré hacerlo a tiempo u.u.

- El radio de ataque de las bombas es 10 + radio del sprite

- Para pausar el juego es "Ctrl + P". El juego se pausa cuando se apreta "Ctrl + P", o "Ctrl + T" para abrir la tienda. Para salir de pausa se usa "Ctrl + P", sirve salir de
  pausa con "Ctrl + T" en caso de que esté abierta la ventana de la tienda.

- La implementación de los 30 segundos de espera es con el fin de que los threads de items (bombas, vidas y monedas) terminen su ciclo y no se acumule el Thread para las
  siguientes etapas, etc.


## Recomendaciones

- Probar las jugabilidades en la primera vida de ejecución del juego jajajaja.