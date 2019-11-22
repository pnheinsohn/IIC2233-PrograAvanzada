def go_param_kwargs(param_list):  # Get kwarg values for instantiate classes
    kwargs = {}
    for i in range(len(param_list[0])):
        if param_list[0][i] == "días_susto":
            kwargs.update({"dias_susto": param_list[1][i]})
        elif param_list[0][i] == "concha_estéreo":
            kwargs.update({"concha_estereo": param_list[1][i]})
        elif param_list[0][i] == "distribución_almuerzo":
            kwargs.update({"distribucion_almuerzo": param_list[1][i]})
        else:
            kwargs.update(({param_list[0][i]: param_list[1][i]}))
    return kwargs


def go_people_kwargs(row, entity, first_filter):  # Get kwarg values for instantiate classes
    kwargs = {}
    for i in range(len(first_filter[0])):
        if first_filter[0][i].lower() == "nombre":
            kwargs.update({"name": row[i]})
        elif first_filter[0][i].lower() == "apellido":
            kwargs.update({"last_name": row[i]})
        elif first_filter[0][i].lower() == "edad":
            kwargs.update({"age": row[i]})
    if entity == "Alumno" or entity == "Funcionario":
        for i in range(len(first_filter[0])):
            if first_filter[0][i] == "Vendedores de Preferencia":
                kwargs.update({"best_sellers": row[i]})
    elif entity == "Vendedor":
        for i in range(len(first_filter[0])):
            if first_filter[0][i] == "Tipo Comida":
                kwargs.update({"food_type": row[i][:-1]})
    elif entity == "Carabinero":
        for i in range(len(first_filter[0])):
            if first_filter[0][i] == "Personalidad":
                kwargs.update({"personality": row[i]})
    return kwargs


def go_product_kwargs(row, first_filter):  # Get kwarg values for instantiate classes
    kwargs = {}
    for i in range(len(first_filter[0])):
        if first_filter[0][i] == "Producto":
            kwargs.update({"product_name": row[i]})
        elif first_filter[0][i] == "Precio":
            kwargs.update({"price": row[i]})
        elif first_filter[0][i] == "Calorias":
            kwargs.update({"calories": row[i]})
        elif first_filter[0][i] == "Tasa Putrefacción":
            kwargs.update({"putrefaction_rate": row[i]})
        elif first_filter[0][i] == "Vendido en":
            kwargs.update({"sold_in": row[i]})
    return kwargs


get_int_list = lambda string: [int(string.split(";")[0]), int(string.split(";")[1])]
get_float_list = lambda string: [float(string.split(";")[0]), float(string.split(";")[1])]
get_list = lambda string: [string.split(";")[0], string.split(";")[1]]
