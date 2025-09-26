import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


class Restaurant:

    # Column names
    # Customers: ID,First Name,Last Name,Gender,Company,Occupation
    ID = 'ID'
    CUSTOMER_ID = 'Customer ID'
    FIRST_NAME = 'First Name'
    LAST_NAME = 'Last Name'
    GENDER = 'Gender'
    COMPANY = 'Company'
    OCCUPATION = 'Occupation'

    # Food ID,Food Item,Price
    FOOD_ID = 'Food ID'
    FOOD_ITEM = 'Food Item'
    PRICE = 'Price'

    # Customer ID,Food ID
    CUST_FOOD_ID = 'Customer ID,Food ID'

    def __init__(self, 
                 customers_filepath='data/customers.csv',
                 food_filepath='data/foods.csv',
                 week1_filepath='data/week_1_sales.csv',
                 week2_filepath='data/week_2_sales.csv',
                 preserve_index=False):  # Preserve index when concatenating weeks

        # Default parameters
        self.customers_filepath = customers_filepath
        self.food_filepath = food_filepath
        self.week1_filepath = week1_filepath
        self.week2_filepath = week2_filepath
        self.preserve_index = preserve_index

        # Load the DataFrames
        self.customers = self._load_customers()
        self.food = self._load_food()
        self.week1 = self._load_week1()
        self.week2 = self._load_week2()
        self.weeks = self._concat_weeks()

    def _load_customers(self):
        df = pd.read_csv(self.customers_filepath)
        return df
    
    def _load_food(self):
        df = pd.read_csv(self.food_filepath)
        return df
    
    def _load_week1(self):
        df = pd.read_csv(self.week1_filepath)
        return df

    def _load_week2(self):
        df = pd.read_csv(self.week2_filepath)
        return df
    
    def _concat_weeks(self):
        if self.preserve_index:
            df = pd.concat([self.week1, self.week2], 
                           ignore_index=False,
                           keys=['Week 1', 'Week 2'])
        else:   
            df = pd.concat([self.week1, self.week2], 
                        ignore_index=True)
        return df