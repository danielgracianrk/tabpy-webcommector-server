import requests
import pandas as pd

keys_csv = ''
first_row_csv = ''

def set_first_row(keys):
    global first_row_csv # Needed to modify global copy of globvar
    first_row_csv = input

def get_first_row():
    global first_row_csv
    return first_row_csv


def set_globvar(keys,first_row):
    global keys_csv  # Needed to modify global copy of globvar
    global first_row_csv
    print(keys)
    print(first_row)
    if keys == "Init":
        keys_csv = keys
    else:
        keys_csv = keys
    first_row_csv = first_row

def get_globvar():
    global keys_csv
    return keys_csv


def get_query_csv(url):
    global first_row_csv
    print("######## VAMONOS KILLO $$$$$")
    url = f'{url.iloc[0]["url"]}'

    response = requests.get(url)
    iter = response.iter_lines()


    set_globvar(next(iter).decode('utf-8').split(';'),next(iter).decode('utf-8').split(';'))

    iter = response.iter_lines()
    a = next(iter)
    data = list()

    for i in iter:
        a = i.decode('utf-8').split(';')
        print(a)
        data.append(i.decode('utf-8').split(';'))
    df = pd.DataFrame(data, columns=get_globvar())
    print(df)
    return df
    #return pd.DataFrame(first_row_csv)


def get_output_schema():
    global keys_csv
    global first_row_csv
    print("#########HOLALA#####")
    if not "keys_csv" in globals():
        set_globvar("Init",'')
    print(globals())
    keys_csv = get_globvar()

    first_row_csv = get_first_row()

    dict = {}


    if keys_csv == 'Init':
        for i in keys_csv:
            dict[i] = prep_string()
    else:
        count = 0
        for i in keys_csv:
            # if first_row_csv[count].isnumeric():
            #     dict[i] = prep_int()
            # else:
            dict[i] = prep_string()
            count = count + 1
    return pd.DataFrame(dict)
