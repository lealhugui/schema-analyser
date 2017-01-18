"""Main GQL schema. It is built dynamically from the
iteration on the models cache."""

from django.apps import apps
import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .models import GQLModel

GQL_MODELS = [m for m in apps.get_models() if issubclass(m, GQLModel)]

for m in GQL_MODELS:
    m.build_graph_attr()

GQL_QUERIES = list()
GQL_MUTATIONS = list()
GQL_NODES = dict()

for m in GQL_MODELS:
    GQL_NODES[m.__name__] = DjangoFilterConnectionField(m._GQL.node)

gql_root_query = type("Node", (graphene.AbstractType, ), GQL_NODES)
node_attrs = { "node": gql_root_query }
node_query = type("NodeQuey", (graphene.AbstractType,), node_attrs)
GQL_QUERIES.append(node_query)

# GQL_QUERIES.append(gql_root_query)

for m in GQL_MODELS:
    GQL_QUERIES.append(m._GQL.query)
    GQL_MUTATIONS.append(m._GQL.mutation)

GQL_QUERIES.append(graphene.ObjectType)
GQL_MUTATIONS.append(graphene.ObjectType)

Query = type("Query", tuple(GQL_QUERIES), dict())
Mutation = type("Mutation", tuple(GQL_MUTATIONS), dict())

SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
