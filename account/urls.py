from django.urls import path, reverse_lazy
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls
from django.conf import settings


from . import views
from . import forms

app_name = "account"

urlpatterns = [
    path('create/<str:token>', views.create),
    path('create/', views.create),
    path('create', views.create),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),

    path('password_reset/',         auth_views.PasswordResetView.as_view(
        from_email=settings.EMAIL_FROM,
        form_class=forms.PasswordResetForm,
        success_url=reverse_lazy("account:password_reset_done")
    ), name='password_reset'),
    path('password_reset/done/',    auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset,   name='password_reset_confirm'),
]

admin.autodiscover()
