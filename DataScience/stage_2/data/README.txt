This directory contains CSV files of movies crawled from IMDb and TMDb.
The schema of each file is described below:

1. imdb.csv: Contains 5000 movies crawled from https://www.imdb.com/
       id       - The primary key.
       name     - Name of the movie.
       year     - Year when the movie was released.
       duration - The runtime of the movie.
       genre    - Genres (comma-separated) the movie belongs to.
       actors   - Main actors (comma-separated) in the movie.
2. tmdb.csv: Contains 5000 movies crawled from https://www.themoviedb.org/
       id       - The primary key.
       name     - Name of the movie.
       year     - Year when the movie was released.
       duration - The runtime of the movie.
       genre    - Genres (comma-separated) the movie belongs to.
       actors   - Top billed actors (comma-separated) in the movie.
