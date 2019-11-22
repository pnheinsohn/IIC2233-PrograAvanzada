# Comenzar:
- Se empieza ejecutando el módulo llamado "Menu.py"

# Funcionalidad:
- La idea del código parte desde la clase "MainMenu" la cual tiene el fin de coordinar todos los objetos de las clases "User", "Market", "Currency" y "Orders" así cuando
  diversos objetos de la misma clase puedan acceder a los mismos objetos que otros accedieron. (ej. los mercados con los users)
- El script del MainMenu, además, tiene como finalidad leer todos los archivos CSV que existen y van siendo creados, así se puede almacenar la información para posteriormente
  distribuirla como se debe.
- Si, el script del user quedo enorme jajajajaja. Suerte revisando, espero que no sea tan tedioso D:

# A considerar:
- Al crear un usuario, éste deberá ingresar su usuario nuevamente para entrar.
- Las formas de mantener la aplicación corriendo mediante "running" y "show_options" fueron extraídas de los contenidos de la semana 1 de clases.
- La forma de verificar la validez de las fechas se obtuvieron gracias a StackOverflow, al igual que el uso de **kwargs.
- Al momento de asignar las orders que ya fueron ejecutadas, se consideró que aquellos montos inferiores a 0 como 0, porque el match ya había sido realizado.
- Se infiere que si una orden no proviene de un "Underaged" o no es match de éste, y no tiene un match_date, la orden no será creada despues del nacimiento del usuario
- Se infiere que en los csv's no vendrán orders sin "date_match" que puedan generar un match.
- Al desplegar el historial de matches no se realiza por fecha de ejecución, sino que por nombre de mercado ya que en el enunciado no se especifica.
- Cualquier usuario puede ver información de un mercado, aunque no esté inscrito en éste.
- Los "Underaged" pueden inscribir mercados, pero no recibirán el regalo del magnate Nebil.
- Uno puede ver su "Currency Balance" en el banco (No tiene sentido que esté en otro lugar.
- Un mercado se asigna automáticamente si un usuario tiene una order ahi. En el caso de los "Underaged", el registro en un mercado no implica que este se guarde, ya que
  no tiene sentido guardarse, es más, es mejor porque así si llegan a iniciar sesión, habiendo cumplido la mayoría de edad, podrán registrarse y obtener el regalo de Nebil.
- No se revisa si un usuario "Trader" tiene más de 5 orders activas sin match como "GustavPrudencio" jajaja. Lo que sí, es que no se le permitirá agregar más orders
  a menos de que tenga menos de 5 orders activas, o bien, no haya completado el límite de 15 orders diarias.
- Al revisar las orders históricas, uno podrá ver todas las orders hechas durante el tiempo seleccionado, pero si un usuario elimina una order, esta seguirá apareciendo, ya
  que es una "order histórica". No obstante, no aparecerá en las orders activas del momento.
- No sirve el "Has Priority", el balance histórico de los investors ni las funciones creadas para los creadores del sistema.

# Librerias:
- datetime para importar datetime y timedelta
- abc para importar ABCMeta y AbstractMethod