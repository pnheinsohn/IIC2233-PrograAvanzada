# Comenzar:
- Se empieza ejecutando el m�dulo llamado "Menu.py"

# Funcionalidad:
- La idea del c�digo parte desde la clase "MainMenu" la cual tiene el fin de coordinar todos los objetos de las clases "User", "Market", "Currency" y "Orders" as� cuando
  diversos objetos de la misma clase puedan acceder a los mismos objetos que otros accedieron. (ej. los mercados con los users)
- El script del MainMenu, adem�s, tiene como finalidad leer todos los archivos CSV que existen y van siendo creados, as� se puede almacenar la informaci�n para posteriormente
  distribuirla como se debe.
- Si, el script del user quedo enorme jajajajaja. Suerte revisando, espero que no sea tan tedioso D:

# A considerar:
- Al crear un usuario, �ste deber� ingresar su usuario nuevamente para entrar.
- Las formas de mantener la aplicaci�n corriendo mediante "running" y "show_options" fueron extra�das de los contenidos de la semana 1 de clases.
- La forma de verificar la validez de las fechas se obtuvieron gracias a StackOverflow, al igual que el uso de **kwargs.
- Al momento de asignar las orders que ya fueron ejecutadas, se consider� que aquellos montos inferiores a 0 como 0, porque el match ya hab�a sido realizado.
- Se infiere que si una orden no proviene de un "Underaged" o no es match de �ste, y no tiene un match_date, la orden no ser� creada despues del nacimiento del usuario
- Se infiere que en los csv's no vendr�n orders sin "date_match" que puedan generar un match.
- Al desplegar el historial de matches no se realiza por fecha de ejecuci�n, sino que por nombre de mercado ya que en el enunciado no se especifica.
- Cualquier usuario puede ver informaci�n de un mercado, aunque no est� inscrito en �ste.
- Los "Underaged" pueden inscribir mercados, pero no recibir�n el regalo del magnate Nebil.
- Uno puede ver su "Currency Balance" en el banco (No tiene sentido que est� en otro lugar.
- Un mercado se asigna autom�ticamente si un usuario tiene una order ahi. En el caso de los "Underaged", el registro en un mercado no implica que este se guarde, ya que
  no tiene sentido guardarse, es m�s, es mejor porque as� si llegan a iniciar sesi�n, habiendo cumplido la mayor�a de edad, podr�n registrarse y obtener el regalo de Nebil.
- No se revisa si un usuario "Trader" tiene m�s de 5 orders activas sin match como "GustavPrudencio" jajaja. Lo que s�, es que no se le permitir� agregar m�s orders
  a menos de que tenga menos de 5 orders activas, o bien, no haya completado el l�mite de 15 orders diarias.
- Al revisar las orders hist�ricas, uno podr� ver todas las orders hechas durante el tiempo seleccionado, pero si un usuario elimina una order, esta seguir� apareciendo, ya
  que es una "order hist�rica". No obstante, no aparecer� en las orders activas del momento.
- No sirve el "Has Priority", el balance hist�rico de los investors ni las funciones creadas para los creadores del sistema.

# Librerias:
- datetime para importar datetime y timedelta
- abc para importar ABCMeta y AbstractMethod