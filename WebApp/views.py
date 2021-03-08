from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import users.forms as f
from numpy import format_parser

from .forms import SpecsUpdateForm, DefectsUpdateForm, TestApi, ProjectForm, ResultsForm
from django.forms import modelformset_factory
import users.models as m
import ReastfulApi.urls as r
import ReastfulApi.views as v
from django.urls import path
import WebApiTester.urls as w
import requests
import json

def sendRequest(request_url, request_type, request_body, request_header):
    print(request_type)
    # if body_type == "JSON":
    #     header = {'Content-type': 'application/json'}
    # else:
    #     header = {'Content-type': 'application/xml'}
    if request_type == "POST":
        response = requests.post(url=request_url, headers=request_header, data=request_body)
    else:
        response = requests.put(url=request_url, headers=request_header, data=request_body)
    print(request_header)
    return response

def is_int(s):
        check = False
        try:
            int(s)
            check = True
            return check
        except ValueError:
            return check

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
def projects(request):
    context = {}
    # extras = 1 if len(m.Project.objects.filter(user=request.user)) == 0 else 0
    ProjectFormSet = modelformset_factory(m.Project, form=ProjectForm,
                                              extra=1, can_delete=True)
    template_name = 'WebApp/projects.html'
    if request.method == 'POST':
        formset = ProjectFormSet(data=request.POST,
                                     queryset=m.Project.objects.filter(user=request.user))
        if formset.is_valid():
            project = formset.save(commit=False)
            if len(project) != 0:
                for i in range(len(project)):
                    project[i].user = request.user
            formset.save()
            messages.success(request, f'Project successfully updated for the {request.user} user')
            return redirect('WebApp-home')
        else:
            messages.error(request, f'Projects could not be updated for {request.user} user')
    else:
        formset = ProjectFormSet(queryset=m.Project.objects.filter(user=request.user))
    context['formset'] = formset
    return render(request, template_name, context)
@login_required
def spec(request):
    # add error flag is None
    project_id = request.GET.get('project', '') if is_int(request.GET.get('project', '')) else -1
    if project_id != -1:
        extras = 1 if len(m.Profile.objects.filter(user=request.user, project=project_id)) == 0 else 0
        project_val = m.Project.objects.get(id=project_id)
        context ={}
        SpecsUpdateFormSet=modelformset_factory(m.Profile, form=SpecsUpdateForm,
                                                extra=extras, can_delete=True)
        template_name = 'WebApp/spec.html'
        if request.method == 'POST':
            formset = SpecsUpdateFormSet(data=request.POST,
                                         queryset=m.Profile.objects.filter(user=request.user, project=project_id))
            if formset.is_valid():
                profile = formset.save(commit=False)
                if len(profile) != 0:
                    print(profile[0].id)
                    for i in range(len(profile)):
                        profile[i].user = request.user
                        profile[i].project = project_val
                        profile[i].endpoint = profile[i].endpoint.strip()
                        profile[i].endpoint = profile[i].endpoint.lstrip('/')
                        profile[i].endpoint = profile[i].endpoint.rstrip('/')
                        profile_endpoint_list = profile[i].endpoint.split('/')
                        profile_endpoint_check = (str(request.user.id) == profile_endpoint_list[len(profile_endpoint_list)-1]
                                                  and str(project_id) == profile_endpoint_list[len(profile_endpoint_list)-2])
                        if (profile_endpoint_check == False):
                            profile[i].endpoint = str(profile[i].endpoint).rstrip('/') + '/' + str(project_id) + '/' + str(request.user.id)
                        # profile[i].save()
                formset.save()
                r.urlpatterns = [path(p['endpoint'], v.GetMockResponse) for p in list(m.Profile.objects.all().values('endpoint'))]
                w.urlpatterns[3].url_patterns = r.urlpatterns

                messages.success(request, f'Specs successfully updated for the {request.user} user')
                return redirect('WebApp-projects')
            else:
                messages.error(request, f'Specs could not be updated for {request.user} user')
                # print(formset.errors)

        else:
            formset = SpecsUpdateFormSet(queryset=m.Profile.objects.filter(user=request.user, project=project_id))
        context['formset'] = formset
    else:
        messages.error(request, f'This project has not yet been created')
        return redirect('WebApp-projects')
    return render(request, template_name, context)

@login_required
def defects(request):
    project_id = request.GET.get('project', '') if is_int(request.GET.get('project', '')) else -1
    print(project_id)
    if project_id != -1:
        extras = 1 if len(m.Profile.objects.filter(user=request.user, project=project_id)) == 0 else 0
        context = {}
        template_name = 'WebApp/defects.html'
        DefectsUpdateFormSet=modelformset_factory(m.Profile, form=DefectsUpdateForm,
                                                extra=extras, can_delete=True)
        if request.method == 'POST':
            formset = DefectsUpdateFormSet(data=request.POST,
                                         queryset=m.Profile.objects.filter(user=request.user, project=project_id))
            if formset.is_valid():
                formset.save()
                messages.success(request, f'Defects successfully updated for the {request.user} user')
                return redirect('WebApp-projects')
            else:
                messages.error(request, f'Defects could not be updated for {request.user} user')
        else:
            formset = DefectsUpdateFormSet(queryset=m.Profile.objects.filter(user=request.user, project=project_id))
        context['formset'] = formset
    else:
        messages.error(request, f'This project has not yet been created')
        return redirect('WebApp-projects')
    return render(request, template_name, context)

@login_required
def testApi(request):
    context = {}
    template_name = 'WebApp/test_api.html'
    if request.method == 'POST':
        form = TestApi(request.POST)
        print("Hello")
        if form.is_valid():
            api_url = form.data['api_url']
            api_request_type = form.data['api_request_type']
            # api_body_type = form.data['api_type']
            api_body = form.data['api_body']
            api_header = json.loads(form.data['api_header'])
            print(api_header)
            response = sendRequest(api_url, api_request_type, api_body, api_header)
            print(response)
            messages.success(request, 'request sent')
        else:
            messages.error(request, 'request not sent')
    else:
        form = TestApi()
    context['form'] = form
    return render(request, template_name, context)

@login_required
def results(request):
    project_id = request.GET.get('project', '') if is_int(request.GET.get('project', '')) else -1
    print(project_id)
    if project_id != -1:
        profile_num_packets = len(m.Profile.objects.filter(user=request.user, project=project_id))
        extras = 1 if profile_num_packets == 0 else 0
        context = {}
        template_name = 'WebApp/results.html'
        for i in range(profile_num_packets):
            if (m.Profile.objects.filter(user=22, project=24).values()[i]["result_match"]):
                messages.add_message(request, 25, "Request matches specs mapped")
                # messages.success(request, "Request matches specs mapped")
            else:
                messages.add_message(request, 40, "Request does not matches specs mapped")
                # messages.error(request, "Request does not matches specs mapped")
        ResultsFormSet=modelformset_factory(m.Profile, form=ResultsForm,
                                                extra=extras, can_delete=True)
        formset = ResultsFormSet(queryset=m.Profile.objects.filter(
                                            user=request.user, project=project_id))
        storage = messages.get_messages(request)
        formset = zip(storage, formset)
        context['formset'] = formset
    else:
        messages.error(request, f'This project has not yet been created')
        return redirect('WebApp-projects')
    return render(request, template_name, context)