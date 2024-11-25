"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_sample_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from autocomplete import urls as autocomplete_urls
from sample_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("teams/<int:team_id>/edit/", views.edit_team, name="edit_team"),
    path(
        "teams/<int:team_id>/edit/with_prefix/",
        views.example_with_prefix,
        name="edit_team_w_prefix",
    ),
    path("teams/<int:team_id>/edit3/", views.example_with_model, name="edit_team3"),
    path("ac/", autocomplete_urls),
    path("app/__debug__/", include("debug_toolbar.urls")),
]
