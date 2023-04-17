from django.db import models


class HackathonQuerySet(models.QuerySet):
    def annotate_is_registered(self, user):
        return self.annotate(
            is_registered=models.Exists(
                Registration.objects.filter(hackathon=models.OuterRef("pk"), user=user)
            )
        )


class Hackathon(models.Model):
    class SubmissionType(models.TextChoices):
        IMAGE = "image"
        FILE = "file"
        LINK = "link"

    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to="hackathon_images")
    hackathon_image = models.ImageField(upload_to="hackathon_images")
    submission_type = models.CharField(max_length=5, choices=SubmissionType.choices)
    reward_prize = models.CharField(max_length=255)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    objects = HackathonQuerySet.as_manager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_datetime__lt=models.F("end_datetime")),
                name="start_datetime_lt_end_datetime",
            )
        ]

    def __str__(self):
        return self.title


class Registration(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    registration_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "hackathon"],
                name="unique_registration",
            )
        ]


class Submission(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    summary = models.TextField()

    file = models.FileField(upload_to="hackathon_submissions", null=True)
    link = models.URLField(null=True)
    image = models.ImageField(upload_to="hackathon_submissions", null=True)

    submission_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    models.Q(file__isnull=False)
                    | models.Q(link__isnull=False)
                    | models.Q(image__isnull=False)
                ),
                name="submission_type",
            )
        ]
