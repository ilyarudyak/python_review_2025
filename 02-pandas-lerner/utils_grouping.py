import pandas as pd
import os

class WeatherDataManager:
    def __init__(self, 
                 data_folder='data', 
                 filenames=[
                     'san+francisco,ca.csv', 
                     'new+york,ny.csv', 
                     'springfield,ma.csv', 
                     'boston,ma.csv', 
                     'springfield,il.csv', 
                     'albany,ny.csv', 
                     'los+angeles,ca.csv', 
                     'chicago,il.csv'
                 ],
                 usecols=[0, 1, 2]
                 ):
        self.data_folder = data_folder
        self.filenames = filenames
        self.usecols = usecols
        self.weather = self.load_weather_data()

    def _extract_city_state(self, filename):
        # Extract city  from the filename and capitalize it
        city_state = filename.replace('.csv', '').replace('+', ' ').split(',')
        city = city_state[0].strip()
        city = city.title() if city else ''

        # Extract state if available and capitalize it
        state = city_state[1].strip() if len(city_state) > 1 else ''
        state = state.upper() if state else ''

        return city, state

    def load_weather_data(self):
        dfs = []
        for fname in self.filenames:
            
            # Read only first three columns
            file_path = os.path.join(self.data_folder, fname)
            df = pd.read_csv(file_path, usecols=self.usecols, parse_dates=[0])
            df.columns = ['date_time', 'max_temp', 'min_temp']

            # Add city and state columns
            city, state = self._extract_city_state(fname)
            df['city'] = city
            df['state'] = state

            # Append the DataFrame to the list
            dfs.append(df)

        # Concatenate all DataFrames into one
        return pd.concat(dfs, ignore_index=True)
