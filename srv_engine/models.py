from django.db import models
import graphene
from graphene import relay, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id


class Model(models.Model):
    """Base Model
    """

    class _GQL:
        node = None
        query = None
        mutation = None

    class Meta:
        abstract = True

    @classmethod
    def build_grapth_attr(cls):
        c_name = cls.__name__
        
        has_node = False
        has_query = False
        has_mutation = False
        if cls._GQL != None:
            if cls._GQL.node != None:
                has_node = True
            if cls._GQL.query != None:
                has_query = True
            if cls._GQL.mutation != None:
                has_mutation = True
        if has_node:
            node = cls._GQL.node
        else:
            # Node defnition
            node_name = "{c}Node".format(c=c_name)

            class Meta:
                model = cls
                interfaces = (relay.Node, )
            
            node_attrs = {"Meta": Meta}
            node = type(node_name, (DjangoObjectType, ), node_attrs)
        if has_query:
            query = cls._GQL.query
        else:                
            # Query definition
            q_attrs = {c_name: DjangoFilterConnectionField(node)}
            query = type("Query", (AbstractType,), q_attrs)
        
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
            m_attrs["mutate_and_get_payload"] = classmethod(mutate_and_get_payload)

            inner_mutation = type("Introduce{c}".format(c=c_name),
                (relay.ClientIDMutation,), 
                m_attrs)

            

            inner_mutation.mutate_and_get_payload = mutate_and_get_payload
        
            mutation = type("Mutation{c}".format(c=c_name),
                (AbstractType,),
                {inner_mutation.__name__.lower(): inner_mutation.Field()}
            )
        
        cls._GQL.node = node
        cls._GQL.query = query
        cls._GQL.mutation = mutation

        return cls._GQL



def mutate_and_get_payload(cls, input, context, info):
    result_ok=False
    if input.get("id")==None or input.get("id")=="":
        # Create....
        result = cls.Opt.model.objects.create(**input)
        result_ok=True
    else:
        # Update
        gid = input.pop("id")
        r_id= from_global_id(input.get("id"))[1]

        o.Opt.model.objects.filter(pk=r_id).update(**input)
        result = o.Opt.model.objects.get(pk=r_id)
        result_ok=True

    result_set = {
        cls.Opt.model.__name__.lower(): result,
        ok: result_ok
    }
    return cls(**result_set)