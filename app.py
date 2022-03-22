import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Import data
df = pd.read_csv('disney_movies_total_gross.csv')

# Do some cleaning
df.dropna(axis = 0, inplace = True)
df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d')
df['year'] = df['release_date'].dt.year
df.set_index('release_date', inplace = True)
df.sort_index(inplace = True)

# Page title and description
st.title('Disney Films (1937-2016)')
st.write(
"""
The dataset for the visualisations on this page is from Kaggle [[1](https://www.kaggle.com/datasets/rashikrahmanpritom/disney-movies-19372016-total-gross)]. I use it to make some dynamic and simple graphs to include in my first Stremlit app
"""
)

# Set some dynamic parameters for app interactivity
genre_options = df['genre'].unique()

with st.sidebar:
    check = st.checkbox('Display table head')
    choose = st.selectbox('Pick a genre', genre_options)
    slide = st.slider("Select a year", int(df['year'].min()), int(df['year'].max()))

# Display table if checkbox ticked
if check:
    st.write(
    """
    ## Raw data
    These are the first 5 rows in the cleaned data. The release date was made the table index, by which entries were then sorted, and a value for year was extracted.
    """
    )
    st.table(df.head())

# Show a plot for the number of releases for each genre in a specified year
st.write(
"""
## Analysis by year
This is a pie chart showing the breakdown of genres in the releases of a given year. Change the year with the slider in the sidebar.   
"""
)
year_bkdn = plt.figure()
plt.pie(df.loc[str(slide), 'genre'].value_counts(), labels = df.loc[str(slide), 'genre'].unique())
year_bkdn.suptitle(f'Number of realeases by genre in {slide}')

st.pyplot(year_bkdn)

# By genre, show the mean total gross and number of films for each rating
st.write(
"""
## Analysis by genre
These graphs show the number of releases and mean total gross income for each rating of a specified genre. The genre can be selected in the sidebar.
"""
)
rating_counts = df.loc[df['genre'] == choose, 'mpaa_rating'].value_counts().sort_index()
gross_rating = df.loc[df['genre'] == choose].groupby('mpaa_rating')[['total_gross']].mean().reset_index().sort_values('mpaa_rating')

rating_fig, ax = plt.subplots(1,2)
rating_fig.suptitle(f'Genre: {choose}')

ax[0].barh(gross_rating['mpaa_rating'], gross_rating['total_gross'])
ax[0].set_ylabel('Rating')
ax[0].set_xlabel('Mean Total Gross')

ax[1].barh(rating_counts.index, rating_counts)
ax[1].set_yticks([])
ax[1].set_xlabel('Number of Films')

st.pyplot(rating_fig)
