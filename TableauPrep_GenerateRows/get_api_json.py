import requests
import pandas as pd
import json
import datetime
from datetime import timedelta, date


keys_csv = ''
first_row_json = ''


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def set_first_row(input):
    global first_row_json # Needed to modify global copy of globvar
    first_row_json = input

def get_first_row():
    global first_row_json
    return first_row_json

def set_globvar(input):
    global keys_json  # Needed to modify global copy of globvar
    global first_row_json
    print(input)
    if input == "Init":
        keys_json = input
    else:
        keys_json = input.keys()
    first_row_json = input


def get_globvar():
    global keys_json
    return keys_json

def get_query_json(url):
    url = f'{url.iloc[0]["url"]}'
    response = requests.get(url)
    response = json.loads(response.text)
    set_globvar(response[0])
    #set_first_row(response["referrals"][0])
    data = list()
    for item in response:
        data.append(item)
    # set_globvar(next(iter).decode('utf-8').split(';'))
    # print(pd.DataFrame(data, columns=get_globvar()))
    #print(pd.DataFrame(data, columns=get_globvar()))
    print( pd.DataFrame(data, columns=get_globvar()))
    return pd.DataFrame(data, columns=get_globvar())

def get_for_2020(url):
    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 31)
    data = list()
    global_var = False
    for single_date in daterange(start_date, end_date):
        url_ini = "https://datahub-api-varnish.intern-we.drift.azure.nrk.cloud/v1/service/sorted-list?id=nrkno&from="
        url_ini = url_ini + single_date.strftime("%Y-%m-%d")+"T00%3A00%3A00Z&to="+single_date.strftime("%Y-%m-%d")+"T23%3A00%3A00Z&sort=desc&limit=1000"
        print(url_ini)

    #url_ini = "https://datahub-api-varnish.intern-we.drift.azure.nrk.cloud/v1/service/sorted-list?id=nrkno&from=2020-04-21T22%3A00%3A00Z&to=2020-05-21T23%3A00%3A00Z&sort=asc&limit=100"

        response = requests.get(url_ini)
        response = json.loads(response.text)
        if not global_var:
            set_globvar(response[0])
            global_var = True
    #set_first_row(response["referrals"][0])
        for item in response:
            data.append(item)
    # set_globvar(next(iter).decode('utf-8').split(';'))
    # print(pd.DataFrame(data, columns=get_globvar()))
    #print(pd.DataFrame(data, columns=get_globvar()))

    print(data)
    print( pd.DataFrame(data, columns=get_globvar()))
    return pd.DataFrame(data, columns=get_globvar())

def get_output_schema():
    print("INIT")
    if not "keys_json" in globals():
        set_globvar("Init")

    keys_json = get_globvar()
    #keys = ['INGR_CHANNELS.ATTR_NAME', 'CALC_DPS.UNIT_RTG', 'CALC_DPS.UNIT_RTGPCT', 'CALC_DPS.UNIT_SHR']
    first_row_json = get_first_row()
    dict = {}

    if keys_json == 'Init':
        for i in keys_json:
            dict[i] = prep_string()
    else:
        for i in keys_json:
            if i == "from":
                dict[i] = prep_datetime()
            elif i == "to":
                dict[i] = prep_datetime()
            elif i == "published":
                dict[i] = prep_datetime()

            elif isinstance(first_row_json[i], int):
                dict[i] = prep_int()
            elif isinstance(first_row_json[i], float):
                dict[i] = prep_decimal()
            else:
                dict[i] = prep_string()

    return pd.DataFrame(dict)

#get_for_2020(222)
