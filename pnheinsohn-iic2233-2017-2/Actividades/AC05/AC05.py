from form import FormRegister


if __name__ == '__main__':
    form = FormRegister()
    with open("test.txt") as test_file:

        for line in test_file:
            name, gender, rut, course, section, comment = line.split(";")
            comment = comment.strip("\n")
            try:
                rut_verified = form.check_rut(rut)
            except ValueError as err:
                if rut.find("-") == -1:
                    rut = rut[:-1] + "-" + rut[-1]
                if rut.find(".") != -1:
                    rut = rut.replace(".", "")
                if rut.find(" ") != -1:
                    rut = rut.replace(" ", "")
            finally:
                if rut_verified:
                    try:
                        form.add_course(course, section)
                    except TypeError as err:
                        print(err)
                        if "section " in section:
                            section = section.replace("section ", "")
                        elif section == "todas":
                            section = "0"
                        if course.find(" ") != -1:
                            course = course.replace(" ", "")
                        form.add_course(course, section)
                        print("Curso consultado de igual forma")
                    except KeyError as err:
                        print(err)
                    except IndexError as err:
                        print(err)
                        section = "0"
                        form.add_course(course, section)
                        print("Curso consultado de igual forma")

                    form.register_people_info(name, gender, comment)
        try:
            form.save_data("result.txt")
        except IOError as err:
            print(err)

