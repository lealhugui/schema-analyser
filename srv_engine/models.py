from django.db.models import Model as DjangoModel
# These imports are made here for the sake of simplicity for the developer.
# This way, the developer can import only this namespace and expect to have
# both the custom model and the base django fields
from django.db.models.fields import *
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import (
    ForeignKey, ForeignObject, OneToOneField, ManyToManyField,
    ManyToOneRel, ManyToManyRel, OneToOneRel,
)
import graphene
from graphene import relay, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id


class GQLModel(DjangoModel):
    """Base Model that will be exposed to GraphQL Interface.

    Beyond every Django's Model attribute, this class can have an inner class called "_GQL", wich in turn can have
      the following attributes:
      query_name: the query name that will be transpiled in the root node
      node: a Graphene's "DjangoObjectType" class for the GraphQL node configuration
      query: a Graphene's "AbstractType" class for GraphQL query configuration
      mutation: a Graphene's "AbstractType" class for GraphQL base mutation configuration
    """

    class Meta:
        abstract = True

    @classmethod
    def build_graph_attr(cls):
        """Consolidate the GraphQL objects defined by the Developer.
        If no object was defined in the class declaration, a generic one is
        created here
        """
        # TODO: give 'Query' and 'Mutation' the option to be an iterable.

        if not hasattr(cls, "_GQL"):
            b = tuple()
            attrs = dict()
            cls._GQL = type("_GQL", b, attrs)

        c_name = cls.__name__
        has_node = hasattr(cls._GQL, "node") and cls._GQL.node is not None
        has_query = hasattr(cls._GQL, "query ") and cls._GQL.query is not None
        has_mutation = hasattr(cls._GQL, "mutation ") and cls._GQL.mutation is not None

        if has_node:
            node = cls._GQL.node
        else:
            # Node defnition
            node_name = c_name

            class Meta:
                model = cls
                interfaces = (relay.Node, )

            node_attrs = {"Meta": Meta}
            node = type(node_name, (DjangoObjectType, ), node_attrs)

        if has_query:
            query = cls._GQL.query
        else:
            # Query definition
            q_name = None
            if hasattr(cls._GQL, "query_name"):
                q_name = cls._GQL.query_name
                print(q_name)
            else:
                q_name = "{}Query".format(c_name)
            q_attrs = dict()
            q_attrs[c_name] = DjangoFilterConnectionField(node)
            # q_attrs = {c_name: relay.Node.Field(node)}
            query = type(q_name, (AbstractType,), q_attrs)
        if has_mutation:
            mutation = cls._GQL.mutation
        else:
            # Mutation definition
            m_fld = dict()
            for f in node._meta.fields:
                m_fld[f] = node._meta.fields[f]
            mutation_input = type("Input", tuple(), m_fld)

            mutation_opt = type("Opt", tuple(), {"model": cls, })

            m_attrs = {c_name.lower() : node}
            m_attrs["Input"] = mutation_input
            m_attrs["OK"] = graphene.Boolean()
            m_attrs["Opt"] = mutation_opt
            m_attrs[cls.__name__.lower()] = graphene.Field(node)
            m_attrs["mutate_and_get_payload"] = classmethod(mutate_and_get_payload)

            inner_mutation = type("Introduce{c}".format(c=c_name),
                                  (relay.ClientIDMutation,),
                                  m_attrs)

            mutation = type("Mutation{c}".format(c=c_name),
                            (AbstractType,),
                            {inner_mutation.__name__: inner_mutation.Field()})

        cls._GQL.node = node
        cls._GQL.query = query
        print(query)
        cls._GQL.mutation = mutation

        return cls._GQL


def mutate_and_get_payload(cls, input, context, info):
    result_ok = False
    if input.get("id") is None or input.get("id") == "":
        # Create....
        gid = input.pop("id")
        result = cls.Opt.model.objects.create(**input)
        result_ok = True
    else:
        # Update
        gid = input.pop("id")
        r_id = from_global_id(gid)[1]

        cls.Opt.model.objects.filter(pk=r_id).update(**input)
        result = cls.Opt.model.objects.get(pk=r_id)
        result_ok = True

    result_set = {
        cls.Opt.model.__name__.lower(): result,
        "OK": result_ok
    }
    return cls(**result_set)
