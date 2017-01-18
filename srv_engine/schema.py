"""Main GQL schema. It is built dynamically from the
iteration on the models cache."""

from django.apps import apps
import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .models import GQLModel

GQL_MODELS = [m for m in apps.get_models() if issubclass(m, GQLModel)]

GQL_MUTATIONS = list()
QUERY_ATTRS = dict()

for m in GQL_MODELS:
    m.build_graph_attr()
    QUERY_ATTRS[m.__name__] = graphene.Field(m._GQL.node)
    QUERY_ATTRS[m._GQL.resolve["name"]] = m._GQL.resolve["method"]
    GQL_MUTATIONS.append(m._GQL.mutation)


QUERY_ATTRS["node"] = graphene.relay.Node.Field()
# node_query = type("NodeQuey", (graphene.AbstractType,), QUERY_ATTRS)

GQL_MUTATIONS.append(graphene.ObjectType)

Query = type("Query", (graphene.ObjectType, ), QUERY_ATTRS)
Mutation = type("Mutation", tuple(GQL_MUTATIONS), dict())

SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
