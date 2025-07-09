import pandas as pd
import numpy as np

class OECDUtils:
    """Utility class for handling OECD data."""
    
    def __init__(self, 
                 df_oecd=None,
                 country_column_oecd='country',   
                 df_so=None,
                 country_column_so='Country',
                 country_to_exclude='North Korea'):
        self.df_oecd = df_oecd
        self.country_column_oecd = country_column_oecd
        self.df_so = df_so
        self.country_column_so = country_column_so
        self.country_to_exclude = country_to_exclude

        self.oecd_countries_list = self.get_oecd_countries()
    
    def get_oecd_countries(self):
        """Creates a list of OECD countries from df_so using df_oecd"""
        countries_oecd = self.df_oecd[self.country_column_oecd].unique()
        countries_so = self.df_so[self.country_column_so].unique()
        oecd_countries_list = []
        for country_oecd in countries_oecd:
            for country_so in countries_so:
                if country_oecd.lower() in country_so.lower():
                    if country_so.lower() == self.country_to_exclude.lower():
                        continue
                    # print(f"Match found: {country_oecd} in {country_so}")
                    oecd_countries_list.append(country_so)
        return oecd_countries_list 
    


class MultiIndexUtils:

    general_columns = ['age',
                    'are.you.datascientist',
                    'is.python.main',
                    'company.size',
                    'country.live',
                    'employment.status',
                    'first.learn.about.main.ide',
                    'how.often.use.main.ide',
                    'is.python.main',
                    'main.purposes'
                    'missing.features.main.ide'
                    'nps.main.ide',
                    'python.version.most',
                    'python.years',
                    'python2.version.most',
                    'python3.version.most',
                    'several.projects',
                    'team.size',
                    'use.python.most',
                    'years.of.coding'
                    ]
    
    def __init__(self, df=None):
        self.df = df
    
    def column_multi_name(self, column_name):
        if column_name in MultiIndexUtils.general_columns:
            return ('general', column_name)
        else:
            first, rest = column_name.rsplit('.', 1)
            return (first, rest)
        
    def with_multi_index_columns(self):
        """Return a new DataFrame with MultiIndex columns."""
        new_df = self.df.copy()
        new_df.columns = pd.MultiIndex.from_tuples(
            [self.column_multi_name(col) for col in new_df.columns]
        )
        return new_df
    
# A function to categorize the years of experience
def categorize_experience(years):
    if years < 1:
        return 'Less than 1 year'
    elif 1 <= years <= 2:
        return '1–2 years'
    elif 3 <= years <= 5:
        return '3–5 years'
    elif 6 <= years <= 10:
        return '6–10 years'
    else:
        return '11+ years'