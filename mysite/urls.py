"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
import settings
from view import *

urlpatterns = patterns('',
	(r'^site_media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.STATIC_PATH}),
	(r'^index/', index),	
    (r'^createSample/$', createSample),
    (r'^search/$', search),
    (r'^SampleRegression/',SampleRegression),
    (r'^getCompound/$',getCompound),
    (r'^regression/$',regression),
    (r'^compound/$',compound),
    (r'^addCompound/$', addCompound),
    (r'^mixCor/$', mixCor),
    (r'^removeItem/$',removeItem),
    (r'^getData/$',getData),
)