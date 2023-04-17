from django.db import IntegrityError
from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import ValidationError

from .models import Hackathon, Registration, Submission
from .serializers import HackathonSerializer, RegistrationSerializer, SubmissionSerializer


class HackathonViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = "hackathon_id"
    lookup_field = "id"
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    serializer_class = HackathonSerializer

    def get_queryset(self):
        qs = Hackathon.objects.annotate_is_registered(self.request.user)
        if self.request.query_params.get("is_registered") == "true":
            qs = qs.filter(registration__user=self.request.user)
        return qs


class CreateRegistrationView(generics.CreateAPIView):
    lookup_url_kwarg = "hackathon_id"
    queryset = Registration.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer: RegistrationSerializer):
        try:
            hackathon = Hackathon.objects.get(id=self.kwargs["hackathon_id"])
            serializer.save(hackathon=hackathon)
        except Hackathon.DoesNotExist:
            raise ValidationError("Hackathon does not exist")
        except IntegrityError:
            raise ValidationError("You are already registered for this hackathon")


class UserSubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubmissionSerializer
    lookup_field = "registration__hackathon_id"
    lookup_url_kwarg = "hackathon_id"

    def get_serializer_context(self):
        return {'hackathon_id': self.kwargs['hackathon_id']} | super().get_serializer_context()

    def get_queryset(self):
        return (
            Submission.objects
            .filter(registration__user=self.request.user)
            .select_related('registration__hackathon', 'registration__user')
        )


class HackathonSubmissionListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubmissionSerializer
    lookup_field = "id"
    lookup_url_kwarg = "submission_id"

    def get_queryset(self):
        return (
            Submission.objects
            .filter(registration__hackathon_id=self.kwargs['hackathon_id'])
            .select_related('registration__hackathon', 'registration__user')
        )

    def check_permissions(self, request):
        super().check_permissions(request)
        # user with privileges to create hackathon can view all submissions
        if not request.user.is_superuser and not request.user.has_perms(['hackathon.can_add_hackathon']):
            self.permission_denied(
                request,
                message="You don't have permission to view submissions",
                code='permission_denied'
            )
