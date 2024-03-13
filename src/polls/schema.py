import graphene
from graphene_django import DjangoObjectType

from .decorators import has_permission
from .models import User, Recipe
import graphene
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "recipes")

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        fields = ("id", "name", "ingredients", "instructions", "created_by")

class Query(graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    protected_data = graphene.String()

    @has_permission('polls.can_create')
    # @has_permission('app.view_protected_data')
    def resolve_protected_data(self, info):
        return "Sensitive Data"

    def resolve_all_recipes(root, info):
        # user = info.context.user
        # if not user.is_authenticated:
        #     raise Exception('Authentication credentials were not provided')
        return Recipe.objects.select_related("created_by").all()

    def resolve_user_by_username(root, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
