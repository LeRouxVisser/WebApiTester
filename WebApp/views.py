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
from WebApiTester import urls as w
import requests
import json

def sendRequest(request_url, request_type, request_body, request_header):
    """
        Function is used to send request sent from the Request page.
    """
    # if body_type == "JSON":
    #     header = {'Content-type': 'application/json'}
    # else:
    #     header = {'Content-type': 'application/xml'}
    if request_type == "POST":
        response = requests.post(url=request_url, headers=request_header, data=request_body)
    else:
        response = requests.put(url=request_url, headers=request_header, data=request_body)
    return response

def is_int(s):
    """
        Function is used to check if a variable is of type int.
    """
    check = False
    try:
        int(s)
        check = True
        return check
    except ValueError:
        return check

def home(request):
    """
        Function is used to render the home page.
    """
    u_form = f.UserUpdateForm()
    context = {
        'u_form': u_form
    }

    return render(request, 'WebApp/home.html', context)

@login_required
def projects(request):
    """
        Function will only execute if user is logged in.
        Function will pull up all the users projects and render the screen Project screen.
    """
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
            # m.Profile.objects.filter(project__isnull=True).delete()
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
    """
        Function will only execute if user is logged in.
        Function will pull up all the users specs bound to parent project
        and render the Spec screen accordingly.
    """
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
    """
        Function will only execute if user is logged in.
        Function will pull up all the users defects bound to parent project
        and render the Defects screen accordingly.
    """
    project_id = request.GET.get('project', '') if is_int(request.GET.get('project', '')) else -1
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
    """
        Function will only execute if user is logged in.
        Function will render the Request screen.
    """
    context = {}
    template_name = 'WebApp/test_api.html'
    if request.method == 'POST':
        form = TestApi(request.POST)
        if form.is_valid():
            api_url = form.data['api_url']
            api_request_type = form.data['api_request_type']
            # api_body_type = form.data['api_type']
            api_body = form.data['api_body']
            api_header = json.loads(form.data['api_header'])
            response = sendRequest(api_url, api_request_type, api_body, api_header)
            messages.success(request, 'request sent')
        else:
            messages.error(request, 'request not sent')
    else:
        form = TestApi()
    context['form'] = form
    return render(request, template_name, context)

@login_required
def results(request):
    """
        Function will only execute if user is logged in.
        Function will pull up the latest results for the users given parent project
        and render the Result screen accordingly.
    """
    project_id = request.GET.get('project', '') if is_int(request.GET.get('project', '')) else -1
    if project_id != -1:
        profile_num_packets = len(m.Profile.objects.filter(user=request.user, project=project_id))
        extras = 1 if profile_num_packets == 0 else 0
        context = {}
        template_name = 'WebApp/results.html'
        for i in range(profile_num_packets):
            if (m.Profile.objects.filter(user=request.user, project=project_id).values()[i]["result_match"]):
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