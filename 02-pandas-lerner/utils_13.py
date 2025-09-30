import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

import pandas as pd

class CollegeScorecard:

    def __init__(self):
        # Default file paths (adjusted to 'data/' as per your setup)
        self.institutions_filename = 'data/Most-Recent-Cohorts-Institution.csv'
        self.fields_filename = 'data/FieldOfStudyData1718_1819_PP.csv'
        
        # Default usecols for institutions
        self.institutions_usecols = ['OPEID6', 'INSTNM', 'CITY', 'STABBR', 
                                     'FTFTPCTPELL', 'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'ADM_RATE', 
                                     'NPT4_PUB', 'NPT4_PRIV', 'NPT41_PUB', 'NPT41_PRIV', 
                                     'NPT45_PUB', 'NPT45_PRIV', 'MD_EARN_WNE_P10', 'C100_4']
        
        # Default usecols for fields of study
        self.fields_usecols = ['OPEID6', 'INSTNM', 'CREDDESC', 'CIPDESC', 'CONTROL']
        
        # Load the DataFrames
        self.univers = pd.read_csv(self.institutions_filename, usecols=self.institutions_usecols)
        self.fields = pd.read_csv(self.fields_filename, usecols=self.fields_usecols)

        ################################################################################
        ########################### University columns names ###########################
        ################################################################################

        # ID, name, city, state
        self.id_col = 'OPEID6' # Unique ID (integer) for each educational institution
        self.name_col = 'INSTNM' # Institution name
        self.city_col = 'CITY' # Institution city
        self.state_col = 'STABBR' # Institution state (abbreviation)

        # Financial aid and tuition
        self.pell_col = 'FTFTPCTPELL' # Percentage of Pell-grant recipients
        self.tuition_in_col = 'TUITIONFEE_IN' # In-state tuition
        self.tuition_out_col = 'TUITIONFEE_OUT' # Out-of-state tuition

        # Net and average prices
        self.net_price_pub = 'NPT4_PUB' # Net price for public institutions
        self.net_price_priv = 'NPT4_PRIV' # Net price for private institutions
        self.avg_price_low_pub = 'NPT41_PUB' # Average price paid by people in the lowest income bracket
        self.avg_price_low_priv = 'NPT41_PRIV' # Average price paid by people in the lowest income bracket
        self.avg_price_high_pub = 'NPT45_PUB' # Average price paid by people in the highest income bracket
        self.avg_price_high_priv = 'NPT45_PRIV' # Average price paid by people in the highest income bracket

        # Earnings, admission, and completion rates
        self.earnings_col = 'MD_EARN_WNE_P10' # Median earnings 10 years following graduation
        self.admission_rate_col = 'ADM_RATE' # Admission rate
        self.completion_rate_col = 'C100_4' # Completion rate within 4 years

        ################################################################################
        ######################### Fields of study columns names ########################
        ################################################################################

        # Field of study columns names
        self.fields_degree_col = 'CREDDESC'
        self.fields_program_col = 'CIPDESC'
        self.fields_type_col = 'CONTROL'

        # Degree types
    #     array(['Bachelors Degree', "Master's Degree", 'Doctoral Degree',
    #    'Graduate/Professional Certificate', 'First Professional Degree',
    #    'Undergraduate Certificate or Diploma', "Associate's Degree",
    #    'Post-baccalaureate Certificate'], dtype=object)
        self.BATCHELORS = 'Bachelors Degree'
        self.MASTERS = "Master's Degree"
        self.DOCTORAL = 'Doctoral Degree'

        # Get universities that offer graduate and undergraduate programs
        self.undergrad_univers = self._get_undergrad_univers()
        self.cs_undergrad = self._get_undegrad_univers_CS()
        self.grad_univers = self._get_grad_univers()

        self.undergrad_univers_set = self._get_undergrad_univers(return_type='set')
        self.grad_univers_set = self._get_grad_univers(return_type='set')

        self.ivy_plus = ['Harvard University', 
                        'Massachusetts Institute of Technology',
                        'Yale University',
                        'Columbia University in the City of New York',
                        'Brown University',
                        'Stanford University',
                        'University of Chicago',
                        'Dartmouth College',
                        'University of Pennsylvania',
                        'Cornell University',
                        'Princeton University']

    def _get_undergrad_univers(self, return_type='df'):
        """Get universities that offer undergraduate programs (bachelor's degrees)."""
        undergrad_mask = self.fields[self.fields_degree_col] == self.BATCHELORS
        undergrad_univs = self.fields[undergrad_mask]
        if return_type == 'df':
            return undergrad_univs
        elif return_type == 'set':
            return set(undergrad_univs[self.name_col].unique())
        else:
            raise ValueError("Invalid return_type. Use 'df' or 'set'.")
            
    def _get_grad_univers(self, return_type='df'):
        """Get universities that offer graduate programs (master's and doctoral degrees)."""
        grad_mask = self.fields[self.fields_degree_col].isin([self.MASTERS, self.DOCTORAL])
        grad_univers = self.fields[grad_mask]
        if return_type == 'df':
            return grad_univers
        elif return_type == 'set':
            return set(grad_univers[self.name_col].unique())
        else:
            raise ValueError("Invalid return_type. Use 'df' or 'set'.")

    def _get_undegrad_univers_CS(self):
        # Degree programs containing "Computer Science"
        mask_computer_science = self.undergrad_univers[self.fields_program_col].str.contains("Computer Science", case=False, na=False)

        # Undegrad universities with "Computer Science" programs
        cs_undergrad = self.undergrad_univers[mask_computer_science]

        return cs_undergrad

    def init_questions(self, quest_num):

        # What state has the greatest number of universities in this database?
        if quest_num == 1:
            return self._init_question_1()
        else:
            raise ValueError("Question number not recognized.")

    def _init_question_1(self):
        return self.univers['STABBR'].value_counts().head(1)

    def get_cs_tuition_stats(self):
        """
        Compute descriptive stats (min, median, mean, max) for TUITIONFEE_OUT
        of unique institutions offering undergrad CS degrees.
        Uses precomputed self.cs_undergrad.
        """
        # Get unique institution IDs from cs_undergrad (deduplicate programs)
        unique_ids = self.cs_undergrad[self.id_col].unique()
        
        # Filter univers to these IDs and get tuition
        tuition_df = self.univers[self.univers[self.id_col].isin(unique_ids)].copy()
        tuition_values = tuition_df[self.tuition_out_col].dropna()
        
        # Return stats
        return tuition_values.describe()

    def plot_tuition_admission_earnings(self):
        """
        Create a scatter plot with tuition on x-axis, admission rate on y-axis,
        and median earnings (10 years) for colorizing. Uses 'Spectral' colormap.
        """
        # Prepare data: Drop rows with NaN in key columns
        data = self.univers[[self.tuition_out_col, self.admission_rate_col, self.earnings_col]].dropna()
        
        # Create the scatter plot
        sns.relplot(
            data=data,
            x=self.tuition_out_col,
            y=self.admission_rate_col,
            hue=self.earnings_col,
            kind='scatter',
            palette='Spectral',
            alpha=0.7
        )
        
        # Add labels and title
        plt.xlabel('Tuition (Out-of-State)')
        plt.ylabel('Admission Rate')
        plt.title('Tuition vs. Admission Rate, Colored by Median Earnings (10 Years)')
        plt.show()

    def get_top_univers_tuition_pell(self):
        """
        Find universities in the top 25% of both tuition and Pell grants.
        Returns the number of such universities and the top 5 sorted by institution name.
        """
        # Remove NaNs from tuition and pell grant columns
        univers_clean = self.univers.dropna(subset=[self.tuition_out_col, self.pell_col])
        
        # Compute the 75th percentile of tuition
        tuition_75th_percentile = univers_clean[self.tuition_out_col].quantile(0.75)
        
        # Find universities with tuition greater than the 75th percentile
        mask_75th_tuition = univers_clean[self.tuition_out_col] > tuition_75th_percentile
        
        # Compute the 75th percentile of Pell grants
        pell_75th_percentile = univers_clean[self.pell_col].quantile(0.75)
        
        # Find universities with Pell grants greater than the 75th percentile
        mask_75th_pell = univers_clean[self.pell_col] > pell_75th_percentile
        
        # Find universities that are in the top 25% of both tuition and Pell grants
        mask_top_both = mask_75th_tuition & mask_75th_pell
        top_both_univs = univers_clean[mask_top_both]
        
        # Number of such universities
        num_top_both = top_both_univs.shape[0]
        
        # Top 5 universities ordered by institution name
        top_univers = top_both_univs[[self.name_col, self.city_col, self.state_col]].sort_values(by=self.name_col)
        
        return top_univers

    def get_cheapest_to_top(self, type='pub'):
        """
        Find universities that are in the cheapest 25% net price and have top 25% salaries 10 years after graduation.
        type: 'pub' for public, 'priv' for private.
        Returns the filtered DataFrame with columns [id, name, city, state], sorted by state and city.
        """
        if type == 'pub':
            net_price_col = self.net_price_pub
        elif type == 'priv':
            net_price_col = self.net_price_priv
        else:
            raise ValueError("Type must be 'pub' or 'priv'")
        
        # Find the cheapest 25% schools
        cheapest_25_quant = self.univers[net_price_col].quantile(0.25)
        mask_cheapest_25 = self.univers[net_price_col] <= cheapest_25_quant
        
        # Find the top 25% salaries
        top_25_quant_salary = self.univers[self.earnings_col].quantile(0.75)
        mask_top_25_salary = self.univers[self.earnings_col] >= top_25_quant_salary
        
        # Filter the universities that meet both criteria
        columns = [self.id_col, self.name_col, self.city_col, self.state_col]
        filtered_univers = self.univers.loc[mask_cheapest_25 & mask_top_25_salary, columns]
        
        # Sort by state and city
        filtered_univers = filtered_univers.sort_values(by=[self.state_col, self.city_col])
        
        return filtered_univers

    def plot_avg_earnings_by_state(self, figsize=(14, 3), top=10, bottom=10):
        """
        Create a bar plot for the average earnings per state, showing only the top N (highest) and bottom N (lowest) states,
        sorted by ascending pay.
        """
        # Clean data: drop rows with NaN in state or earnings
        clean_data = self.univers.dropna(subset=[self.state_col, self.earnings_col])
        
        # Compute average earnings per state
        avg_earnings = clean_data.groupby(self.state_col)[self.earnings_col].mean()

        # Sort by ascending earnings
        sorted_earnings = avg_earnings.sort_values()
        
        # Get bottom N (lowest) and top N (highest)
        bottom_earnings = sorted_earnings.head(bottom)
        top_earnings = sorted_earnings.tail(top)

        # Combine for plotting: bottom N + top N, still sorted ascending
        selected_states = pd.concat([bottom_earnings, top_earnings])

        # Plot
        plt.figure(figsize=figsize)
        selected_states.plot(kind='bar')
        plt.title(f'Average Earnings by State (Top {top} Highest and Bottom {bottom} Lowest)')
        plt.ylabel('Average Earnings')
        plt.xlabel('State')
        plt.xticks(rotation=90)
        plt.show()

    def plot_earnings_boxplot_by_state(self, figsize=(6, 4)):
        """
        Create a boxplot for the average median earnings by state.
        """
        # Compute average earnings per state
        avg_earnings = self.univers.groupby(self.state_col)[self.earnings_col].mean().dropna()
        
        # Create the boxplot
        plt.figure(figsize=figsize)
        avg_earnings.plot(kind='box')
        plt.title('Boxplot of Average Median Earnings by State')
        plt.show()