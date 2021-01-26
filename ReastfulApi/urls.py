from django.urls import path
import users.models as m
from . import views as v

urlpatterns = [path(p['endpoint'], v.GetMockResponse) for p in list(m.Profile.objects.all().values('endpoint'))]
