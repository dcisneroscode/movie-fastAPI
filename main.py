# python imports
import json
import os
from typing import Optional, List

from fastapi.security.http import HTTPAuthorizationCredentials
from starlette.requests import Request


# My imports
from jwt_manager import create_token, validate_token


# pydantic imports
from pydantic import BaseModel, Field


# fastapi imports
from fastapi import FastAPI, Path, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer


with open("movies.json", "r", encoding="utf-8") as data:
    movies = json.load(data)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="invalid credentials")

class User(BaseModel):
    email: str
    password: str



class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_lenght= 5, max_length=15, default= "movie title")
    overview: str = Field(min_length=5, max_length=100, default="movie overview")
    year: int = Field(default=2022, le=2022)
    rating: float = Field(default=1.0, ge=1,le=10)
    category: str = Field(default="category movie")



app = FastAPI()
app.title = "My API Movie App"
app.version = "0.0.1"



# GET ALL MOVIES
@app.get(
    path="/movies",
    tags=["movies"],
    response_model= List[Movie],
    status_code=200,
    dependencies=[Depends(JWTBearer())]
)
def get_movies() -> List[Movie]:
    """
    Get all movies

    This path gets all movies

    Parameters: without parameters

    
    Returns a json with the basic movie information:
        id
        tittle
        overview
        year
        rating
        category
    """
    return JSONResponse(status_code=200, content=movies)


# GET MOVIE FOR THIS ID
@app.get(
    path="/movies/{id}",
    tags=["movies"],
    response_model= Movie
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    """
    Get a one movie

    This path gets a movie through your id

    Parameters: required
        id: int
       
    
    Returns a json with the information movie
        id
        tittle
        overview
        year
        rating
        category
        or an empty list if not found
    """
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])



# CREATE A MOVIE IN THE DATABASE
@app.post(
    path="/movies",
    tags=["movies"],
    response_model = dict
)
def create_movie(movie: Movie) -> dict:
    """
    Create a movie

    
    This path create a movie in the database

    Query Parameters:
        id: int
        title: string
        overview: string
        year: string
        rating: float
        category: string
    
    returns a json with a succesfully message
    
    """
    with open("movies.json", "r+", encoding="utf-8") as data:
        results = json.loads(data.read())
        movie_list = movie
        results.append(dict(movie_list))
        data.seek(0)
        data.write(json.dumps(results, indent=4))
        return JSONResponse(content={"message" : "the movie was successfully registered"})
    


# UPDATE A MOVIE
@app.put(
        path="/movies/{id}",
        tags=["movies"],
        response_model= dict
)
def update_movie(id: int, 
                 movie: Movie) -> dict:
    """
    Update a movie data

    This path update a movie data

    Parameters: required
        id: int

    
    returns  a json with a succesfully message
       
    """
    with open("movies.json", "r+", encoding="utf-8") as data:
        result = json.loads(data.read())
        update_list = result
        for item in update_list:
            if item["id"] == id:
                item["title"] = movie.title
                item["overview"] = movie.overview
                item["year"] = movie.year
                item["rating"] = movie.rating
                item["category"] = movie.category
                with open("update_movies.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(update_list, indent= 4))
                    os.rename("./update_movies.json", "./movies.json")
                    return JSONResponse(content={"message" : "the movie was successfully updated"})
              

# DELETE A MOVIE
@app.delete(
        path="/movies/{id}",
        tags=["movies"],
        response_model= dict
)
def delete_movie(id: int ) -> dict:
    """
    Delete a movie data

    This path delete a movie data

    Parameters: required
        id: int

    
    returns  a json with a succesfully message
       
    """
    
    with open("movies.json", "r+", encoding="utf-8") as data:
        remove_item = json.loads(data.read())
        for item in remove_item:
            if item["id"] == id:
                remove_item.remove(item)
                with open("remove_movies.json", "w+", encoding="utf-8") as f:
                    f.write(json.dumps(remove_item, indent=4))
                    os.rename("./remove_movies.json", "./movies.json")
                    return JSONResponse(content={"message" : "the movie was successfully eliminated"})
                




# GET NAME CATEGORY
@app.get(
    path="/movies-category/",
    tags=["category"]
)
def get_movies_by_category(category: str):
    """
    Get categories name

    This path return is to get categories name

    Parameters:
        category: string

    
    Returns the information name categories
       
    """
    return category



# GET ALL MOVIES FOR A ONE CATEGORY
@app.get(
    path="/movies-category/{category}",
    tags=["category"],
    response_model= List[Movie]
)
def get_movie_by_category(category: str) -> List[Movie]:
    """
    Get all movies 

    This path return is to get all movies in a category

    Parameters: required
        category: string

    
    Returns all the information of the movies that are equal to the category given in the parameter
       
    """
    data = list(filter(lambda movie: category == movie["category"], movies))
    return JSONResponse(content = data)




# VALIDATE A USER
@app.post(
        path="/login",
        tags=["Auth"],
        
)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
    return JSONResponse(content=token, status_code=200)

