import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

class Employees:

    # Column names 
    # First Name	Gender	Start Date	Last Login Time	Salary	Bonus %	Senior Management	Team
    FIRST_NAME = 'First Name'
    GENDER = 'Gender'
    START_DATE = 'Start Date'
    LAST_LOGIN_TIME = 'Last Login Time'
    SALARY = 'Salary'
    BONUS = 'Bonus %'
    SENIOR_MANAGEMENT = 'Senior Management'
    TEAM = 'Team'

    def __init__(self, 
                 filepath='data/Employees.csv',
                 date_format='%m/%d/%Y',
                 time_format='%I:%M %p'):  # To match '8/6/1993'
        
        # Default parameters
        self.filepath = filepath
        self.date_format = date_format
        self.time_format = time_format

        # Load the DataFrame
        self.employees = self._load_data()

    def _load_data(self):
        df = pd.read_csv(
            self.filepath,
            parse_dates=[self.START_DATE],
            date_format={self.START_DATE: self.date_format},
        )

        # Parse 'Last Login Time' to time only
        df[self.LAST_LOGIN_TIME] = pd.to_datetime(
            df[self.LAST_LOGIN_TIME], 
            format=self.time_format,
            errors='coerce'
        ).dt.time

        # Convert 'Senior Management' to boolean
        df['Senior Management'] = df['Senior Management'].astype(bool)

        # Make gender as a category
        df[self.GENDER] = df[self.GENDER].astype('category')
        
        return df


class NETFLIX:

    # Column names: title,director,date_added,type
    TITLE = 'title'
    DIRECTOR = 'director'
    DATE_ADDED = 'date_added'
    TYPE = 'type'

    def __init__(self, 
                 filepath='data/netflix.csv',
                 date_format='%d-%b-%y'):  # To match '15-Apr-17'
        
        # Default parameters
        self.filepath = filepath
        self.date_format = date_format

        # Load the DataFrame
        self.netflix = self._load_data()

    def _load_data(self):
        df = pd.read_csv(
            self.filepath,
            parse_dates=[self.DATE_ADDED],
            date_format={self.DATE_ADDED: self.date_format},
        )

        # Convert 'type' to category
        df[self.TYPE] = df[self.TYPE].astype('category')
        
        return df