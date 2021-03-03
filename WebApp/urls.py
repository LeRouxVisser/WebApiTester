from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='WebApp-home'),
    path('about/', v.about, name='WebApp-about'),
    path('test_api/', v.testApi, name='WebApp-test_api'),
    path('projects/', v.projects, name='WebApp-projects'),
    path('defects/', v.defects, name='WebApp-defects'),
    path('specs/', v.spec, name='WebApp-specs')
]
