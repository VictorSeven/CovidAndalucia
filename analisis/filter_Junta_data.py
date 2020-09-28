import numpy as np
import pandas as pd
from datetime import date,timedelta


def create_provinces_csv(input_txt_path="../data/aux_updated_series.txt", output_csv_path="../data/datos_andalucia_ultimo.csv"):
    
    #Read file
    fich = open(input_txt_path, 'r') 
    lines = fich.readlines() 
    fich.close()

    #Name of columns
    header = lines[0].replace(" ", "_").replace("\n", "").split("\t")

    #Get last date and how much days have passed since last data
    init_date = date(2020, 2, 26)
    end_date_str = lines[1].split("\t")[0].split("/")
    end_date_str = [int(f) for f in end_date_str]
    end_date = date(end_date_str[2], end_date_str[1], end_date_str[0])

    numdays = (end_date - init_date).days + 1 #+1 so last one is also included



    #Now let's construct the CSV in good format
    all_data = []

    for j in range(numdays):
        today = end_date + timedelta(days=-j)
        
        thisline = [str(today)]
                
        #Append for 8 provinces + total
        for k in range(9):
            thisline = [str(today)] #Date
            
            index = 1 + 9*j+k
            
            #print(index, j, k)
            dataline = lines[index].replace("\n", "").split("\t")[1:]
           
            #print(dataline)
            thisline.append(dataline[0]) #Territory name
            #Numerical data
            for d in dataline[1:]:
                thisline.append(int(d))
            all_data.append(thisline)


    #Construct a DF and sort by date
    df = pd.DataFrame(all_data, columns=header)
    df.set_index("Fecha", inplace=True)
    df.sort_index(inplace=True)

    #Export it
    df.to_csv(output_csv_path)


create_provinces_csv()
