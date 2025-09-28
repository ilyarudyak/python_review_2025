import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

class MovieLens:

    # Column names
    # users: unames = ["user_id", "gender", "age", "occupation", "zip"]
    USER_ID = 'user_id'
    GENDER = 'gender'
    AGE = 'age'
    OCCUPATION = 'occupation'
    ZIP = 'zip'

    # rnames = ["user_id", "movie_id", "rating", "timestamp"]
    MOVIE_ID = 'movie_id'
    RATING = 'rating'
    TIMESTAMP = 'timestamp'

    # mnames = ["movie_id", "title", "genres"]
    TITLE = 'title'
    GENRES = 'genres'

    # Miscellaneous
    M = 'M'
    F = 'F'
    DIFF = 'diff'  # Difference in mean ratings

    def __init__(self, 
                 users_filepath='data/movielens/users.dat',
                 ratings_filepath='data/movielens/ratings.dat',
                 movies_filepath='data/movielens/movies.dat',
                 sep='::',
                 engine='python'):  # Separator and engine for reading .dat files
        
        # Default parameters
        self.users_filepath = users_filepath
        self.ratings_filepath = ratings_filepath
        self.movies_filepath = movies_filepath
        self.sep = sep
        self.engine = engine

        # Load the DataFrames
        self.users = self._load_users()
        self.ratings = self._load_ratings()
        self.movies = self._load_movies()
        self.data = self._merge_data()
        self.data_by_genre = self._merge_data(by_genre=True)

    def _load_users(self):
        names = [self.USER_ID, self.GENDER, self.AGE, self.OCCUPATION, self.ZIP]
        return pd.read_csv(self.users_filepath, 
                           sep=self.sep, 
                           header=None, 
                           names=names,
                           engine=self.engine)
    
    def _load_ratings(self):
        names = [self.USER_ID, self.MOVIE_ID, self.RATING, self.TIMESTAMP]
        return pd.read_csv(self.ratings_filepath, 
                           sep=self.sep, 
                           header=None, 
                           names=names,
                           engine=self.engine)

    def _load_movies(self):
        names = [self.MOVIE_ID, self.TITLE, self.GENRES]
        return pd.read_csv(self.movies_filepath, 
                           sep=self.sep, 
                           header=None, 
                           names=names,
                           engine=self.engine)
    
    def _merge_data(self, by_genre=False):

        # Merge users and ratings on user_id
        data = pd.merge(self.ratings, self.users, on=self.USER_ID, how='left', indicator=True)
        data = self._check_merge(data, 'users')

        # Merge the result with movies on movie_id
        if by_genre:
            movies = self._explode_genre()
        else :
            movies = self.movies

        data = pd.merge(data, movies, on=self.MOVIE_ID, how='left', indicator=True)
        data = self._check_merge(data, 'movies')

        return data
    
    def _check_merge(self, df, entity):
        """
        Check if all entities from the left DataFrame are present in the right.
        If not, raise a ValueError.
        """
        missing = df[df['_merge'] == 'left_only']
        if not missing.empty:
            raise ValueError(f"Some {entity} in the left DataFrame are missing. Count: {len(missing)}")
        return df.drop(columns=['_merge'])

    def mean_ratings_by_gender(self, index=[MOVIE_ID, TITLE], active=False):
        """
        Calculate the mean movie ratings for each film, grouped by gender using pivot table.
        """
        
        mean_ratings = pd.pivot_table(data=self.data, 
                              index=index,
                              columns=self.GENDER, 
                              values=self.RATING, 
                              aggfunc='mean')
    
        if active:
            active_titles = self.get_active_titles()
            mean_ratings = mean_ratings.loc[active_titles]

        return mean_ratings

    def get_active_titles(self, min_ratings=250, cols=[MOVIE_ID, TITLE]):
        """
        Return movie titles that have received at least `min_ratings` ratings.
        """
        rating_counts = self.data.groupby(cols).size()
        active_titles = rating_counts.index[rating_counts >= min_ratings]
        return active_titles
    
    def get_titles_with_disagreement(self, index=[MOVIE_ID, TITLE], active=True, n=10):
        """
        Return the top `n` movie titles with the highest disagreement in ratings.
        """

        # Group by movie and title, then calculate std deviation of ratings
        std_ratings = self.data.groupby(index)[self.RATING].std()

        if active:
            active_titles = self.get_active_titles()
            std_ratings = std_ratings.loc[active_titles]

        most_disagreement = std_ratings.sort_values(ascending=False)
        return most_disagreement.head(n)
    
    def _explode_genre(self):

        movies = self.movies.copy()
        movies[self.GENRES] = movies[self.GENRES].str.split('|')
        movies = movies.explode(self.GENRES)

        return movies
