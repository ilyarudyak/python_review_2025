import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


class BabyNames:

    # Column names: names=["name", "sex", "births"]
    NAME = "name"
    SEX = "sex"
    M = "M"
    F = "F"
    BIRTHS = "births"
    YEAR = "year"
    PROP = "prop"  # Proportion of births
    CUMSUM = "cumsum"  # Cumulative sum of births
    LAST_LETTER = "last_letter"  # Last letter of the name

    def __init__(self, 
                 directory='data/babynames/',
                 col_names=[NAME, SEX, BIRTHS],
                 years=range(1880, 2011)):  # Column names
        
        self.directory = directory
        self.col_names = col_names
        self.years = years

        # Load the data
        self.names = self._load_data()
        self.total_births = self._get_total_births()
        self.names_with_prop = self._add_prop()
        self.top1000 = self._get_top1000()
        self.boys, self.girls = self._split_into_boys_girls()
        self.names[self.LAST_LETTER] = self.names[self.NAME].str[-1]

    def _load_data(self):
        
        # List to hold the yearly DataFrames
        pieces = []

        # Load each year's data and append to pieces
        for year in self.years:
            path = f'{self.directory}yob{year}.txt'
            df = pd.read_csv(path, names=self.col_names)
            df[self.YEAR] = year
            pieces.append(df)

        # Concatenate all pieces into a single DataFrame
        return pd.concat(pieces, ignore_index=True)

    def _get_total_births(self):
        return pd.pivot_table(data=self.names,
                              index=self.YEAR,
                              columns=self.SEX,
                              values=self.BIRTHS,
                              aggfunc='sum')
    
    def _add_prop(self):
        # Use transform for an efficient, non-ambiguous calculation
        prop = self.names.groupby([self.YEAR, self.SEX])[self.BIRTHS].transform(lambda x: x / x.sum())
        
        # Add the new 'prop' column to a copy of the original DataFrame
        names_with_prop = self.names.copy()
        names_with_prop[self.PROP] = prop
        return names_with_prop

    def plot_total_births(self, 
                          method='pd',
                          title="Total births by sex and year",
                          figsize=(6, 3)):
        # Plot total births using pandas
        if method == 'pd':
            self.total_births.plot(title=title, figsize=figsize)

        # Plot total births using seaborn
        elif method == 'sns':
            # Seaborn requires data in long format
            melted = self.total_births.reset_index().melt(id_vars='year', var_name='sex', value_name='births')
            sns.relplot(data=melted, x='year', y='births', hue='sex', kind='line', 
                        height=figsize[1], aspect=figsize[0]/figsize[1] )
            plt.title(title)
            plt.show()
        else:
            raise ValueError("Method must be 'pd' or 'sns'")
        
    def _get_top1000(self):
        # Function to get top 1000 names for each year/sex combination
        def get_top1000(group):
            return group.nlargest(1000, self.BIRTHS)
        return (self.names_with_prop
                .groupby([self.YEAR, self.SEX])
                .apply(get_top1000)
                .reset_index(drop=True)
                )
    
    def _split_into_boys_girls(self):
        # Split the top1000 names into boys and girls
        boys = self.top1000[self.top1000[self.SEX] == self.M]
        girls = self.top1000[self.top1000[self.SEX] == self.F]
        return boys, girls
    
    def plot_top_names(self, names=['Anna', 'Emma', 'Elizabeth'],
                       title="Popularity of Names Over Time",
                       figsize=(8, 3)):
        """
        Plots the number of births over time for a given list of names.

        This function filters the top 1000 names data for the specified names
        and plots their usage over the years, differentiating by sex using line style.
        """
        # Filter the DataFrame to include only the specified names
        subset = self.top1000[self.top1000[self.NAME].isin(names)]

        # Create the plot
        plt.figure(figsize=figsize)
        sns.lineplot(data=subset, 
                     x=self.YEAR, 
                     y=self.BIRTHS, 
                     hue=self.NAME, # Different line style for each sex
                     errorbar=None)  # No error bars for clarity

        plt.title(title)
        plt.ylabel("Number of Births")
        plt.xlabel("Year")
        plt.show()

    def plot_prop(self, 
                  method='pd', 
                  figsize=(6, 3),
                  title="Proportion of Births in Top 1000 Names by Sex",
                  yticks=np.linspace(0, 1.2, 7)):
        # Compute the pivot table
        table = pd.pivot_table(data=self.top1000,
                               index=self.YEAR,
                               columns=self.SEX,
                               values=self.PROP,
                               aggfunc='sum')
        
        if method == 'pd':
            table.plot(yticks=yticks, figsize=figsize)
            plt.title(title)
        elif method == 'sns':
            # Melt the pivot table to long form
            melted_table = table.reset_index().melt(id_vars=self.YEAR, var_name=self.SEX, value_name=self.PROP)
            plt.figure(figsize=figsize)
            sns.lineplot(data=melted_table, x=self.YEAR, y=self.PROP, hue=self.SEX)
            plt.yticks(yticks)
            plt.title(title)
        else:
            raise ValueError("Method should be 'pd' or 'sns'...")
        
    def get_diversity(self):
        """
        Compute number of distinct names, taken in order of popularity 
        from highest to lowest, in the top 50% of births.
        """

        def get_quantile_count(group, q=0.5):

            # Sort by proportion in descending order
            sorted_group = group.sort_values(by=self.PROP, ascending=False)

            # Compute cumulative sum of proportions
            sorted_group[self.CUMSUM] = sorted_group[self.PROP].cumsum()

            # Find the number of distinct names in the top quantile
            n = sorted_group[sorted_group[self.CUMSUM] <= q].shape[0]

            # Add 1 to include the name that crosses the threshold
            return n + 1  

        # Group top1000 names by year and sex and apply the function
        diversity = (self.top1000
                     .groupby([self.YEAR, self.SEX])
                     .apply(get_quantile_count)
                     )
        return diversity.unstack()
    
    def plot_diversity(self,
                       title="Number of Distinct Names in Top 50% of Births",
                       figsize=(6, 3)):
        diversity = self.get_diversity()
        diversity.plot(title=title, figsize=figsize)
        plt.ylabel("Number of Distinct Names")
        plt.xlabel("Year")
        plt.show()

    def _get_last_letter_counts(self, 
                                years=[1910, 1960, 2010],
                                letters=["d", "n", "y"],
                                sex=M):
        # Create pivot table: index=LAST_LETTER, columns=[YEAR, SEX], values=BIRTHS
        table = self.names.pivot_table(index=self.LAST_LETTER,
                                        columns=[self.YEAR, self.SEX],
                                        values=self.BIRTHS,
                                        aggfunc='sum')
        
        ############## Table filtered by years ##############
        # Filter to the selected years
        table_years = table.loc[:, years]
        # Normalize the table by dividing each column by its sum
        table_years = table_years / table_years.sum()
        # Swap the levels of the columns
        table_years.columns = table_years.columns.swaplevel(0, 1)

        ############## Table with timeseries #################
        # Normalize the entire table by dividing each column by its sum
        table_ts = table / table.sum()
        # table_ts = table_ts.loc[["d", "n", "y"], sex].T
        table_ts = table_ts.xs(sex, axis=1, level=1).loc[letters].T

        return table_years, table_ts

    def plot_last_letter(self, type='all', sex=M, 
                         years=[1910, 1960, 2010],
                         letters=["d", "n", "y"], 
                         figsize=(16, 3)):

        table_years, table_ts = self._get_last_letter_counts(years=years, 
                                                   letters=letters, 
                                                   sex=sex)

        if type == 'all':
            # Plot the histogram for the selected sex
            last_letters = table_years[sex]
            last_letters.plot(kind='bar', rot=0, figsize=figsize)
            title = f"Proportion of {sex} names ending in each letter"
            plt.title(title)
            plt.ylabel("Proportion")
            plt.xlabel("Last Letter")

        elif type == 'letters':
            # For later implementation
            table_ts.plot(figsize=figsize)
            title = f"Proportion of {sex} born with names ending in {'/'.join(letters)} over time"
            plt.title(title)
            plt.ylabel("Proportion")
            plt.xlabel("Year")

        else:
            raise ValueError("Type must be 'all' or 'letters'")
