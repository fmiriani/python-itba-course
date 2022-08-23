import requests
import json
import pandas as pd
import sqlite3


def extract_insert(token,datelist):
    ''' 
    inputs: 
        - datelist: list of dates with format YYYY-MM-DD
        - token: type of symbol required

    process:
        - takes the list of dates and goes thorugh it appending the information if the Status is OK
        - when appending converts the value in tupple with specific order
        - INSERTS in the DB 

    '''


    ############# EXTRACCION DE LA INFORMACION ###########
    print("Extrayendo la información")

    #1- Generar lista vacia
    ticker_list_dates=[]
    columnas = ['symbol','from','close']
    for i in datelist:

        url = f"https://api.polygon.io/v1/open-close/{token}/{i}?adjusted=true&apiKey=03pzZnk6hCLJIOTIB989IXPUlqFEnb70"  
        ticker_value = requests.get(url).json()
        
        if __name__ == "__main__":
            print(f"El dato obtenido es:{ticker_value}")
        #2- Hacer un append the los JSON deseados en la lista vacia
        #   Convertimos cada dictionario en una tupla y lo ordenamos segun el orden en "columnas"
        
        if ticker_value['status']=="ERROR":

            print(f"No hay información de {token} el día {i} debido a que se excedio las requests maximas permitidas")
        
        if ticker_value['status']=="NOT_FOUND":

            print(f"No hay información de {token} el día {i}")

        if ticker_value['status']=="OK":
        #Appending only if the value has been received

            print(f"Cargando información del ticker {token} en el día {i}")
            ticker_list_dates.append(tuple(ticker_value[c] for c in columnas ))
        
        else:
            continue


    #3-Finalmente generar una LISTA de TUPLAS para luego insertar
    if __name__ == "__main__":
        print(f"La lista de tuplas es:\n {ticker_list_dates}")



    ########## INSERTING INFORMATION ###################
    try:

        sqliteConnection = sqlite3.connect('ticket.db')

        sqlite_validate_if_exists = ''' SELECT * FROM ticket_table WHERE (ticker_symbol=? AND ticker_date=? AND close_value=?);'''
        
        sqlite_insert = '''INSERT INTO ticket_table (ticker_symbol,ticker_date,close_value)
                                    VALUES(?,?,?);'''

        cursor = sqliteConnection.cursor()
        if __name__ == "__main__":
            print("Successfully Connected to SQLite")

        for i in range(0,len(ticker_list_dates),1):
        #Insertamos todas los datos de la tupla
        
            cursor.execute(sqlite_validate_if_exists,ticker_list_dates[i])
            found_values = cursor.fetchone()
            #Genera una query donde valida si existe la row que vamos a insert
            #En caso que exista, no inserta. 

            if found_values is None:
                cursor.execute(sqlite_insert,ticker_list_dates[i])
                if __name__ == "__main__":
                    print("Row inserted")
            else:
                if __name__ == "__main__":
                    print("Row already existed")
        
        
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
            print("Error while inserting a row", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()
                if __name__ == "__main__":
                    print("sqlite connection is closed")
