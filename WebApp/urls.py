from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='WebApp-home'),
    path('about/', v.about, name='WebApp-about'),
    path('test_api/', v.testApi, name='WebApp-test_api'),
    path('spec/', v.spec, name='WebApp-spec'),
    path('defects/', v.defects, name='WebApp-defects')
]
