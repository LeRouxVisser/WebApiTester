from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import users.forms as f
from .forms import SpecsUpdateForm, DefectsUpdateForm
from django.forms import modelformset_factory
import users.models as m
import ReastfulApi.urls as r
import ReastfulApi.views as v
from django.urls import path
import WebApiTester.urls as w

def home(request):
    if request.method == 'POST':
        u_form = f.UserUpdateForm(request.POST
                                  , instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'{request.user} information updated successfully')
            return redirect('WebApp-home')

        else:
            messages.error(request, f'{request.user} information could not be updated')

    else:
        # print(str(request.user) == 'AnonymousUser')
        if str(request.user) == 'AnonymousUser':
            u_form = f.UserUpdateForm()
        else:
            u_form = f.UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'WebApp/home.html', context)

def about(request):
    print(request.path)
    return render(request, 'WebApp/about.html')

@login_required
def spec(request):
    context ={}
    SpecsUpdateFormSet=modelformset_factory(m.Profile, form=SpecsUpdateForm,
                                            extra=0, can_delete=True)
    template_name = 'WebApp/spec.html'
    if request.method == 'POST':
        formset = SpecsUpdateFormSet(data=request.POST,
                                     queryset=m.Profile.objects.filter(user=request.user))
        if formset.is_valid():
            profile = formset.save(commit=False)
            if len(profile) != 0:
                print(profile[0].id)
                for i in range(len(profile)):
                    profile[i].user = request.user
                    profile[i].endpoint = profile[i].endpoint.strip()
                    profile[i].endpoint = profile[i].endpoint.lstrip('/')
                    profile[i].endpoint = profile[i].endpoint.rstrip('/')
                    profile_endpoint_list = profile[i].endpoint.split('/')
                    profile_endpoint_check = (str(request.user.id) == profile_endpoint_list[len(profile_endpoint_list)-1])
                    if (profile_endpoint_check == False):
                        profile[i].endpoint = str(profile[i].endpoint).rstrip('/') + '/' + str(request.user.id)
                    # profile[i].save()
            formset.save()
            r.urlpatterns = [path(p['endpoint'], v.GetMockResponse) for p in list(m.Profile.objects.all().values('endpoint'))]
            w.urlpatterns[3].url_patterns = r.urlpatterns

            messages.success(request, f'Specs successfully updated for the {request.user} user')
            return redirect('WebApp-home')
        else:
            messages.error(request, f'Specs could not be updated for {request.user} user')
            # print(formset.errors)

    else:
        formset = SpecsUpdateFormSet(queryset=m.Profile.objects.filter(user=request.user))
    context['formset'] = formset

    return render(request, template_name, context)

@login_required
def defects(request):
    context = {}
    template_name = 'WebApp/defects.html'
    DefectsUpdateFormSet=modelformset_factory(m.Profile, form=DefectsUpdateForm,
                                            extra=0, can_delete=True)
    if request.method == 'POST':
        formset = DefectsUpdateFormSet(data=request.POST,
                                     queryset=m.Profile.objects.filter(user=request.user))
        if formset.is_valid():
            formset.save()
            messages.success(request, f'Defects successfully updated for the {request.user} user')
            return redirect('WebApp-home')
        else:
            messages.error(request, f'Defects could not be updated for {request.user} user')
    else:
        formset = DefectsUpdateFormSet(queryset=m.Profile.objects.filter(user=request.user))
    context['formset'] = formset
    return render(request, template_name, context)

