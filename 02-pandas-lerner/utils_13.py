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

        # University columns names
        self.id_col = 'OPEID6'
        self.name_col = 'INSTNM'
        self.city_col = 'CITY'
        self.state_col = 'STABBR'
        self.admission_rate_col = 'ADM_RATE'
        self.tuition_out_col = 'TUITIONFEE_OUT'
        self.earnings_col = 'MD_EARN_WNE_P10'

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