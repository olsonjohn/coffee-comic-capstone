"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path

from ComicBaseApp.views import (
    index,
    AddCommentView,
    SignupView,
    LoginView,
    logout_view,
    ComicDetailView,
    profile_view,
    AddFavoriteView,
    CheckoutView,
    HoldView,
    AddToDB,
    SearchResultsView
)

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path("add_comment/<int:id>/", AddCommentView.as_view(), name="add_comment"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("comicinfo/<int:id>/", ComicDetailView.as_view(), name="comicinfo"),
    path("profile/<str:username>/", profile_view, name="profile_view"),
    path("add_favorite/<int:id>/", AddFavoriteView.as_view(), name="favorite_view"),
    path("checkout/<int:id>/", CheckoutView.as_view(), name="checkout_view"),
    path("hold/<int:id>/", HoldView.as_view(), name="hold_view"),
    path("db_add/<int:id>/", AddToDB.as_view(), name="db_add"),
    path("search/", SearchResultsView.as_view(), name="search_results")
    
]

handler404 = "ComicBaseApp.views.e404"
handler500 = "ComicBaseApp.views.e500"
