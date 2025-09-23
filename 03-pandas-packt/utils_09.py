import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

class Fortune1000:

    # Column names
    COMPANY = 'Company'
    SECTOR = 'Sector'
    INDUSTRY = 'Industry'
    REVENUE = 'Revenue'
    PROFITS = 'Profits'
    EMPLOYEES = 'Employees'

    def __init__(self, 
                 filepath='data/fortune1000.csv'):
        
        # Default parameters
        self.filepath = filepath

        # Load the DataFrame
        self.fortune = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath, index_col="Rank")
        
        return df

class Cereals:

    # Column names
    NAME = 'Name'
    MANUFACTURER = 'Manufacturer'
    TYPE = 'Type'
    CALORIES = 'Calories'
    FIBER = 'Fiber'
    SUGARS = 'Sugars'

    def __init__(self, 
                 filepath='data/cereals.csv'):
        
        # Default parameters
        self.filepath = filepath

        # Load the DataFrame
        self.cereals = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath)
        
        return df