from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.serializers import UserBriefSerializer
from .models import Hackathon, Registration, Submission


class HackathonSerializer(serializers.ModelSerializer):
    is_registered = serializers.BooleanField(read_only=True)

    class Meta:
        model = Hackathon
        fields = "__all__"

    def validate(self, attrs):
        start_datetime = attrs.get("start_datetime")
        end_datetime = attrs.get("end_datetime")

        if start_datetime and end_datetime:
            if start_datetime > end_datetime:
                raise ValidationError("Start datetime must be before end datetime")

        return attrs


class HackathonBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ("id", "title", "description", "hackathon_image")


class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Registration
        fields = ("user",)


class SubmissionSerializer(serializers.ModelSerializer):
    hackathon = HackathonBriefSerializer(read_only=True, source="registration.hackathon")
    user = UserBriefSerializer(read_only=True, source="registration.user")

    class Meta:
        model = Submission
        fields = ("id", "file", "link", "image", "hackathon", "user")

    def validate(self, attrs):
        crt = timezone.now()
        hackathon_id = self.context["hackathon_id"]
        user = self.context["request"].user
        try:
            registration = (
                Registration.objects
                .select_related('hackathon')
                .get(hackathon_id=hackathon_id, user=user)
            )

            # Don't allow submissions create, update after hackathon has ended
            if crt > registration.hackathon.end_datetime:
                raise ValidationError("Hackathon has ended")

            # Don't allow submissions create before hackathon has started
            if not self.instance:
                if crt < registration.hackathon.start_datetime:
                    raise ValidationError("Hackathon has not started yet")
                if crt > registration.hackathon.end_datetime:
                    raise ValidationError("Hackathon has ended")

        except Registration.DoesNotExist:
            raise ValidationError("You are not registered for this hackathon")

        hackathon = registration.hackathon

        submissions_types_to_remove = Hackathon.SubmissionType.values
        submissions_types_to_remove.remove(hackathon.submission_type)

        for submission_type in submissions_types_to_remove:
            attrs[submission_type] = None

        if attrs.get(hackathon.submission_type) is None:
            raise ValidationError(f"{hackathon.submission_type} is required")

        return attrs | {"registration": registration}
