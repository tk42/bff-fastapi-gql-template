# from fastapi import FastAPI
import strawberry
from api.schema import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
