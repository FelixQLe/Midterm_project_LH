def classify(num):
    """This function classifies delay into five sections
    to make it easier to understand delay time distribution """
    if (num < 0):
        if (num < -30):
          return ('Early: > 30 mins') 
        else:
          return ('Early: < 30 mins')
    else:
        if (num < 30):
          return ('Late: < 30 mins')
        elif (num < 250):
          return ('Late: < 5 hours')
        else:
          return ('Late: > 5 hours')

def write_csv(df, name):
    """
    - make a csv file if not exit with data file and name
    
    - df.to_csv('origin_cities.csv', index=False)
    """
    return df.to_csv(name, index=False)

def weather_f(dict_cities,df_weather, apikey, csv_name):
    
    """
    - send requests to weatherapis to get weather conditions
       according to locations and dates params
    
    - write csv file df_weather, include date, city, condition
    - csv_name will be the name of output file
    """
    
    import requests
    import json
    
    
    index = 0

    for date, cities in dict_cities.items():
        for city in cities:       
            url = f'http://api.weatherapi.com/v1/history.json?key={apikey}&q={city}&dt={date}'
            res = requests.get(url)
            res = res.json()
            condition = res['forecast']['forecastday'][0]['day']['condition']['text']
            df_weather.iloc[index] = [date, city, condition]
            index += 1
            
    #return df_weather
    return write_csv(df_weather, csv_name)
    
    
def format_air_time(hours):
    """
    format the air_time,e.g 134 to 214(2hour14mins)
    """
    import datetime
    hour = int(hours)//60
    if hour == 0:
        mins = int(hours)
        #hours = str(hour)+str(mins)
        if len(str(mins)) == 1:
            Hourmin = str(hour)+str(0)+str(mins)
        else:
            Hourmin = str(hour)+str(mins)
    else:
        mins = int(hours)-60*int(hour)
        if len(str(mins)) == 1:
            Hourmin = str(hour)+str(0)+str(mins)
        else:
            Hourmin = str(hour)+str(mins)
    return Hourmin

def to_int_hour(hours):
    """
    calcualte the int to integer hour,e.g 795 to 835(8:35)
    """
    import datetime
    hours = "{0:04d}".format(int(hours))
    if int(hours[2:4]) >= 60:
        mins = int(hours[2:4]) - 60
        hour = int(hours[0:2]) + 1
        if len(str(mins)) == 1:
            Hourmin = str(hour)+str(0)+str(mins)
        else:
            Hourmin = str(hour)+str(mins)
        #Hourmin = str(hour)+str(mins)
    else:
        Hourmin = hours
    return Hourmin

def TimeFormatted(hours):
    
    import datetime
    """
    using: array.apply(TimeFormatted)
    Changing times from int format into HH:MM format
    """
    if hours == 2400:
        hours = 0
    else:
        hours = "{0:04d}".format(int(hours))
        Hourmin = datetime.time(int(hours[0:2]), int(hours[2:4]))
        return Hourmin

class MultiColumnLabelEncoder:
    """class to transform categories features to label and inverse transform back to categories"""
    def __init__(self, columns=None):
        self.columns = columns # array of column names to encode


    def fit(self, X, y=None):
        from sklearn.preprocessing import LabelEncoder
        self.encoders = {}
        columns = X.columns if self.columns is None else self.columns
        for col in columns:
            self.encoders[col] = LabelEncoder().fit(X[col])
        return self


    def transform(self, X):
        output = X.copy()
        columns = X.columns if self.columns is None else self.columns
        for col in columns:
            output[col] = self.encoders[col].transform(X[col])
        return output


    def fit_transform(self, X, y=None):
        return self.fit(X,y).transform(X)


    def inverse_transform(self, X):
        output = X.copy()
        columns = X.columns if self.columns is None else self.columns
        for col in columns:
            output[col] = self.encoders[col].inverse_transform(X[col])
        return output


