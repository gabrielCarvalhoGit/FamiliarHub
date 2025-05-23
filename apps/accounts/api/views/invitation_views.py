from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.core.utils.permissions import UserPermission
from apps.core.utils.pagination import CustomPagination

from apps.accounts.services import UserInvitationService
from apps.accounts.api.serializers import InvitationRequestSerializer, InvitationResponseSerializer, InvitationAcceptedRequestSerializer


class UserInvitationView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = InvitationRequestSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuserinvitation'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = UserInvitationService()

    def get(self, request):
        paginator = CustomPagination()

        invitations = self.__service.get_not_accepted(request)
        page = paginator.paginate_queryset(invitations, request)

        response = InvitationResponseSerializer(page, many=True)
        return paginator.get_paginated_response(response.data, resource_name='pending_invitations')

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.__service.create_invitation(request.user, **serializer.validated_data)
            return Response({'detail': 'User invited successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        token = request.query_params.get('token')
        invitation = self.__service.get_invitation(token)

        self.__service.resend_invitation(invitation, request)
        return Response({'detail': 'User invitation resent successfully.'})

class UserInvitationAcceptedView(APIView):
    permission_classes = [AllowAny]
    serializer_class = InvitationAcceptedRequestSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuserinvitation'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = UserInvitationService()
    
    def post(self, request):
        token = request.query_params.get('token')

        if token:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                self.__service.accept_invitation(token, **serializer.validated_data)
                return Response({'detail': 'invitation successfully accepted.'})

            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)