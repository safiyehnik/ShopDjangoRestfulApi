from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from users.serializer.profile_serializer import ProfileUpdateSerializer, ProfileSerializer
from users.serializer.user_serializer import UserSerializer


class ProfileView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    # queryset = get_user_model()
    # serializer_class = UserSerializer()

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.pk)

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "PATCH":
            return ProfileUpdateSerializer
        return ProfileSerializer

