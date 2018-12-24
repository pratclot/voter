"""voter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as views_auth
from django.views.generic.base import RedirectView

urlpatterns = [
    path('movies/', include('movies.urls'), name='movies'),
    path('admin/', admin.site.urls),
    path('admin', admin.site.urls),
    # url(r'^admin/?$', admin.site.urls),
    # url(r'^movies/', admin.site.urls, name='movies'),
    url(r'^login/?$', views_auth.LoginView.as_view(), name='login'),
    url(r'^logout/?$', views_auth.LogoutView.as_view(), name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^.*$',
        RedirectView.as_view(url='movies/', permanent=False),
    )
]