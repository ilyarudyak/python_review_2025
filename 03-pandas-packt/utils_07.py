import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


class BIGMAC:

    # Column names: Date,Country,Price in US Dollars
    DATE = 'Date'
    COUNTRY = 'Country'
    PRICE = 'Price in US Dollars'

    def __init__(self, 
                 filepath='data/bigmac.csv',
                 index_col=None,
                 round=False,
                 precision=2):
        
        # Default parameters
        self.filepath = filepath
        self.index_col = index_col
        self.round = round
        self.precision = precision

        # Load the DataFrame
        self.bigmac = self._load_data()

    def _load_data(self):
        # Parse dates while reading the CSV file: 2000-04-01
        df = pd.read_csv(self.filepath, 
                         parse_dates=[self.DATE],
                         date_format={self.DATE: '%Y-%m-%d'},
                         index_col=self.index_col)
        if self.round:
            df = df.round(self.precision)
        return df
    
class INVESTMENTS:

    # Column names: Name,Market,Status,State,Funding Rounds
    NAME = 'Name'
    MARKET = 'Market'
    STATUS = 'Status'
    STATE = 'State'
    FUNDING_ROUNDS = 'Funding Rounds'

    def __init__(self, 
                 filepath='data/investments.csv',
                 index_col=["Status", "Funding Rounds", "State"]):
        
        # Default parameters
        self.filepath = filepath
        self.index_col = index_col

        # Load the DataFrame
        self.investments = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.filepath, 
                         index_col=self.index_col)
        df = df.sort_index()
        
        return df