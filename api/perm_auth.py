from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication as BaseTokenAuth

class TokenAuthentication(BaseTokenAuth):
    """keyword = 'Berear'"""


class PermissionsAndAuthentication():
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]