import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Movie as MovieModel
from app import db

class MovieType(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Query(graphene.ObjectType):
    all_movies = graphene.List(
        MovieType,
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=10)
    )
    movie_by_id = graphene.Field(MovieType, id=graphene.ID(required=True))
    search_movies = graphene.List(
        MovieType,
        title=graphene.String(),
        genre=graphene.String(),
        release_year=graphene.Int()
    )

    def resolve_all_movies(root, info, page, per_page):
        query = db.select(MovieModel).offset((page - 1) * per_page).limit(per_page)
        return db.session.scalars(query)

    def resolve_movie_by_id(root, info, id):
        query = db.select(MovieModel).filter(MovieModel.id == id)
        return db.session.scalar(query)

    def resolve_search_movies(root, info, title=None, genre=None, release_year=None):
        query = db.select(MovieModel)
        if title:
            query = query.filter(MovieModel.title.contains(title))
        if genre:
            query = query.filter(MovieModel.genre == genre)
        if release_year:
            query = query.filter(MovieModel.release_year == release_year)
        return db.session.scalars(query)

class CreateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        release_year = graphene.Int(required=True)
        genre = graphene.String(required=True)
        rating = graphene.Float(required=False)
    
    movie = graphene.Field(MovieType)
    
    def mutate(self, info, title, director, release_year, genre, rating=None):
        movie = MovieModel(
            title=title,
            director=director,
            release_year=release_year,
            genre=genre,
            rating=rating
        )
        db.session.add(movie)
        db.session.commit()
        return CreateMovie(movie=movie)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=False)
        director = graphene.String(required=False)
        release_year = graphene.Int(required=False)
        genre = graphene.String(required=False)
        rating = graphene.Float(required=False)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title=None, director=None, release_year=None, genre=None, rating=None):
        movie = db.session.get(MovieModel, id)
        if movie is None:
            raise Exception(f"Movie with id {id} not found")
        
        if title:
            movie.title = title
        if director:
            movie.director = director
        if release_year:
            movie.release_year = release_year
        if genre:
            movie.genre = genre
        if rating:
            movie.rating = rating
        
        db.session.commit()
        return UpdateMovie(movie=movie)

class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    message = graphene.String()

    def mutate(self, info, id):
        movie = db.session.get(MovieModel, id)
        if movie is None:
            raise Exception(f"Movie with id {id} not found")
        db.session.delete(movie)
        db.session.commit()
        return DeleteMovie(message=f"Movie {movie.title} deleted successfully")

class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
