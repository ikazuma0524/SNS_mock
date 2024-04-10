import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
import graphql_jwt
from graohene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graghql_jwt.decorators import login_required
from .models import Profile
from graghql_relay import from_global_id

class UseerNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'username' : ['exact','icontains']
        }
        interfaces = (relay.Node,)

class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = {
            'user_prof__username' : ['icontains'],
        }
        interfaces = (relay.Node,)
        
class CreateUserMutation(relay.ClientIDMutation):
    
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        
    user = graphene.Field(UserNode)
    
    def mutate_and_get_payload(root, info, **input):
        user = User(
            username = input.get('username'),
            email = input.get('email')
        )
        user.set_password(input.get('password'))
        user.save()
        return CreateUserMutation(user=user)