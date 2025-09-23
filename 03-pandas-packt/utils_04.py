import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
import datetime as dt

class JamesBond:

    # Column names
    FILM = 'Film'
    YEAR = 'Year'
    ACTOR = 'Actor'
    DIRECTOR = 'Director'
    BOX_OFFICE = 'Box Office'
    BUDGET = 'Budget'
    BOND_ACTOR_SALARY = 'Bond Actor Salary'

    def __init__(self, 
                 filepath='data/jamesbond.csv'):
        
        # Default parameters
        self.filepath = filepath

        # Load the DataFrame
        self.bond = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath)
        
        return df
    
class NFL:

    # Column names: Name,Team,Position,Birthday,Salary
    NAME = 'Name'
    TEAM = 'Team'
    POSITION = 'Position'
    BIRTHDAY = 'Birthday'
    SALARY = 'Salary'

    def __init__(self, 
                 filepath='data/nfl.csv',
                 date_format='%m/%d/%Y'):  # To match '7/21/1983'
        
        # Default parameters
        self.filepath = filepath
        self.date_format = date_format

        # Load the DataFrame
        self.nfl = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath)

        # Convert the birthday column to datetime
        df[self.BIRTHDAY] = pd.to_datetime(df[self.BIRTHDAY], format=self.date_format)

        return df