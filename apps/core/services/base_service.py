from django.db import DatabaseError
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied, APIException


class ServiceBase(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                attrs[attr_name] = ServiceBaseDecorator(attr_value)
        return super().__new__(cls, name, bases, attrs)

def ServiceBaseDecorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound as e:
            raise e
        except ValidationError as e:
            raise e
        except PermissionDenied as e:
            raise e
        except ValueError as e:
            raise APIException(str(e))
        except DatabaseError as e:
            raise APIException(f'Database error. {str(e)}') from e
        except Exception as e:
            raise APIException(f'Unexpected error. {str(e)}') from e
        
    return wrapper