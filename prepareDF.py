import pandas as pd

# Preparing the dataset based on the exploratory analysis

def PrepareDF(file_name = 'netflix_titles.csv', rating_file = './Scrapper/rating.txt', vis = 0):

    #Processing the rating text file
    #Slicing based on ":" and accessing first and last index into dict
    with open(rating_file) as file:
        data = file.read().split('\n')
        data = [i.split(':') for i in data]
        data_dict = {}
        for i in data:
            if i[-1] not in ['NONE', '[ERROR]', '']:
                data_dict['s'+i[0]] = float(i[-1]) 

    # Opening the csv file as pandas data frame
    MovieData = pd.read_csv(file_name)

    # Dropping values if the ratings do not exist
    for index, val in enumerate(MovieData['show_id']):
        if val not in data_dict:
            MovieData = MovieData.drop(index)

    #Assigning audience rating (originally under'rating') to a different column
    if(vis): MovieData['aud_cat'] = MovieData['rating']
    
    # adding the movie/show ratungs to the dataFrame
    MovieData['rating'] = [i for i in data_dict.values()]

    # Removing the rows in which either directors, actors, or genres or both are not mentioned
    MovieData.dropna(inplace=True)

    #Renaming 'listed_in' to 'genres'
    MovieData.rename(columns={'listed_in': 'genres'}, inplace=True)

    # Converting strigns in cast and genres columns to lists with strings
    MovieData['cast'] = MovieData['cast'].str.split(', ')
    MovieData['genres'] = MovieData['genres'].str.split(', ')
    if(vis):
        #These variables are explored to have a median and mean of approximately one value per entry
        #Modelling will be done as one value (non-array) for better/simpler modelling (e.g. easy regression without encoding function)
        #Only split to arrray if for visualization
        MovieData['director'] = MovieData['director'].str.split(', ')
        MovieData['country'] = MovieData['country'].str.split(', ')

    # Resetting the index of the dataframe after removing the rows 
    MovieData.reset_index(inplace=True)
    MovieData.drop(columns=['index'], inplace=True)

    if(vis): return MovieData

    #Removing the non-predictor columns as we will not need it for the prediction later
    MovieData.drop(columns=['show_id', 'description', 'country', 'duration', 'date_added', 'release_year', 'type'], inplace=True)

    return MovieData


def Labelencode(MovieData, labelEncoder):
    # Converting the string in the director and title column to float -> Makes no difference to the computer
    MovieData['director'] = labelEncoder.fit_transform(MovieData['director'].values)

    # Since the cast has way too many poeple, we are going to select the 4 with the most screen time (assuming actor with most screen time is listed first)
    MovieData['cast'] = MovieData['cast'].to_list()

    # Creatinng new columns for individual cast
    for i in range(4):
        MovieData[f'cast_{i+1}'] = ''

    for ind, item in enumerate(MovieData['cast']):
        MovieData['cast']
        for index, cast_a in enumerate(item[:4]):
            MovieData[f'cast_{index+1}'][ind] = cast_a

    MovieData.drop(columns=['cast'], inplace=True)

    MovieData['cast_1'] = labelEncoder.fit_transform(MovieData['cast_1'].values)
    MovieData['cast_2'] = labelEncoder.fit_transform(MovieData['cast_2'].values)
    MovieData['cast_3'] = labelEncoder.fit_transform(MovieData['cast_3'].values)
    MovieData['cast_4'] = labelEncoder.fit_transform(MovieData['cast_4'].values)

    MovieData['genres']=labelEncoder.fit_transform(MovieData['genres'].values)

    return MovieData


