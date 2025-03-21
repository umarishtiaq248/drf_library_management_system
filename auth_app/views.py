from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from auth_app.serializers import AuthenticationSerializer, CRUDSerializer
from auth_app.models import CustomUser
from rest_framework.exceptions import PermissionDenied


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "Successfully logged out"})


class UserCreateView(CreateAPIView):
    serializer_class = CRUDSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(UpdateAPIView):
    serializer_class = CRUDSerializer

    def get_queryset(self):
        return CustomUser.objects.all()


class UserDeleteView(DestroyAPIView):
    serializer_class = CRUDSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            raise PermissionDenied("Admins cannot delete their own account.")
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()
        user.delete()
        return Response(
            {"detail": "Your account has been deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserListView(ListAPIView):
    serializer_class = CRUDSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return CustomUser.objects.all()
