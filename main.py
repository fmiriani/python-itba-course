from Update.updateData import update_data
from Visualize.visualizeData import resume_function, grafico_de_ticker
import sys

#  https://github.com/ITBA-Python/Certificacion-Profesional-Python/blob/main/TP_Final.md

# API: https://polygon.io/docs/stocks/getting-started

def answer_validator(menu_type):
    """ funcion que valida que la respuesta sea 1 o 2 y sigue pidiendo input hasta que se cumpla la condición

    Args:
        menu_type: str con el tipo de menu de donde proviene la elección; usado para re-dirigir en answer_handdler

    Returns:
        anser_handdler(rta, menu_type): función que elije el proximo paso a cumplir según haya sido la rta y el menu donde fue elegida
    """


    while True:
        try:
            rta = int(input("Ingrese su opción:"))
        except ValueError:
            print("La respuestas debe ser un número")
            continue

        if rta not in [1,2]:
            print("La respuestas debe ser 1 o 2")
            continue
        else:
            break
    
    return anser_handdler(rta, menu_type)


def anser_handdler(rta, menu_type):
    """ función que elije el siguiente paso según sea la rta y el menú
        En cada opción llama a una función que realiza una tarea.
        Si la respuesta proviene del menú de salida y la elección es salir, corta el programa

    Args:
        rta: respuesta del usuario
        menu_type: str con el tipo de menu de donde proviene la elección; usado para re-dirigir en answer_handdler

    Returns:
        exit_menu(): menu con las opciones de salida que luego corta el programa
        main_menu(): menu con las opciones del programa
        
    """


    if menu_type == "main":
    
        if rta==1 :

            update_data()
            #Va la funcion que hace las actualizaciones

            return exit_menu()

        else:
            
            visualize_menu()
            #Va la funcion que hace las visualizaciones

            return exit_menu()
    
    elif menu_type == "visual":

        if rta==1 :
            
            resume_function()
    
            return exit_menu()

        else:
    
            grafico_de_ticker()

            return exit_menu()
    
    elif menu_type == "exit":

        if rta==1 :

            return main_menu()
            #Eleccion de continuar

        else:
            print("Gracias por usar nuestro programa")
            sys.exit()
            

def visualize_menu():
    """Menu para visualización con opciones

    Args:
        none

    Returns:
        función: validadora de respuesta
    """
    
    menu_type = "visual"
    print("\n____________________________MENU VISUALIZACION__________________________________")
    print("Que Visualización de datos desea?\nResponda con 1 o 2 según sea su elección:"+"\n\t1.Resumen"+"\n\t2.Gráfico de ticker")

    return answer_validator(menu_type = menu_type)


def exit_menu():
    """Menu para selecciónar salida o continuar

    Args:
        none

    Returns:
        función: validadora de respuesta
    """


    menu_type = "exit"
    print("\n_______________________________MENU SALIDA__________________________________")
    print("Desea continuar o salir?\nResponda con 1 o 2 según sea su elección:"+"\n\t1.Continuar"+"\n\t2.Salir")
    return answer_validator(menu_type = menu_type)

def main_menu():
    """Menu principal con opciones

    Args:
        none

    Returns:
        función: validadora de respuesta
    """
    
    menu_type = "main"
    print("\n_______________________________MENU PRINCPIAL__________________________________")
    print("Bienvenido/a al Proyecto Final de Fabricio Miriani para el curso de Python del ITBA\nQue desea hacer?\nResponda con 1 o 2 según sea su elección:"+"\n\t1.Actualización de datos"+"\n\t2.Visualización de datos")
    
    return answer_validator(menu_type)

main_menu()