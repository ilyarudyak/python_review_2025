import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
import json

from collections import defaultdict, Counter


class USA_GOV:

    # Column names
    TZ = 'tz' # Time zone
    A = 'a'  # User agent
    OS = 'os'  # Operating system
    TOTAL = 'total'  # Total count

    def __init__(self, 
                 filepath='data/bitly_usagov/example.txt',
                 fill=False):  # Fill missing values with 'Missing' or 'Unknown'
        
        # Default parameters
        self.filepath = filepath
        self.fill = fill    

        # Load the DataFrame
        self.records = self._load_data()
        self.records_df = self._convert_to_df(fill=fill)
        self.decomposed_os = self._decompose_windows_users()
        self.pivot_os = self._get_pivot_os()

    def _load_data(self):
    
        with open(self.filepath) as f:
            records = [json.loads(line) for line in f]

        return records
    
    def _convert_to_df(self, fill=False):
        df = pd.DataFrame(self.records)
        if fill:
            df = df.fillna('Missing')
            df[self.TZ] = df[self.TZ].replace('', 'Unknown')
        return df
    
    def count_time_zones(self,
                         approach='Counter', 
                         top=None):

        # Simple version
        def get_counts_simple(sequence):
            counts = {}
            for x in sequence:
                if x in counts:
                    counts[x] += 1
                else:
                    counts[x] = 1
            return counts

        # Using defaultdict
        def get_counts_defaultdict(sequence):
            counts = defaultdict(int)
            for x in sequence:
                counts[x] += 1
            return counts
        
        # Using Counter from collections
        def get_counts_counter(sequence):
            return Counter(sequence)
        
        time_zones = [rec['tz'] for rec in self.records if 'tz' in rec]

        # Select the counting approach
        if approach == 'simple':
            get_counts = get_counts_simple
        elif approach == 'defaultdict':
            get_counts = get_counts_defaultdict
        elif approach == 'Counter':
            get_counts = get_counts_counter
        else:
            raise ValueError("Invalid approach. Use 'simple', 'defaultdict', or 'Counter'.")

        # If top is specified, return only the top N time zones
        if top is not None:
            counts = get_counts(time_zones)
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_counts[:top])

        return get_counts(time_zones)
    
    def count_time_zones_pandas(self):
        return self.records_df[self.TZ].value_counts().sort_values(ascending=False)
    
    def plot_time_zones(self, top=5):
        counts = self.count_time_zones_pandas().head(top)
        sns.catplot(x=counts.index, y=counts.values, kind='bar', height=3, aspect=1.5)
        plt.xlabel('Number of Records')
        plt.ylabel('Time Zone')
        plt.title(f'Top {top} Time Zones in USA Gov Data')
        # Rotate x labels for better readability
        plt.xticks(rotation=90)

    def get_user_agents(self):
        
        user_agents = self.records_df[self.A].str.split().str[0]
        return user_agents.value_counts().sort_values(ascending=False)
    
    def _decompose_windows_users(self):

        # Copy the dataframe
        if self.fill:
            df = self.records_df.copy()
        else:
            df = self._convert_to_df(fill=True)

        # Create a new column 'os' based on whether 'Windows' is in the user agent string
        os_map = {True: 'Windows', False: 'Not Windows'}
        df[self.OS] = df[self.A].str.contains('Windows').map(os_map)

        return df

    def _get_pivot_os(self):
        df = self.decomposed_os
        pivot = df.pivot_table(index=self.TZ, 
                                columns=self.OS, 
                                aggfunc='size', 
                                fill_value=0)  
        pivot[self.TOTAL] = pivot.sum(axis=1)

        return pivot.sort_values(by=self.TOTAL, ascending=False)
    
    def plot_time_zones_by_os(self, top=10):

        # Get long format DataFrame for plotting
        long_df = self._get_long_pivot(top=top)
        
        # Plot using sns.catplot as horizontal bar plot
        g = sns.catplot(
            data=long_df, 
            x='count', 
            y=self.TZ, 
            hue=self.OS, 
            kind='bar', 
            height=6, 
            aspect=2,
            orient='h'
        )
        plt.title('Top 10 Time Zones by OS Count')
        plt.show()

    def _get_long_pivot(self, top=10):
        # Copy existing pivot table
        long_pivot = self.pivot_os.copy()

        # Extract top N time zones
        long_pivot = long_pivot.head(top)

        # Sort in an opposite order for better visualization
        long_pivot = long_pivot.sort_values(by=self.TOTAL, ascending=True)

        # Drop the 'total' column for plotting
        long_pivot = long_pivot.drop(columns=[self.TOTAL])

        # Melt pivot_os to long format
        long_df = long_pivot.reset_index().melt(
            id_vars=self.TZ, 
            value_vars=['Not Windows', 'Windows'], 
            var_name=self.OS, 
            value_name='count'
        )

        return long_df