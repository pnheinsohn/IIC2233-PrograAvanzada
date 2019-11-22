# Supuestos

- Tal y como lo menciona el enunciado los metodos de "Guardar Juego" y "Click Number" funcionan como "Github", si tengo varios estados guardados (1, 2, 3 y 4), en donde
  si el 2 es presionado, los estados superiores (3 y 4) dejaran de existir y serán inaccesibles (como los "commit").
- Si bien, el hechizo plot twist no está implementado, un jugador, si esque se apropia de una de las piezas del contrincante, podrá retirar (mediante "retroceder") 
  las piezas que se apropió. Por lo tanto, si un jugador pierde alguna pieza, éste no podrá retirarla.
- "Ctrl-Z" no es guardado en el historial, ya que carece de funcionalidad. Lo que se realiza es que cada jugada es registrada (insertar una pieza en el tablero), y en caso
  de que dicha jugada sea retirada, esta será eliminada del historial.
- Al guardar un estado o retirar una pieza, la pieza a insertar es cambiada, ya que ese turno finaliza. Sin embargo, esas piezas no son perdidas, sino que son devueltas
  al "Deck" de piezas. Lo mismo ocurre al volver a un estado anterior; todas las piezas que estaban se devuelven al "Deck".

# A Considerar

- Los métodos del módulo Iterador fueron extraídos principalmente de clases (Semanas 4 y 5), y de StackOverflow para el método reverse. Los métodos len, repr, pop, delitem
  y setitem que los pensé yo jajajaja (yey!).
- Los metodos heredados que sirven a la cabalidad son: "Colocar Pieza", "Guardar Juego", "Rotar Pieza", "Retroceder", "Click Number". No se implementó "Contar Puntaje", 
  "Plot Twist" ni terminar el juego con la "Snitch Dorada". "Hint" está medianamente logrado, solo entrega una pista si la pieza puede ser colocada, no por puntaje.
- Se realizó una estructura de datos llamada "PilaAndQueue" solo para demostrar que logré crearla, ya que no se usa. Se esperaba emplear en retroceder, pero creo que lo
  planteado por mí, en ese método, se ajusta mejor al modelamiento del problema.
- 3 módulos de scripts bastan y sobran producto a los fines que tiene cada uno; el "Tablero" que interactúa con la "GUI", "Piezas" que contiene dos clases que interactúan
  con csv's y las piezas del juego, y "EDD" que contiene todo lo relevante respecto a las estructuras de datos.
- Si bien el uso de "yield" induce al hecho de usar generadores, se dejó puesto producto a que venía con el demo.py.

# Librerias

- Sys
- Random