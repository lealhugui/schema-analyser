import graphene
from graphene import relay, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from .models import Person

class PersonNode(DjangoObjectType):

    class Meta:
        model = Person
        filter_fields = ["id", "first_name", "last_name"]
        interfaces = (relay.Node, )

class Query(AbstractType):
    all_person = DjangoFilterConnectionField(PersonNode)

class CreatePerson(relay.ClientIDMutation):
    class Input:
        firstName = graphene.String()
        lastName = graphene.String()
    
    person = graphene.Field(PersonNode)
    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        f_name = input.get('firstName')
        l_name = input.get('lastName')
        p = Person.objects.create(first_name=f_name, last_name=l_name)
        
        return CreatePerson(person=p, ok=True)

class UpdatePerson(relay.ClientIDMutation):
    class Input:
        id = graphene.String()
        firstName = graphene.String()
        lastName = graphene.String()

    person = graphene.Field(PersonNode)
    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        ok = False
        f_name = input.get('firstName')
        l_name = input.get('lastName')
        r_pk = from_global_id(input.get("id"))[1]  
        Person.objects.filter(pk=r_pk).update(
            first_name=f_name,
            last_name=l_name
        )
        result = Person.objects.get(pk=r_pk)
        ok = True
        return UpdatePerson(person=result, ok=ok)

class MutationPerson(AbstractType):
    createPerson = CreatePerson.Field()
    updatePerson = UpdatePerson.Field()
