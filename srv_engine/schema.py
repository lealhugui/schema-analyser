"""Main GQL schema. It is built dynamically from the
iteration on the models cache."""

from django.apps import apps
import graphene

from .models import GQLModel

GQL_MODELS = [m for m in apps.get_models() if issubclass(m, GQLModel)]

for m in GQL_MODELS:
    m.build_graph_attr()

GQL_QUERIES = list()
GQL_MUTATIONS = list()

for m in GQL_MODELS:
    GQL_QUERIES.append(m._GQL.query)
    GQL_MUTATIONS.append(m._GQL.mutation)

GQL_QUERIES.append(graphene.ObjectType)
GQL_MUTATIONS.append(graphene.ObjectType)

Query = type("Query", tuple(GQL_QUERIES), dict())
Mutation = type("Mutation", tuple(GQL_MUTATIONS), dict())

SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
