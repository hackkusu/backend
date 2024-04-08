from functools import wraps

def user_passes_test(test_func):
    def decorator(resolver):
        @wraps(resolver)
        def wrapper(self, info, **kwargs):
            if not test_func(info.context.user):
                raise Exception("You do not have permission to perform this action")
            return resolver(self, info, **kwargs)
        return wrapper
    return decorator

def has_permission(permission):
    def has_perm(user):
        return user.has_perm(permission)
    return user_passes_test(has_perm)
