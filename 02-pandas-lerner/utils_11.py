# utils_11.py - Utility functions for visualizing data in pandas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class CityGrowth:
    def __init__(self, data, states=None):
        """
        Initialize with the raw cities dataframe and two states.
        data: raw pandas DataFrame from cities.json
        states: list of two state names, e.g., ['Texas', 'Michigan']
        """
        
        if states is not None:
            if len(states) != 2:
                raise ValueError("Exactly two states must be provided.")
            self.states = states

        self.raw_data = data
        self.growth_col = 'growth_from_2000_to_2013'
        self.data = self.clean_data()
        self.state_growth = self.compute_weighted_avg_growth()

    def clean_data(self):
        """
        Clean the data: remove NaN/empty growth values, convert growth to numeric.
        """
        growth = self.growth_col
        # Remove rows with NaN or empty growth values
        cleaned = self.raw_data[~self.raw_data[growth].isna() & (self.raw_data[growth] != '')].copy()
        # Convert growth column to numeric
        cleaned[growth] = (
            cleaned[growth]
            .str.rstrip('%')  # Remove trailing '%'
            .astype(float) / 100  # Convert to float and divide by 100
        )
        return cleaned

    def compute_weighted_avg_growth(self):
        """
        Compute weighted average growth per state.
        Returns a DataFrame with total_weighted_growth, total_population, and weighted_avg_growth.
        """
        growth_col = self.growth_col
        # Create weighted growth column
        wg_data = self.data.copy()
        wg_data['weighted_growth'] = wg_data[growth_col] * wg_data['population']

        # Group and sum
        grouped = wg_data.groupby('state')
        total_weighted = grouped['weighted_growth'].sum()
        total_pop = grouped['population'].sum()

        # Compute weighted average
        weighted_avg_growth = total_weighted / total_pop

        # Combine into DataFrame
        state_growth = pd.DataFrame({
            'total_weighted_growth': total_weighted,
            'total_population': total_pop,
            'weighted_avg_growth': weighted_avg_growth
        })
        return state_growth

    def plot_growth(self, bins=20, alpha=0.5, figsize=(8, 4), verbose=False):
        """
        Plot overlapping histograms of growth rates for the two states.
        If verbose=True, print the weighted average growth for each state.
        """
        if verbose:
            # state_growth = self.compute_weighted_avg_growth()
            state_growth = self.state_growth
            for state in self.states:
                if state in state_growth.index:
                    avg_growth = state_growth.loc[state, 'weighted_avg_growth']
                    print(f"Weighted average growth for {state}: {avg_growth:.4f}")
                else:
                    print(f"No data for {state}")

        # Filter data for the two states
        cities_filtered = self.data[self.data['state'].isin(self.states)].copy()
        cities_filtered = cities_filtered.sort_values(by=['state', self.growth_col])

        # Plot
        plt.figure(figsize=figsize)
        sns.histplot(
            data=cities_filtered,
            x=self.growth_col,
            hue='state',
            bins=bins,
            alpha=alpha
        )
        plt.title(f'Growth Rates: {self.states[0]} vs {self.states[1]}')
        plt.show()

    def plot_weighted_avg_growth(self, figsize=(6, 4)):
        """
        Plot a bar chart of the weighted average growth for the two states.
        """
        # Extract state growth data
        state_growth = self.state_growth

        # Compute an average weighted growth for all states
        weighted_avg_growth = state_growth['weighted_avg_growth'].mean()
        # Add a row for 'Average' state
        state_growth.loc['Average'] = [None, None, weighted_avg_growth]

        # Sort by weighted average growth
        state_growth = state_growth.sort_values(by='weighted_avg_growth')

        # Filter 5 states with lowest and 5 states with the highest one
        state_growth = pd.concat([
            state_growth.head(5),
            # Add a row for average state
            state_growth.loc[['Average']],
            state_growth.tail(5)
        ])

        # Define colors: red for negative, blue for non-negative
        def color(val):
            if val == state_growth.loc['Average', 'weighted_avg_growth']:
                return 'green'
            elif val < 0:
                return 'red'
            else:
                return 'blue'
        state_growth['color'] = [color(val) for val in state_growth['weighted_avg_growth']]

        plt.figure(figsize=figsize)
        sns.barplot(
            data=state_growth,
            x='state',
            y='weighted_avg_growth',
            hue='color',
            palette={'red': 'red', 'blue': 'blue', 'green': 'green'},
            legend=False
        )
        plt.title('Weighted Average Growth by State')
        plt.ylabel('Weighted Average Growth')
        plt.xticks(rotation=90)  # Rotate x-axis labels vertically
        plt.show()

class WeatherPlotter:
    def __init__(self, 
                 filenames={
                    'Chicago': 'data/chicago,il.csv', 
                    'Los Angeles': 'data/los+angeles,ca.csv',
                    'Boston': 'data/boston,ma.csv'
                 }, 
                 usecols=[0, 1, 2], 
                 new_names=['date_time', 'max_temp', 'min_temp']):
        """
        Initialize with the weather data filename and column indices.
        filename: path to the CSV file containing weather data.
        usecols: list of column indices to use, default [0, 1, 2].
        """
        # Store parameters
        self.filenames = filenames
        self.usecols = usecols
        self.new_names = new_names

        # Pre-load all cities and combined
        self.chicago = self.load_city('Chicago')
        self.la = self.load_city('Los Angeles')
        self.boston = self.load_city('Boston')
        self.combined = self.combine()

    def load_city(self, city_name):
        """
        Load weather data for a specific city.
        city_name: 'Chicago', 'Los Angeles', or 'Boston'
        """

        df = pd.read_csv(self.filenames[city_name], 
                         usecols=self.usecols, 
                         header=0, 
                         names=self.new_names,
                         parse_dates=['date_time'])
        return df

    def combine(self):
        """
        Combine the loaded city DataFrames into one with a 'city' column.
        """
        chicago = self.chicago.copy()
        la = self.la.copy()
        boston = self.boston.copy()

        chicago['city'] = 'Chicago'
        la['city'] = 'Los Angeles'
        boston['city'] = 'Boston'

        combined = pd.concat([chicago, la, boston], ignore_index=True)
        return combined

    def get_averages(self):
        """
        Calculate mean and median for min_temp and max_temp for each city.
        Returns a DataFrame with stats as rows and cities as columns.
        """
        # Group by city and compute mean/median for min_temp and max_temp
        stats = self.combined.groupby('city').agg({
            'min_temp': ['mean', 'median'],
            'max_temp': ['mean', 'median']
        })
        
        # Flatten column names
        stats.columns = ['min_temp_mean', 'min_temp_median', 'max_temp_mean', 'max_temp_median']
        
        # Transpose to have stats as rows and cities as columns
        stats = stats.T
        return stats

    def plot_min_temp(self, figsize=(10, 6)):
        """
        Create a line plot of minimum temperatures for each city.
        x-axis: dates, y-axis: temperatures, lines: different cities.
        """
        plt.figure(figsize=figsize)
        sns.lineplot(data=self.combined, x='date_time', y='min_temp', hue='city')
        plt.title('Minimum Temperatures by City')
        plt.xlabel('Date')
        plt.ylabel('Minimum Temperature (°C)')
        plt.legend(title='City')
        plt.show()

class NYCTaxiPlotter:
    def __init__(self):
        """
        Initialize with filenames, usecols, and parse_dates.
        Loads and combines the taxi data into self.taxi.
        """
        # Set defaults
        self.filenames = ['data/nyc_taxi_2019-01.csv', 'data/nyc_taxi_2019-07.csv',
                         'data/nyc_taxi_2020-01.csv', 'data/nyc_taxi_2020-07.csv']

        self.usecols = ['tpep_pickup_datetime', 'passenger_count', 'trip_distance',
                            'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
                            'improvement_surcharge', 'total_amount', 'congestion_surcharge']

        self.date_cols = ['tpep_pickup_datetime']
        self.date_col = self.date_cols[0]
        self.years = [2019, 2020]
        self.months = [1, 7]  # January and July 

        # Load and combine the taxi data
        self.taxi = self._load_and_combine()

    def _load_and_combine(self):
        """
        Load each taxi CSV file and concatenate into a single DataFrame.
        """
        dfs = [
            pd.read_csv(filename, 
                        usecols=self.usecols, 
                        parse_dates=self.date_cols)
            for filename in self.filenames
        ]
        
        combined = pd.concat(dfs, ignore_index=True)
        return self._clean_data(combined)

    def _clean_data(self, df):
        """
        Clean the data by keeping only rides in months 1 (January) or 7 (July).
        """
        df = df.dropna(subset=[self.date_col])
        df = df[df[self.date_col].dt.year.isin(self.years)]
        df = df[df[self.date_col].dt.month.isin(self.months)]
        return df

    def plot_rides_bar(self):
        """
        Plot bar plot of rides by year and month    .
        """
        df = self.taxi.copy()
        df['year'] = df[self.date_cols[0]].dt.year
        df['month'] = df[self.date_cols[0]].dt.month.map({1: 'January', 7: 'July'})
        rides = df.groupby(['year', 'month']).size().reset_index(name='ride_count')
        plt.figure(figsize=(6, 3))
        sns.barplot(data=rides, x='month', y='ride_count', hue='year', 
                    palette={2019: 'skyblue', 2020: 'salmon'})
        plt.title('Rides by Year and Month (Bar)')
        # Remove x label (it is clear from the tick labels)
        plt.gca().set_xlabel('')
        plt.ylabel('Number of Rides, in millions')
        plt.legend(title='Year')
        plt.show()

    def plot_amount_paid_bar(self):
        """
        Plot bar plot of the total amount paid by year and month.
        """

        # Prepare data for plotting
        df = self.taxi.copy()
        df['year'] = df[self.date_cols[0]].dt.year
        df['month'] = df[self.date_cols[0]].dt.month.map({1: 'January', 7: 'July'})
        amounts = df.groupby(['year', 'month'])['total_amount'].sum().reset_index(name='total_paid')

        # Plot bar plot of total amount paid
        plt.figure(figsize=(6, 3))
        sns.barplot(data=amounts, x='month', y='total_paid', hue='year',
                    palette={2019: 'skyblue', 2020: 'salmon'})
        plt.title('Total Amount Paid by Year and Month (Bar)')
        # Remove x label (it is clear from the tick labels)
        plt.gca().set_xlabel('')
        plt.ylabel('Total Amount Paid, in millions')
        plt.legend(title='Year')
        plt.show()

    def plot_fare_components_stacked(self, figsize=(8, 3)):
        """
        Plot stacked bar of fare components by year and month.
        """
        df = self.taxi.copy()
        df['year'] = df[self.date_cols[0]].dt.year
        df['month'] = df[self.date_cols[0]].dt.month.map({1: 'Jan', 7: 'Jul'})
        
        # Aggregate sums per year/month
        fair_components = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount']
        components = df.groupby(['year', 'month'])[fair_components].sum().reset_index()
        components[fair_components] /= 1e6  # Scale down for better readability
        components = components.set_index(['year', 'month'])
        print(components)

        # Pivot for stacking (optional, but helps with plotting)
        components.plot.bar(
            stacked=True, figsize=figsize, colormap='summer', alpha=0.75
        )
        plt.title('Fare Components by Year and Month (Stacked)')

        # plt.gca().set_xlabel('')
        # plt.xlabel('Year-Month')
        # Modify x-tick labels to show year-month
        labels = [f"{row['year']}-{row['month']}" for _, row in components.reset_index().iterrows()]
        plt.xticks(ticks=range(len(labels)), labels=labels, rotation=0)

        plt.ylabel('Amount (in millions $)')
        plt.legend(title='Component')
        plt.show()

    def plot_fare_per_passenger(self, figsize=(6, 3)):
        """
        Plot fare amount per passenger count.
        """
        df = self.taxi.copy()
        df['fare_per_passenger'] = df['fare_amount'] / df['passenger_count']
        fare_per_passenger = df['passenger_count'].value_counts().sort_index() / 1e6  # Scale down for better readability

        plt.figure(figsize=figsize)
        sns.barplot(x=fare_per_passenger.index, y=fare_per_passenger.values, color='green', alpha=0.6)
        plt.title('Fare Amount per Passenger Count')
        plt.xlabel('Passenger Count')
        plt.ylabel('Fare Amount (in millions $)')
        plt.show()

    def plot_tip_percentage_hist(self, bins=30, binrange=(0, 50), figsize=(6, 3)):
        """
        Plot histogram of tip percentages.
        """
        df = self.taxi.copy()
        df = df[df['fare_amount'] > 0].copy()
        df = df.dropna(subset=['fare_amount', 'tip_amount'])

        df['tip_percentage'] = (df['tip_amount'] / df['fare_amount']) * 100

        plt.figure(figsize=figsize)
        sns.histplot(df['tip_percentage'], bins=bins, binrange=binrange)
        plt.title('Histogram of Tip Percentages')
        plt.xlabel('Tip Percentage (%)')
        plt.ylabel('Number of Rides')
        plt.show()

    def plot_average_distance_per_day(self, month=7, year=2020, figsize=(6, 3), debug=False):
        """
        Create a bar plot, showing the average distance traveled per day of the week in July 2020.
        The x axis shows the name of each day.
        """
        # Maps day numbers to names and vice versa
        numday_to_name = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                           4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        name_to_numday = {v: k for k, v in numday_to_name.items()}

        # Filter data for the specified month and year
        df = self.taxi.copy()
        mask = (df[self.date_col].dt.year == year) & (df[self.date_col].dt.month == month)
        df = df[mask].copy()

        # Compute average distance per day of the week
        df['day_of_week'] = df[self.date_col].dt.day_name().map(name_to_numday)
        avg_distance = df.groupby('day_of_week')['trip_distance'].mean().sort_index()
        avg_distance.index = avg_distance.index.map(numday_to_name)
        avg_distance.name = 'avg_distance'

        if debug:
            print(avg_distance)

        # Plot bar plot
        plt.figure(figsize=figsize)
        sns.barplot(x=avg_distance.index, y=avg_distance.values, color='green', alpha=0.6)
        plt.title(f'Average Distance Traveled per Day')
        # Remove x label (it is clear from the tick labels)
        plt.gca().set_xlabel('')
        # plt.xlabel('Day of the Week')
        plt.ylabel('Average Distance (miles)')
        plt.xticks(rotation=90)

    def plot_scatter(self, 
                    month=7, year=2020, low=0, 
                    high=500, figsize=(6, 3), alpha=0.5,
                    cols_of_interest=('trip_distance', 'total_amount')
                    ):
        """
        Plot scatter plot of trip_distance vs total_amount for a given month and year,
        filtered by distance and amount ranges.
        """
        dist_col, amount_col = cols_of_interest
        columns_of_interest = [dist_col, amount_col]
        
        # Copy the data
        df = self.taxi.copy()
        
        # Filter out rows for the given month and year
        mask_date = (df[self.date_col].dt.year == year) & (df[self.date_col].dt.month == month)
        df = df[mask_date][columns_of_interest]
        
        # Filter out rows within the given range
        mask_range = (df[dist_col].between(low, high)) & (df[amount_col].between(low, high))
        df = df[mask_range]
        
        # Create the scatter plot
        df.plot.scatter(x=dist_col, y=amount_col, figsize=figsize, alpha=alpha)

        # Extract the title and labels from the columns_of_interest
        title = f'{dist_col.replace("_", " ").title()} vs {amount_col.replace("_", " ").title()}'
        xlabel = dist_col.replace("_", " ").title() + ' (miles)'
        ylabel = amount_col.replace("_", " ").title() + ' ($)'
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

class CorrFinder:
    def __init__(self,
                 
                 wti_filename='data/wti-daily.csv',
                 wti_date_col='Date',
                 wti_new_names=['date', 'oil'],

                 ice_cream_filename='data/ice-cream.csv',
                 ice_cream_date_col='DATE',
                 ice_cream_new_names=['date', 'icecream'],
                 ice_cream_value_col='icecream',

                 miles_filename='data/miles-traveled.csv',
                 miles_date_col='DATE',
                 miles_new_names=['date', 'miles'],

                 index_col='date'

                 ):
        
        # Index column
        self.index_col = index_col
        
        # Load wti data
        self.wti_filename = wti_filename
        self.wti_date_col = wti_date_col
        self.wti_new_names = wti_new_names
        self.oil = self._load_data(self.wti_filename, self.wti_date_col, self.wti_new_names)

        # Load ice cream data
        self.ice_cream_filename = ice_cream_filename
        self.ice_cream_date_col = ice_cream_date_col
        self.ice_cream_new_names = ice_cream_new_names
        self.ice_cream_value_col = ice_cream_value_col
        self.ice_cream = self._load_data(self.ice_cream_filename, self.ice_cream_date_col, self.ice_cream_new_names)
        self.ice_cream = self._convert_to_digits(self.ice_cream, self.ice_cream_value_col)

        # Load miles traveled data
        self.miles_filename = miles_filename
        self.miles_date_col = miles_date_col
        self.miles_new_names = miles_new_names
        self.miles = self._load_data(self.miles_filename, self.miles_date_col, self.miles_new_names)

        # Combine all three datasets
        self.combined = self._combine()

    def _load_data(self, filename, date_col, new_names):
        """
        Load WTI daily data from CSV file.
        """
        df = pd.read_csv(filename,
                         parse_dates=[date_col])
        df.columns = new_names
        df = df.set_index(self.index_col)
        return df
    
    def _convert_to_digits(self, df, col):
        """
        Convert a column to numeric, coercing errors to NaN.
        """
        mask_digits = df[col].str.match(r'^\d+(\.\d+)?$')
        df = df[mask_digits].copy()
        df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    
    def _combine(self):
        """
        Combine the three datasets on the date index.
        """
        combined = self.oil.join(self.ice_cream, how='inner').join(self.miles, how='inner')
        return combined
    
    def correlation_matrix(self, precision=4):
        """
        Compute and return the correlation matrix of the combined dataset.
        precision: number of decimal places to round to (default 4).
        """
        return self.combined.corr().round(precision)
    
    def plot_scatter(self, x_col, y_col, figsize=(6, 3), alpha=0.5):
        """
        Plot a scatter plot of two specified columns from the combined dataset.
        x_col: column name for x-axis
        y_col: column name for y-axis
        """
        plt.figure(figsize=figsize)
        sns.scatterplot(data=self.combined, x=x_col, y=y_col, alpha=alpha)
        plt.title(f'Scatter Plot of {x_col} vs {y_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()

    def correlation_with_months(self):
        """
        Compute correlation of each column with the month extracted from the date index.
        Returns a Series with correlation values.
        """
        df = self.combined.copy()
        df['month'] = df.index.month
        return df.corr().round(4)

class NYCTaxiPlotterSeaborn:

    def __init__(self, both_years=False, trip_length=False):
        """
        Initialize with filenames, usecols, and parse_dates for 2020 data only.
        Loads, cleans, and subsets the taxi data into self.taxi and self.taxi_toy.
        """
        # Set defaults for 2020 only
        self.filenames = ['data/nyc_taxi_2020-01.csv', 'data/nyc_taxi_2020-07.csv']
        if both_years:
            self.filenames = ['data/nyc_taxi_2019-01.csv', 'data/nyc_taxi_2019-07.csv',
                              'data/nyc_taxi_2020-01.csv', 'data/nyc_taxi_2020-07.csv']

        self.usecols = ['tpep_pickup_datetime', 'passenger_count', 'trip_distance', 'total_amount']
        self.passenger_count = np.arange(1, 7)  # Valid passenger counts from 1 to 6

        self.date_cols = ['tpep_pickup_datetime']
        self.date_col = self.date_cols[0]
        self.years = [2020]
        if both_years:
            self.years = [2019, 2020]
        self.months = [1, 7]  # January and July

        # Load and combine the taxi data
        self.taxi = self._load_and_combine()

        # Create tiny subset
        np.random.seed(0)
        self.taxi_toy = self.taxi.sample(frac=0.01)
        self.taxi_toy = self.taxi_toy.reset_index(drop=True)

    def _load_and_combine(self):
        """
        Load each taxi CSV file and concatenate into a single DataFrame.
        """
        dfs = [
            pd.read_csv(filename, 
                        usecols=self.usecols, 
                        parse_dates=self.date_cols)
            for filename in self.filenames
        ]
        
        combined = pd.concat(dfs, ignore_index=True)
        combined = self._clean_data(combined)
        combined = self._add_date_columns(combined)
        if 'trip_distance' in combined.columns:
            combined = self._add_trip_length_column(combined)
        return combined

    def _clean_data(self, df):
        """
        Clean the data by keeping only rides in 2020, months 1 (January) or 7 (July).
        Reset index after cleaning.
        """
        df = df.dropna(subset=[self.date_col])
        df = df[df[self.date_col].dt.year.isin(self.years)]
        df = df[df[self.date_col].dt.month.isin(self.months)]

        # Keep only valid passenger counts
        df = df[df['passenger_count'].isin(self.passenger_count)]

        # Reset index after cleaning
        df = df.reset_index(drop=True)

        return df
    
    def _add_trip_length_column(self, df):
        """
        Add 'trip_length' column to the DataFrame based on 'trip_distance'.
        Categories:
        - Short: <= 2 miles
        - Medium: > 2 and <= 10 miles
        - Long: > 10 miles
        """
        conditions = [
            (df['trip_distance'] <= 2),
            (df['trip_distance'] > 2) & (df['trip_distance'] <= 10),
            (df['trip_distance'] > 10)
        ]
        choices = ['Short', 'Medium', 'Long']
        df['trip_length'] = np.select(conditions, choices, default='Unknown')
        return df

    def _add_date_columns(self, df):
        """
        Add 'year', 'month', 'day' columns to the DataFrame.
        """
        df['year'] = df[self.date_col].dt.year
        df['month'] = df[self.date_col].dt.month
        df['day'] = df[self.date_col].dt.day
        return df

    def plot_relplot_scatter(self, x_col, y_col, toy=True):
        """
        Plot scatter plot using relplot with specified x and y columns.
        If toy=True, use the 1% sample; else use full data.
        """
        df = self.taxi_toy if toy else self.taxi
        sns.relplot(data=df, x=x_col, y=y_col, 
                    hue='passenger_count', alpha=0.5,
                    palette='summer')
        plt.title(f'{x_col} vs {y_col}')
        plt.show()

    def plot_relplot_line(self, x_col, y_col, hue=None, toy=True, data=None):
        """
        Plot line plot using relplot with specified x and y columns.
        If toy=True, use the 1% sample; else use full data.
        """
        df = data.copy() if data is not None else (self.taxi_toy if toy else self.taxi)

        if hue is None:
            sns.relplot(data=df, x=x_col, y=y_col, 
                        kind='line',  
                        alpha=0.5, errorbar=None,
                        palette='winter')
        else:
            sns.relplot(data=df, x=x_col, y=y_col, 
                        kind='line', hue=hue,
                        alpha=0.5, errorbar=None,
                        palette='winter')
        plt.title(f'{x_col} vs {y_col}')
        plt.show()