
import sqlite3
import pandas as pd

import matplotlib.pyplot as plt

def resume_function():

    ########## INSERTING INFORMATION ###################
    print("\nGenerando resumen")

    try:

        sqliteConnection = sqlite3.connect('ticket.db')

        sqlite_get_all_rows = ''' SELECT ticker_symbol, MIN(ticker_date) as minDate, MAX(ticker_date) as maxDate
                                    FROM ticket_table
                                    GROUP BY ticker_symbol;'''
        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_get_all_rows)
        found_values = cursor.fetchall() #returns all the rows as a list of tuples
        df = pd.DataFrame.from_records(found_values, columns =['Ticker','From','Until'])


        print("\nLos tickers guardados en la base de datos son:")
        print(df)

        
        cursor.close()

    except sqlite3.Error as error:
            print("Failed to read data from table", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()
                if __name__ == "__main__":
                    print("sqlite connection is closed")


def grafico_de_ticker():

    #Primero: validamos si el ticker esta dentro del archivo.
    #Caso contrario devolvemos "no está guardado"
    try:
        rta =(input("Ingrese un ticker:"),)
        # (a,) saves into a tuple the var a. Tupple consist only of 1 term
        
    except ValueError:

        print("El formato ingresado es incorrecto, pruebe de nuevo")

    try:

        sqliteConnection = sqlite3.connect('ticket.db')

        sqlite_validate_if_exists = ''' SELECT * FROM ticket_table WHERE ticker_symbol=? ORDER BY ticker_date ASC ;'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_validate_if_exists,rta)
        found_values = cursor.fetchall() #returns empty list if nothing found. Else a list of tupples
        
        if len(found_values)==0:
            print("El ticker no está en la base de datos")


    #Segundo: en caso de estar, conectamos con la tabla y hacemos un fetchall para traer todos los datos   
        else:
        #el ticker está en la base de datos
            
            df = pd.DataFrame.from_records(found_values, columns =['ID','Ticker','Date','Price'])
            #get df from list of tuples

    
    #Tercero: usamos pandas para graficas los datos traidos.

            #Making the graph
            plt.plot(df['Date'], df['Price'])
            plt.xticks(rotation='vertical')
            plt.xlabel('Timeline') 
            plt.ylabel('Ticker Price')
            plt.title("Ticker Graph")
            plt.show()


        cursor.close()

    except sqlite3.Error as error:
            print("Failed to read data from table", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()
                if __name__ == "__main__":
                    print("sqlite connection is closed")

    

    
    

    

