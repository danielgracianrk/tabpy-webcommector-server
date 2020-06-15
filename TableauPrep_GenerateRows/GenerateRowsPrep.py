import pandas as pd
import numpy as np
import requests



def getTheQuery(url):
	url = "https://api.instarsuite.com/norwaytvov/IADS.asmx/GetData?iads_params=name:NRK-NO-API-1;password:wySGA3M9h;idLang:EN;idApp:3000;outformat:CSV;skipmetadata:1&tq=SELECT TOP 10 INGR_CHANNELS.ATTR_NAME, CALC_DPS.UNIT_RTG, CALC_DPS.UNIT_RTGPCT, CALC_DPS.UNIT_SHR FROM CALC_DPS, INGR_CHANNELS WHERE INGR_CHANNELS.ATTR_ID LIKE '1:%' ORDER  BY CALC_DPS.UNIT_RTG DESC LIMIT 300 OFFSET 0&tqx=reqId:9"
	response = requests.get(url)
	print(response)
	return response

def GenerateRowsPrep(df):


	getTheQuery("lala")

	# Generate the number of rows per invoice months
	inv_months = df[['Invoice_Number', 'DateDiffMonths']]
	inv_months = np.repeat(inv_months.Invoice_Number,inv_months.DateDiffMonths)

	# Merge with original dataset to explode rows
	df = pd.merge(df, inv_months, how = 'left', on = 'Invoice_Number')

	# Group by invoice number and running count of months to add
	df["MonthsToAdd"] = df.groupby(['Invoice_Number']).cumcount()
	df["danielo"] = "hello"
	# Spread revenue
	df.Value = df.Value/df.DateDiffMonths

	return(df)


def get_output_schema():
 	return pd.DataFrame({
 			'Customer_Name' : prep_string(),
 			'Invoice_Number' : prep_int(),
 			'Product' : prep_string(),
 			'Invoice_Start' : prep_date(),
 			'Invoice_End' : prep_date(),
 			'Value' : prep_decimal(),
 			'MonthsToAdd' : prep_int(),
			'danielo' : prep_string()
 		})


df = pd.DataFrame(['Invoice_Number', 'DateDiffMonths'])
GenerateRowsPrep(df)
