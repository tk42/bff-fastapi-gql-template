import asyncio
import uvicorn

from fastapi import FastAPI

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from populate import create_tables
from api.db.session import engine
from api.core.config import settings
from api.schemas.query_schema import Query
from api.schemas.mutation_schema import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=True))


def application():
    app = FastAPI()
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    return app


if __name__ == "__main__":
    print("Populating database...")
    asyncio.run(create_tables(engine))
    print("Database populated.")

    print("Starting server...")
    uvicorn.run("main:application", host=settings.HOST_URL, port=settings.HOST_PORT, reload=True)
