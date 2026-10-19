from fastapi import FastAPI
from database import engine, Base
import models
from router import auth, expense


app=FastAPI(title="Personal Finance Management API")
app.include_router(auth.router)
app.include_router(expense.router)


#Bind database
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return{
        "message": "Personal Finance Management API."
    }

@app.get("/about")
def about():
    return{
        "message": "About Finance Management API"
    }
        