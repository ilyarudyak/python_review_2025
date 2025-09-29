import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


class Tips:

    # Class variables: total_bill,tip,smoker,day,time,size,tip_pct
    TOTAL_BILL = "total_bill"
    TIP = "tip"
    SMOKER = "smoker"
    DAY = "day"
    TIME = "time"
    SIZE = "size"
    TIP_PCT = "tip_pct"  # Tip as a percentage of total bill

    def __init__(self, 
                 filepath='data/tips.csv'):  # File path to the CSV file
        
        self.filepath = filepath

        # Load the data
        self.tips = self._load_data()

    def _load_data(self):

        # Load the CSV file into a DataFrame
        df = pd.read_csv(self.filepath)

        # Add tip percentage column
        df[self.TIP_PCT] = df[self.TIP] / df[self.TOTAL_BILL]

        return df
    
    def top(self, group, n=5, column=TIP_PCT):
        """Return the top n rows sorted by the specified column."""
        return group.nlargest(n, columns=column)

    def top_tips_by_group(self,
                          group_by=SMOKER,
                          n=5):
        """Select the top n tip_pct values by group."""
        
        def top_n(group, column=self.TIP_PCT, n=n):
            return group.nlargest(n, columns=column)
        
        return self.tips.groupby(group_by).apply(top_n)