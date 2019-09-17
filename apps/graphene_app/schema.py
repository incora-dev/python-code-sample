import graphene
from apps.users_app.schema import Mutation, Query

class Mutations(Mutation, graphene.ObjectType):pass

class Query(Query, graphene.ObjectType):pass

schema = graphene.Schema(query= Query, mutation= Mutations) 