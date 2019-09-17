from .models import User, StripeCustomer, UserProfile
import graphene
from graphene_django.types import DjangoObjectType
from .forms import UserFormCreator
# from django.shortcuts import get_object_or_404

class UserCreateOrUpdateInput(graphene.InputObjectType):
    id = graphene.Int(required= False)
    email = graphene.String(required= False)
    password = graphene.String(required= False)
    # UserProfile fields
    photo_url = graphene.String(required= False)
    photo_name = graphene.String(required= False)
    name = graphene.String(required= False)

class UserNode(DjangoObjectType):

    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )

class UserProfileNode(DjangoObjectType):

    class Meta:
        model = UserProfile
        interfaces = (graphene.relay.Node, )


class CreateOrUpdateUser(graphene.Mutation):
    class Arguments:
        user_create_or_update_input = UserCreateOrUpdateInput(required= True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)
    profile = graphene.Field(UserProfileNode)
    error = graphene.String()

    @staticmethod
    def mutate(_, info, user_create_or_update_input):

        form = UserFormCreator(user_create_or_update_input)

        if form.is_valid():
            user, profile = form.save()
            return CreateOrUpdateUser(
                user= user, 
                profile= profile, 
                ok= True, 
                error= None
                )
        else:
            raise Exception(form.top_error)

class Mutation(graphene.ObjectType):
    create_or_update_user = CreateOrUpdateUser.Field()

class Query(graphene.ObjectType):
    users = graphene.Node.Field(UserNode)
