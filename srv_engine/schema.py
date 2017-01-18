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
    GQL_NODES[m.__name__] = graphene.Field(m._GQL.node)
    GQL_MUTATIONS.append(m._GQL.mutation)    


GQL_NODES["node"] = graphene.relay.Node.Field()
# node_query = type("NodeQuey", (graphene.AbstractType,), GQL_NODES)

GQL_MUTATIONS.append(graphene.ObjectType)

Query = type("Query", (graphene.ObjectType, ), GQL_NODES)
Mutation = type("Mutation", tuple(GQL_MUTATIONS), dict())

SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
