import graphene

import srv_engine.main.schema as main_schema


class Query(main_schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(main_schema.MutationPerson, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)