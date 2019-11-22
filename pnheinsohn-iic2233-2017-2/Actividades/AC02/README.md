# Actividad 2
## Integrantes: Paul Heinsohn y Tien Villalobos



# Supuestos de la Tarea


- Asumimos que el cliente frecuente se asigna como un atributo (booleano) al instanciar la clase Cliente.


- Asumimos que el estilo de las fechas era de la forma "dia-mes-año", donde el separador debía ser "-" (ie: 17-08-2017).


- Asumimos que si no se entrega la información de la dieta (vegano/vegetariano) al instanciar la clase Cliente, el usuario puede agregar cualquier producto al carro.


- Asumimos que no existirán errores al instanciar ciertas clases (ie: entregar "pickle rick" en vez de una fecha).



# Comentarios


- En el archivo probablemente sobra un par de parentesis antes de un format al final de un método, pero en la ultima versión que subimos, segundos más tarde
	(o al menos eso creemos, si es asi: casi :cry:) fue arreglado ese detalle.


- Tuvimos un problema al instanciar pantalon de queso, pero creemos que fue porque le estabamos pasando un argumento más del que necesitaba,
	ya que la clase con multiherencia tenia todos los atributos con el super(). Debimos haber usado **kwargs.

- Decidimos dejar a los Clientes "veganos" y "vegetarianos" como atributos por terminos de tiempo y facilidad.


- Hay dos formas de ver la información nutricional de una comida (alimento):
	con print(comida), y el metodo get_product_info() del Cliente que permite ver lo mismo, pero con las proporciones de cuántos gramos quiere.


- La mejor instancia es la verdura... Pickle Rick! :cucumber:

![Alt Text](https://media.giphy.com/media/9zXWAIcr6jycE/giphy.gif)


.
- Saludos, y éxito corrigiendo.