
# Project Name 

Python Program developed as final project for the Python Certification of [ITBA](https://innovacion.itba.edu.ar/institucional/).
The program allows the user to select options from different menus to:
- Get information from API
- Save API information into SQL Lite database
- Get the information saved in the DB an display it
- Get a graph of the information available in the DB.

# Installation 

1. Install [latest version](https://www.python.org/downloads/) of Python.

2. Install a [code editor](https://code.visualstudio.com/Download)  as Visual Studio.

3. Install [SQLI Lite 3](https://www.sqlite.org/download.html)  

4. Download from github the [.zip](https://github.com/fmiriani/python-itba-course/archive/refs/heads/master.zip) and open the folder containing all documents with your code editor.

5. Before running the main.py please go to terminal and use the virtual enviroment located in  the ./env folder.
The virtual enviroment allows you to run the program with all pre-installed modules.

To do so, run the following commmand in your terminal to open the folder where the env folder is located:

```batch
cd C:\Folder\env is located here
```

Then run the command below, which runs the script that allows to start using the virtual enviroment.


```batch
env\Scripts\activate
```

Once you had finished you had deactivate using the command

```batch
deactivate
```

6. Run the [main.py](#mainpy) program in your terminal

# Description 

## **Functionality**



The menu provides the options of:
- Update information from an [API](https://polygon.io/docs/stocks/getting-started) into an SQLlite database

- Interact visualy with the information in the DB. This can be:
    - Getting a [summary](#summary-view) of the information saved into the database.
    - Getting a [graph](#graph) with the information of an specific ticker. 

In each step the user is guided throught menu's that facilitate the interaction.

## **How it works?**

The program has been divided in different .py to simplify the individual testing of each one of them as well as the organization of the program. Below the description of the program functionality:


### **main.py** 





1. Running main.py starts the program, runs the function  <span style="color:yellow">main_menu()</span> that will assign the variable menu_type (which is used understand what is the menu where the option has been selected) and returns <span style="color:yellow">answer_validator()</span>. 

    
    The purpose of this function is to validate if the inputs are valid. It is separeted to keep all validations in one place. This wil help to escalate our function in case our program grows (more menus and more options). (Example: if visual_menu has a new option we can just add the condition of the menu_type and validate the answer "3")

2. <span style="color:yellow">answer_validator()</span> in  [updateData.py](#updatedatapy) continues asking for a valid input and then returns <span style="color:yellow">anser_handdler()</span>. 

    The function <span style="color:yellow">anser_handdler()</span> decides what is the the next step of the program basd on user's answer and the type of menu where the answer is coming from. It has been created separetely to be able to increase the amount of menu's without adding too much complexity to the program.

3. The first options that use can select take us to <span style="color:yellow">update_data()</span> or <span style="color:yellow">visualize_menu()</span>:
    
    - <span style="color:yellow">update_data():</span> allows to select a ticker and dates to get information from API and then insert it into SQL, located in [updateData.py](#updatedatapy) 
    - <span style="color:yellow">visualize_menu():</span> validates the answer and selects the function that performs requested task, this can be <span style="color:yellow">resume_function()</span> or <span style="color:yellow">	grafico_de_ticker()</span>  located in  [visualizeData.py](#visualizedatapy)


4.  After functions in point 3 had finished it takes you to  <span style="color:yellow">exit_menu()</span> that allows the user to continue (goes to <span style="color:yellow">main_menu()</span> ) or to stops the program.

    
    




### **updateData.py** 

Once inside updateData.py <span style="color:yellow">update_data()</span> runs.
This function contains:

- <span style="color:yellow">validate_if_ticker_exist()
:</span> asks the user of ticker input, sends a GET request to the API and validates if status answer is "OK". Will continue asking until getting a valid ticker.

- Then the programs requests the initial date, the format YYYY-MM-DD is is validated with
<span style="color:yellow">date_validate()
</span> 
    and then validates end date with the same function. The end function also has to be greater than start date. In both cases the program will continue asking until valid input is entered.
    
- A list of dates between start date and end date is created with 
<span style="color:yellow">create_list_of_dates()
</span> 
 . The API requires individual dates as parameter, this list will be used to make individual GET requests to the API for each date between start and end date.


```python

token = ticker code
i= individual date
url = f"https://api.polygon.io/v1/open-close/{token}/{i}?adjusted=true&apiKey=03pzZnk6hCLJIOTIB989IXPUlqFEnb70"

```


- Then runs the
<span style="color:yellow">connect_to_sql()
</span> function located in <span style="color:#728FCE">connectSQL.py
</span>  which creates the database and table in case they don't exist. 

- Finally it runs 
<span style="color:yellow">extract_insert()
</span> function located in  [ExtractAndInsert.py](#extractandinsertpy) which makes a GET request to the API using the list of dates created in previous steps and saves them into a tuple. Then, INSERTS into the table only the values that are not duplicated.

- Goes back to [main.py](#mainpy)





### **visualizeData.py** 

We have two function in the program <span style="color:yellow">resume_function()
</span> and <span style="color:yellow">grafico_de_ticker()
</span>

In case the function <span style="color:yellow">resume_function()
</span> gets called:

1.  we connect to the database and SELECT all information in the table GROUPY BY ticker and adding the max and min date of each ticker as column

2. We store this values with fetchall and create a data frame with pandas. To profit from the visual organization and then we print it.

If <span style="color:yellow">grafico_de_ticker()
</span> gets called:

1. We request the ticker input and save in the a tuple to be used on the SQL function.

2. We make a SELECT to validate if the ticker is already in the DB or not. In case values had been found in the DB we store them in a tuple and create a data frame.

3. Using matplotlib.pyplot we define X and Y values, together with other parameters like labels and titles.



### **ExtractAndInsert.py** 

1. The only function in the program is <span style="color:yellow">extract_insert()
</span>. The funciton iterates the full list of dates between start and end date, for the selected ticker.

2. In each iteration we convert the request in a json object and validates what is the status of the answer. In case the answer is not OK returns the reason. NOK answers can be due to exceeding the free API requests or because no information during that date (normally weekends)

3. For the date values where the answer is OK it stores the value in a tuple (because the sql3 execute function requires a tuple). The tuple is saved in a pre-defined order to match the order to match the column order from the SQL function.


4. To INSERT the values into the SQL DB we iterate the tuple with saved values. Before INSERT, we SELECT the values with the same ticker and date to find duplicates and saved them with fetchone() function.

5. In case the value is found we don't INSERT, contrary case we execute the INSERT.


# Visuals 

### **UPDATE FUNCTION:**

Below an image on how the program reacts to the update function when selecting "1.Actualización de datos".

![alt text](/Images/Main_menu_update.JPG)

### **SUMMARY VIEW:**
Below an image of how to program reacts when selecting "2. Visualización de datos" and then "1.Resumen"

![alt text](/Images/main_menu_summary.JPG)

### **GRAPH:**
Below an image of the visualization that the program generates for a given ticker.

![alt text](/Images/tickergraph.JPG)

<!--

| Reference       | Function |
| ----------- | ----------- |
|  m_m()      | main_menu()  |
| a_v()       | answer_validator()        |
| a_h()       | anser_handdler()        |
| u_d()       | update_data()        |
| v_m()       | visualize_menu()       |
| r_f()       | resume_function()       |
| g_t()       | grafico_de_ticker()       |
| e_m()       | exit_menu()     |

<!-- For more about markdown tables 
https://www.markdownguide.org/extended-syntax/ -->



## License 
[MIT](https://choosealicense.com/licenses/mit/)