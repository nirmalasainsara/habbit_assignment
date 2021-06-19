from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "assignment"

urlpatterns = [
    path("add_course/", views.CourseView.as_view(), name="add_course"),
    path(
        "course_detail/<int:id>/",
        views.CourseDetailView.as_view(),
        name="course_detail",
    ),
    path("register/", views.RegisterView.as_view(), name="Register"),
    path(
        "forgot_password/", views.ForgotPasswordView.as_view(), name="forgot_password"
    ),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
]
