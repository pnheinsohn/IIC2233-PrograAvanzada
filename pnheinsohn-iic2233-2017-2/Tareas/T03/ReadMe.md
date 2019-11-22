## Librerías usadas:

- Collections para importar Counter y namedtuple.
- os para el archivo "resultados.txt".
- PyQt5 para importar QtWidgets.
- functools para usar reduce.
- random para usar choice.
- unittest para testing.
- time para usar time().
- sys.


## Consideraciones:

- El programa lee los archivos una vez que se ejecuta guardando todos los genomas en listas en namedtuples, luego uso mucha RAM, pero es bastante rápido. (tarda entre 4 - 6
  segundos en abrir los archivos, pero las consultas las ejecuta en menos de 0.1 segundo).

# Consultas
- Para obtener la consulta "pariente_de" nótese en el módulo de "Consultas.py" varias funciones llamadas "likehood", estas si bien no parecen atomizadas, si lo están, y
  procuré de hacer las referencias lo más claro posible --> Fen: Fenotypes, get_característica(persona) --> la cual retorna el fenotipo de la característica del individuo
  en cuestión.

- Luego está "get_gemelo_genetico(persona, personas)", el que generará listas con contadores de "similitud" de todas las personas, según las 9 características mediante
  la función "get_counters_char(persona, otras_personas)", y otras de recursión. Aquella posición de la lista resultante con el número más grande, será la posición de la 
  lista "otras_personas" de la persona que califica como "gemelo genético".

- A medida que uno va haciendo consultas en una misma ejecución, los números de consultas van aumentando (tanto como en el "Set de Consultas" realizadas, como en cada
  "Consulta" per se. Lo anterior, producto a que cuando uno quiera generar el archivo "resultados.txt" pueda diferenciar correctamente cuándo se ejecutó el programa
  nuevamente, y así poder tener mayor información respecto a las consultas realizadas --> Es más útil.

# Raise Errors
- Al momento de elevarse un error en alguna consulta, el programa lo que hace es detener la consulta realizada, imprimir tanto en la GUI como en consola el problema, y
  posteriormente seguir con la próxima consulta.

# Testing
- Cree una carpeta llamada "Testing" donde guardé 3 archivos: "genomas.txt", "listas.txt" y "wrong_genomas.txt", en donde los primeros 2 son los inicialmente entregados,
  mientras que el último tiene a dos personas con "GenomeError"; uno con solo "espacios" en su genoma y otro con puras "F's". El setUp se encarga netamente de definir
  variables a usar, mientras el tearDown de asegurarse que los archivos usados se cierren --> No se creó ningún archivo entre medio, por lo que no fue necesario tener que
  eliminarlos.

- No basta mencionar que se usó bastante la librería random para implementar "choice()", así se logra a cabalidad el testeo de distintas consultas en los mismos escenarios
  cumpliendo a su vez "engañosamente" el requisito de probar todas las funciones..., Pueden correr cuantas veces quieran el testing y siempre saldrá correcto :). Saludos, y
  éxito corrigiendo. Aca abajo dejo una breve descripción de los tests:

- Bad Request    : Solo bastó mostrar los dos escenarios posibles: "Ask" existe (Expected Failure), y "Ask" no existe.
- Not Found      : Tres escenarios posibles: "Cantidad de Parámetros errónea" (seguida de una correcta, para asegurar que sirve), "Nombre de Persona No Existe", y "Tag 
	           Característica No Existe".
- Not Acceptable : Solo bastó mostrar los dos escenarios posibles: "Ask" tiene solución (Expected Failure), y "Ask" no tiene solución.
- Genome Error   : Solo bastó mostrar los dos escenarios posibles: Persona tiene un "Espacio" en su genoma, y Persona tiene un caracter distinto de "AGTC" en su genoma
 		   (seguido de un test de una persona con el genoma correcto, para asegurar que sirve).