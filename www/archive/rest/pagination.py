from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom default limit offset pagination
    """
    default_limit = 20
    max_limit = 100
