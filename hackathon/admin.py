from django.contrib import admin

from .models import Submission, Registration, Hackathon

admin.site.register(Submission)
admin.site.register(Registration)
admin.site.register(Hackathon)
