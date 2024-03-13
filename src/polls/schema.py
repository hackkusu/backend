import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .decorators import has_permission
from .filters import RecipeFilter
from .models import User, Recipe
import graphene
import graphql_jwt
from graphene import relay


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "recipes")
        # interfaces = (relay.Node,)

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        filterset_class = RecipeFilter
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    # all_my_models = DjangoFilterConnectionField(UserType)
    # all_recipes = graphene.List(RecipeType)
    logged_in_user = graphene.Field(UserType, data=graphene.String(required=False))
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    protected_data = graphene.String()
    all_recipes = DjangoFilterConnectionField(RecipeType)

    def resolve_all_recipes(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        # Apply additional filtering logic here if needed, e.g., only return recipes created by the user
        queryset = Recipe.objects.filter(created_by=user)
        return queryset

    @has_permission('polls.can_create')
    # @has_permission('app.view_protected_data')
    def resolve_protected_data(self, info):
        return "Sensitive Data"

    # def resolve_all_recipes(root, info):
    #     # user = info.context.user
    #     # if not user.is_authenticated:
    #     #     raise Exception('Authentication credentials were not provided')
    #     return Recipe.objects.select_related("created_by").all()

    def resolve_logged_in_user(root, info):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        # queryset = User.objects.filter(pk=user.pk)
        return user

    def resolve_user_by_username(root, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, username, email, password):
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return CreateUser(user=user, success=True, errors=None)
        except Exception as e:
            # You might want to log this exception.
            return CreateUser(user=None, success=False, errors=[str(e)])


class Mutation(AuthMutation, graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
