from rest_framework.decorators import api_view
from django.http import JsonResponse, response, HttpResponse
import json
import users.models as m
import random as r
import xml.dom.minidom as xdm
import time
import threading
import requests
import ReastfulApi.modules.dynamic_mapper as dm
import ReastfulApi.modules.function_check as fc


def AsyncCall(result_url, sleep_time, result_response):
    """
        Function is used to perform async result request and will determine
        if the request should be of type xml or json
    """
    time.sleep(sleep_time)
    result_response_type = fc.CheckType(result_response)
    if result_response_type == "json":
        result_header = {'Content-Type': 'application/json'}
    elif result_response_type == "xml":
        result_header = None
    else:
        result_header = None
    print(result_header)
    response = requests.post(url=result_url, data=result_response, headers=result_header, verify=False)
    print(result_response)
    print(response)


def GetResponse(response, response_status, response_type,
                   async_bool, async_resp_time, async_result_url, result_response):
    """
        Function is used to determine what type of response to send back to user.
        Function will also trigger the async functionality when activated on the spec page.
    """
    if len(response) != 0:
        if async_bool:
            t1 = threading.Thread(target=AsyncCall, args=[async_result_url, async_resp_time, result_response])
            t1.start()
        if response_type == 'json':
            return JsonResponse(response, status=response_status)
        elif response_type == 'xml':
            xml = xdm.parseString(response)
            xml_pretty_response = xml.toprettyxml()
            return HttpResponse(xml_pretty_response, content_type='application/xml')
        else:
            return HttpResponse(response, status=response_status)
    else:
        if response_type == 'json':
            response["error"] = "No packed found that matches request"
            return JsonResponse(response, status=response_status)
        else:
            response = "No packed found that matches request"
            return HttpResponse(response, status=response_status)

@api_view(["POST"])
def GetMockResponse(request):
    """
        Function is used to lookup responses, using the sent request on the mapped spec stored on the DB.
        Function will also save the results, if matched only the matched mapped request and if not matched
        all the mapped request separated with a comma.
    """
    api_response = {}
    api_response_status = 404
    result_response = None
    api_response_type = None
    path_striped = request.path.lstrip('/')
    profile_obj = m.Profile.objects.get(endpoint=path_striped)
    json_spec_str = profile_obj.json_spec
    c_d_bool = profile_obj.connection_down
    i_c_i_bool = profile_obj.Intermittent_connection_issues
    i_c_per = (profile_obj.Intermittent_connection_per)/100
    i_c_i_chance = r.random()
    async_bool = profile_obj.async_func
    async_resp_time = profile_obj.async_result_time_delay
    async_result_url = profile_obj.async_result_url
    json_spec = json.loads(json_spec_str.replace('\r', '').replace('\t', '').replace('\n', ''))
    if (len(request.META["CONTENT_TYPE"].split('/')) == 2):
        request_type = request.META["CONTENT_TYPE"].split('/')[1]
    else:
        request_type = None
    api_c_d_response = '''  <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <title>Not Found</title>
                                </head>
                                <body>
                                    <h1>Not Found</h1>
                                    <p>The requested resource was not found on this server. </p>
                                </body>
                                </html>'''
    if request_type == 'json':
        request_body = request.body.decode('utf-8')
        try:
            request_body = json.loads(request_body)
        except json.decoder.JSONDecodeError:
            request_body = None
    else:
        request_body = request.body.decode('utf-8').replace('\r', '').replace('\t', '').replace('\n', '') \
            .replace('"', "'")

    profile_obj.result = "request:\n" + str(request_body) + "." + "\n\n" + "mapped request(s):\n"
    profile_obj.result_match = 0
    mapped_request = ""
    for pack in json_spec:
        if async_bool:
            check_match, dynamic_request, dynamic_response, dynamic_async_response = dm.Main(request_body, pack[0], pack[1], pack[3])
        else:
            check_match, dynamic_request, dynamic_response, dynamic_async_response = dm.Main(request_body, pack[0], pack[1])
        if mapped_request != str(request_body):
            mapped_request = mapped_request + str(dynamic_request) + ("." if (pack == json_spec[len(json_spec) -1]) else ",\n")
        else:
            mapped_request = mapped_request + "."
        if (check_match):
            profile_obj.result_match = 1
            api_response = dynamic_response
            api_response_status = pack[2]
            api_response_type = fc.CheckType(api_response)
            if async_bool:
                result_response = dynamic_async_response
    profile_obj.result = profile_obj.result + mapped_request
    profile_obj.save()

    if not c_d_bool:
        if not i_c_i_bool:
            return GetResponse(api_response, api_response_status, api_response_type,
                               async_bool, async_resp_time, async_result_url, result_response)
        else:
            if i_c_i_chance <= i_c_per:
                return HttpResponse(api_c_d_response, status=404)
            else:
                return GetResponse(api_response, api_response_status, api_response_type,
                                   async_bool, async_resp_time, async_result_url, result_response)
    elif c_d_bool:
        return HttpResponse(api_c_d_response, status=404)






