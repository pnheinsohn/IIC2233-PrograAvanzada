## Librerias Usadas

- Json
- Pickle
- Datetime
- Socket
- threading
- os
- PyQt5
- random


## Consideraciones

- Hay dos módulos llamados "Variables.py", uno en el directorio Server y otro en el Client. Se emplean dos porque se supone que el server no está en el mismo computador
  que el cliente, por lo que no tiene sentido que exista solo 1. Además, así saben perfectamente dónde modificar el "HOST y PORT", así es más ordenado que las primeras dos
  líneas. 

- Por favor, no modificar el orden de las capetas ni archivos, por lo que al agregar las imágenes con las que trabajarán, agréguenlas a la carpeta "Imagenes" del directorio 
  Server (no confundir con la que el código genera en Cliente, ni con la carpeta Background del Server). Además, asegurarse de que el archivo csv "comentarios.csv" en ese 
  mismo directorio ("Imagenes") no exista antes de poner las imágenes y correr el programa, porque osino habrá un index error -> Imaginen si el server se abre y no hay fotos
  el archivo comentarios.csv es vacío, pero ahora se agrega una foto, el archivo seguiría siendo vacío pero el índice 0 ahora si existe. Esto se soluciona borrando los
  "comentarios.csv" jajajajaja. En resumen, suban las imagenes a la carpeta y después corran el server, no antes :).

- No trabajo con las imágenes, por lo que ningun método de edición está implementado. En pocas palabras, no sirve el boton "Send Changes", "Recortar", "Balde", ni "Blurry". 
  El programa por lo tanto no actualiza en tiempo real la ventana espectador, pero sí diferencia cuando alguien está "editando" o no, y se le pregunta si prefiere ser
  espectador o regresar (GUI espectador != GUI editor), luego el bloqueo de imagen sirve.

- En cuanto a los comentarios, estos funcionan a cabalidad a excepción de los emojis.

- Para editar una imagen se debe abrir la galería de fotos y apretar la imagen deseada. No se pueden agregar fotos externas.

- Lamento la tarea vaga pero necesito muy poca nota, como un 1.5, por ahi jajajaja. Feliz recorrección y ánimo con lo que queda del semestre!!! Saludos, y gracias por la
  paciencia. Un abrazo.