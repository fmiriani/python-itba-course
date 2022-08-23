import datetime
from Update.connectSQL import connect_to_sql
import requests

from Update.ExtractAndInsert import extract_insert
#BUG:If I run directly from UpdateData.py is ok with "from ExtractAndInsert "; from outside I need it to be "from Update.ExtractAndInsert"

import pandas as pd

# 1- Cuando main llama a update_data, se toman los inputs del usuario, los cuales son validados por date_validate; esta ultima devuelve la fecha
# 1a Dentro Al final de la validacion se corre la actualizacion de la informacion


def create_list_of_dates(sdate,edate):
    """ a partir de la fechas de comienzo y fin ingresadas crea una lista de fechas
        la lista será usada como input para la API, en la sección que requiere fechas

    Args:
        sdate(str): fecha comienzo formato YYYY-MM-DD ingresada por usuario
        edate(str): fecha fin formato YYYY-MM-DD ingresada por usuario

    Returns:
        list_dates(list):  lista de fechas entre sdate y edate
    """  
    list_dates=pd.date_range(start=sdate,end=edate).strftime("%Y-%m-%d").tolist()

    return list_dates

def date_validate(tipo , fecha_inicio=datetime.datetime.strptime("1111-01-01",'%Y-%m-%d')):
    """ funcion que valida que la fecha ingresada tenga el formato YYYY-MM-DD
        en caso que la fecha ingresa sea de fin, valida que sea mayor a la fecha de inicio
        caso contrario sigue pidiendo la fecha hasta que el formato sea correcto

    Args:
        tipo(str): define si la fecha ingresa la fecha de inicio o de fin
        fecha_inicio: fecha inicio previamente ingresada, se usa para comparar con la fecha fin. 
        (Default: es 1111-01-01 ya que requiere un valor)

    Returns:
        fecha(datetime): con formato YYYY-MM-DD
    """    
    
    #Validación de las fechas
    #Si hay un error entonces devolver mensaje y "continue" nos devuelve al pricipio del try
    
    while True:
        try:
           fecha = datetime.datetime.strptime(input("Ingrese fecha:"), '%Y-%m-%d')
        except ValueError:
            print("Formato Incorrecto, debería ser YYYY-MM-DD")
            continue
        
        if tipo == "fin" and fecha < fecha_inicio:
            
            print("La fecha de fin debe ser mayor a la fecha de inicio\nVuelva a ingresar la fecha de fin:")
            continue
        else:
            return fecha


def validate_if_ticker_exist():
    """ funcion que valida que el ticker ingresado exista, caso contrario sigue pidiendo un nuevo ticker hasta que sea valido

    Args:
        none

    Returns:
        ticker(str): simbolo del ticker
    """    

    while True:
    #Pregunta por el input hasta que la condición se cumple y break el loop


        ticker = input("Ingrese ticker: ")
        url= f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey=03pzZnk6hCLJIOTIB989IXPUlqFEnb70" 
        ticker_value = requests.get(url).json()

        if ticker_value['status']=="OK": 
            print("Ticker Valido")
            break
            
        else:
            print(f"El token {ticker} no es valido, por favor elija otro")
            continue
    
    return ticker

    
        
    
def update_data():
    """ funcion que valida que la respuesta sea 1 o 2 y sigue pidiendo input hasta que se cumpla la condición

    Args:
        menu_type: str con el tipo de menu de donde proviene la elección; usado para re-dirigir en answer_handdler

    Returns:
        anser_handdler(rta, menu_type): función que elije el proximo paso a cumplir según haya sido la rta y el menu donde fue elegida
    """    
    
    
    ############# INGRESO DE DATOS #######################

    
    ticker = validate_if_ticker_exist()

    print("\nIngrese fecha de inicio con formato YYYY-MM-DD")
    tipo = "inicio"
    fecha_inicio = date_validate(tipo)

            #(TO-DO) Validación fecha inicio sea fecha

    print("\nIngrese una fecha de fin con formato YYYY-MM-DD")
    tipo = "fin"
    fecha_fin = date_validate(tipo, fecha_inicio)

            #(TO-DO) Validación que la fecha fin sea mas grande que la inicio + que sea fecha

    list_of_dates = create_list_of_dates(fecha_inicio,fecha_fin)
    #Generate a list of dates that will be used as input for the extract_insert  

    connect_to_sql()

    #This extracts the information from the API and Inserts it into de DB
    extract_insert(token=ticker,datelist=list_of_dates)

    return print("Información fue actualizada")