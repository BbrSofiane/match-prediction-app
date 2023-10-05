from django.urls import path

from match_prediction_app.core import views

urlpatterns = [
    path("", views.index, name="home"),
    path(
        "submit-prediction/<int:fixture_pk>/",
        views.submit_prediction,
        name="submit-prediction",
    ),
    path(
        "<int:prediction_pk>/delete/", views.delete_prediction, name="delete-prediction"
    ),
]
