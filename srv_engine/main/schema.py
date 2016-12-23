import graphene
from graphene import relay, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Person

class PersonNode(DjangoObjectType):

    class Meta:
        model = Person
        filter_fields = ["id", "first_name", "last_name"]
        interfaces = (relay.Node, )

class Query(AbstractType):
    all_person = DjangoFilterConnectionField(PersonNode)

class CreatePerson(graphene.Mutation):
    class Input:
        firstName = graphene.String()
        lastName = graphene.String()
    
    person = graphene.Field(PersonNode)
    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        f_name = args.get('firstName')
        l_name = args.get('lastName')
        p = Person.objects.create(first_name=f_name, last_name=l_name)
        # result_person = PersonNode(p)
        return CreatePerson(person=p, ok=True)

class MutationPerson(AbstractType):
    createPerson = CreatePerson.Field()
