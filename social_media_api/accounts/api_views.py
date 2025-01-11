from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from accounts.models import UserProfile
from accounts.views import CustomAuthToken
from .serializers import CustomUserSerializer, LoginSerializer, LogoutSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.CreateAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        print("user authenticated?", request.user.is_authenticated)
        print(request.user.auth_token)
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
        return Response("user not logged in")

# allow anyone ot view a user's profile


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer

    def retrieve(self, request, user_id, * args, **kwargs):
        try:
            profile = UserProfile.objects.select_related(
                'user').get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""Custom permission to only allow owners of a profile to edit it."""


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        # Retrieve the profile associated with the authenticated user.
        return self.request.user.profile


class ProfileDeleteView(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user.profile

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.delete()
        return Response({"message": "Profile and corresponding user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#    def update(self, request, *args, **kwargs):
#        instance = self.get_object()
#        user = instance.user
#        instance.delete()
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
#
#    def get_object(self):
#        # Retrieve the profile associated with the authenticated user.
#        return self.request.user.profile
