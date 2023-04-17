from django.urls import path

from hackathon import views

urlpatterns = [
    path("", views.HackathonViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:hackathon_id>/",
         views.HackathonViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("<int:hackathon_id>/register/", views.CreateRegistrationView.as_view()),

    path("<int:hackathon_id>/submission/", views.UserSubmissionViewSet.as_view(
        {"get": "retrieve", "post": "create", "put": "update", "delete": "destroy"})),
    path("<int:hackathon_id>/submission/all/", views.HackathonSubmissionListView.as_view()),
]
