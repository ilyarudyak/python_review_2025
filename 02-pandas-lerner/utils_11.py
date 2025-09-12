# utils_11.py - Utility functions for visualizing data in pandas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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