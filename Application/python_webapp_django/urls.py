"""
Definition of urls for python_webapp_django.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.views.decorators.csrf import csrf_exempt

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^maps$', app.views.maps, name='maps'),
    url(r'^camps', app.views.returnClosestCamps, name='camps'),
    url(r'^newref/$', app.views.AddNewRefugee, name='newRef'),
    url(r'^viewresc/$', app.views.viewResources, name='viewResc'),
    # url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    # url(r'^rescueadd$', app.views.AddRescueSpot)
    url(r'^rescueadd$', csrf_exempt(app.views.AddRescueSpot))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
