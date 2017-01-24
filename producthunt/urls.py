"""producthunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from links.views import LinkListView
from links.views import UserProfileDetailView
from django.contrib.auth.decorators import login_required as auth # Keep non-users out
from links.views import UserProfileEditView
from links.views import LinkCreateView, LinkDetailView
from links.views import LinkEditView
from links.views import LinkDeleteView
from django.contrib import sites
from django_comments import comments

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', LinkListView.as_view(), name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(),name='profile'),
    url(r'^edit_profile/$', auth(UserProfileEditView.as_view()), name='edit_profile'),
    url(r'^link/submit/$', auth(LinkCreateView.as_view()), name='link_submit'),
    url(r'^link/(?P<pk>\d+)/$', LinkDetailView.as_view(), name='link_detail'),
    url(r'^link/edit/(?P<pk>\d+)/$', auth(LinkEditView.as_view()), name='link_edit'),
    url(r'^link/delete/(?P<pk>\d+)/$', auth(LinkDeleteView.as_view()), name='link_delete'),
    url(r'^comments/', include('django_comments.urls')),
]
