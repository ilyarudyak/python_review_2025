import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


class FOOD:

    # Column names: First Name,Gender,City,Frequency,Item,Spend
    FIRST_NAME = 'First Name'
    GENDER = 'Gender'
    CITY = 'City'
    FREQUENCY = 'Frequency'
    ITEM = 'Item'
    SPEND = 'Spend'

    def __init__(self, 
                 filepath='data/foods.csv'):
        
        # Default parameters
        self.filepath = filepath

        # Load the DataFrame
        self.foods = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath)
        
        return df
    

class Cars:
    
    # Column names: Manufacturer,Year,Fuel,Transmission,Price
    MANUFACTURER = 'Manufacturer'
    YEAR = 'Year'
    FUEL = 'Fuel'
    TRANSMISSION = 'Transmission'
    PRICE = 'Price'

    def __init__(self, 
                 filepath='data/used_cars.csv'):
        
        # Default parameters
        self.filepath = filepath

        # Load the DataFrame
        self.cars = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath)
        df[self.PRICE] = df[self.PRICE].astype(float)
        
        return df