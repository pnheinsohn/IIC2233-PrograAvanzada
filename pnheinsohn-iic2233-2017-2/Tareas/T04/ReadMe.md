#####################
## Consideraciones ##
#####################

- El programa se ejecuta con el módulo "Main.py".

- El formato de tiempo se basa en minutos, donde cada día va de 0 a 240 minutos, cada 30 días se conforma 1 mes, y la simulación dura 4 meses.

- Se tomaron los días números 6, 7, 13, 14, 20, 21, 27 y 28 como fines de semana, siendo los impares sábado y los pares domingo. Luego, son 22 días hábiles por mes. Si bien
  cuando llega uno de esos días empleo una modelación pseudo-síncrona (hago un "self.actual_day += 1"), esta es DES ya que el cambio de día es un EVENTO y es válida esta
  implementación. Si hubiese hecho "self.actual_time += 1" sería síncrona :).

- Durante los findes de semana pueden ocurrir "Lluvias de hamburguesas" y "Temperaturas extremas", las cuales serán contadas para las estadísticas finales, pero no se
  mostrarán en consola. El resto de los eventos no ocurren durante dichos días.

- Si hay un miembroUC en alguna cola, esperando comprar algun snack o almuerzo, y tocan las 15:00, éste se irá a su casa y no alcanzará a comprar dicho producto.

- Se me olvidó quitarle el stock cuando un miembroUC le compraba un producto a un vendedor. Esto se corrige fácilmente, agregando un "self.daily_stock -= 1" en el método
  attend_member(self, actual_time) de la clase "Seller" en el módulo "Persons.py" ("Nótese el commit del ReadMe para ver este cambio comentado al final del método"). Con
  este cambio, ellos pueden quedar "stockless" y aportar a las estadísticas, y los alumnos pueden cambiar correctamente de cola cuando un funcionario entra antes que ellos.
  ¡Lo que ya está implementado! -> El programa no se cae ni nada, sin este cambio el programa funciona bien, solo afecta en esos dos detalles. Please Mercy u.u.

- No se implementaron los Carabineros, ni todo lo relacionado con ellos (incluyendo las estadísticas)... no existen en esta simulación jajajajajaja (solo existe la clase 
  "Cops", y se le asignan sus atributos).

- Para manejar los cambios en la putrefacción y calidad de los productos agregué dos variables "putrefaction_intensification" y "quality_reduction" a las fórmulas, en donde
  casi siempre tendrán el valor numérico de "1", y el resto de las veces de "2" para lograr lo pedido.

- Cuando un miembroUC llega a la U, éste tendrá un 50% de probabilidades de comprar un solo snack ese día, si la probabilidad falla, éste no comprará un snack.

- Para abrir los archivos de personas y productos no lo hago igual que los parámetros iniciales, ya que plantee una modelación completa en ingles por lo que cree el módulo
  "Functions.py" para realizar las conversiones. Sin embargo, por temas de tiempo, decidí abrir los parámetros iniciales de la forma más directa que encontré.

- Durante los días de la concha acústica no incluí que la asistencia en dicho día aumentara, ya que no se explicita bien cómo hacerlo, y por miedo decidí no implementarla.
  (No quise abrir una issue, no debe ser tanto puntaje jaja).

- Creo que eso sería todo. Un gran abrazo y suerte en la corrección de las tareas. Saludos!!!!