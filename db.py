import pickle

import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def createHotelDict(df, hotelnames):
	cat_df = df.select_dtypes(exclude=['object', 'bool']).copy()
	cat_df = cat_df.drop(columns=['deptDateYear', 'deptDateMonth', 'deptDateDay', 'retDateYear', 'retDateMonth', 'retDateDay'], axis=1)
	columns = list(cat_df.columns)
	hotel_dict = {}
	for name, row in zip(hotelnames, df.iterrows()):
		if name not in hotel_dict.keys():
			cols = []
			for col in columns:
			#	cols.update({col:row[1][col]})
				cols.append(row[1][col])
			instance = [cols]
			hotel_dict.update({name: instance})
	return hotel_dict

def createDatesDict(df):
	dates_dict = {'deptDateYear': [], 'deptDateMonth': [], 'deptDateDay': [], 'retDateYear': [], 'retDateMonth': [],
				  'retDateDay': []}
	date_tuple = zip(df.get('departureDate'), df.get('returnDate'))
	for dDate, rDate in date_tuple:
		dates_dict.get('deptDateYear').append(dDate.year)
		dates_dict.get('deptDateMonth').append(dDate.month)
		dates_dict.get('deptDateDay').append(dDate.day)
		dates_dict.get('retDateYear').append(rDate.year)
		dates_dict.get('retDateMonth').append(rDate.month)
		dates_dict.get('retDateDay').append(rDate.day)
	return dates_dict

def createInstance(hotelname, departureDate, returnDate):
	pass

def stripDate(date):
	datelist = date.split('-')
	return int(datelist[0]), int(datelist[1]), int(datelist[2])

def createConnection(host, username, password, db, charset, cursorclass):
	return pymysql.connect(host=host,user=username,password=password,db=db,charset=charset, cursorclass=cursorclass)

def getDfFromSql(sql_query, connection):
	return pd.read_sql(sql=sql_query, con=connection)

def main():
	db = createConnection(host='localhost', username='root', password='', db='sanapi', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	# connection = db.cursor()
	
	#df_hotels = pd.read_csv("../data/append.csv")
	df_hotels = getDfFromSql(sql_query="SELECT * FROM sandata", connection=db)

	# Filter out the data to be consist of only numerical values
	cat_df_hotels = df_hotels.select_dtypes(exclude=['object', 'bool']).copy()

	# Separate boolean values, convert into integer (0,1)
#	cat_df_hotels_bool = df_hotels.select_dtypes(include=['bool']).copy().astype(int)

	# Replace categorical data on bestOfferidmealType with corresponding numerical data
	mealTypeLabels = df_hotels['bestOfferidmealType'].astype('category').cat.categories.tolist()
	replace_map_comp = {'bestOfferidmealType': {k: v for k, v in zip(mealTypeLabels, list(range(1, len(mealTypeLabels) + 1)))}}
	df_hotels_replace = df_hotels.copy()
	df_hotels_replace.replace(replace_map_comp, inplace=True)
	bestOfferidMealType_df = pd.DataFrame({'bestOfferidmealType': df_hotels_replace['bestOfferidmealType']})
	result = pd.concat([cat_df_hotels, bestOfferidMealType_df], ignore_index=False, axis=1)

	dates_dict = createDatesDict(df_hotels)
	dates_df = pd.DataFrame(data=dates_dict)
	result = pd.concat([result, dates_df], ignore_index=False, axis=1)

	# target column
	y = result.pop('bestOfferidpricePerNight')
	result = result.drop(['hindex'], axis=1)
	# data to be trained on
	X = result
#	print(X.info())
	# split the data into train and test data (0.7 / 0.3)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)
	# Linear Regression model
	reg = LinearRegression()
	# fit Linear Regression
	fit = reg.fit(X_train, y_train)
	predictions = reg.predict(X_test)
	lin_mse = mean_squared_error(predictions, y_test)
	print("Computed error:", lin_mse)
	# accuracy
	A = reg.score(X_test, y_test)
	print("Accuracy:", A * 100, '%')

	hotelname = "Crystal Palace Luxury Resort & Spa - Ultra All Inclusive"
	departureDate = '2022-09-12'
	returnDate = '2022-09-17'
	departureDate_yy, departureDate_mm, departureDate_dd = stripDate(departureDate)
	returnDate_yy, returnDate_mm, returnDate_dd = stripDate(returnDate)
	hotelnames = df_hotels.get('hotelname')
	mydict = createHotelDict(result, hotelnames)
	d = mydict.get(hotelname)
	d[0].extend([departureDate_yy, departureDate_mm, departureDate_dd, returnDate_yy, returnDate_mm, returnDate_dd])
	print(d[0])
	print(reg.predict(d))
	return reg.predict(d)

if __name__ == '__main__':
	prediction = main()
#trained_model = pickle.dumps(reg)
	# sql = "insert into predictions values (%s,%s,%f)"
#conn = db.cursor()
#conn.execute(sql, (1, 'Linear_Regression', trained_model,))

