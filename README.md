GraphQL API for Movie Database

Overview

The GraphQL API for Movie Database project provides a versatile and efficient API for managing movie collections. This API allows users to add, update, delete, search, and retrieve movies, supporting a seamless user experience with pagination and filtering capabilities.

Project Requirements

Schema Modification

The GraphQL schema has been extended to include the "Movie" data type with the following fields:

id: Unique identifier for the movie.
title: Title of the movie.
genre: Genre of the movie.
releaseYear: Release year of the movie.
director: Director of the movie.
rating: Rating of the movie.
Implementation of Queries

The following GraphQL queries are implemented:

allMovies: Retrieve all movies with pagination.
movieById: Retrieve a movie by its ID.
searchMovies: Search for movies by title.
Implementation of Mutations

The following GraphQL mutations are available:

createMovie: Create a new movie. Accepts input parameters for title, genre, releaseYear, director, and rating.
updateMovie: Update an existing movie. Accepts input parameters for id, title, genre, releaseYear, director, and rating.
deleteMovie: Delete an existing movie. Accepts input parameter for the movie ID.
Installation Instructions

Clone the repository:
git clone https://github.com/Winter-Krimmert/GraphQL_API_for_a_Movie_Database