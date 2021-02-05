from rest_framework.decorators import api_view
from django.http import JsonResponse, response, HttpResponse
import json
import users.models as m
import random as r
import xml.dom.minidom as xdm
import time
import threading
import requests

def async_call(result_url, sleep_time, result_response):
    time.sleep(sleep_time)
    response = requests.post(url=result_url, data=result_response)
    print(result_response)
    print(response)

def pack_not_found(response, response_status, json_check, xml_parse, async_bool, async_resp_time, async_result_url, result_response):
    if len(response) != 0:
        if async_bool:
            t1 = threading.Thread(target=async_call, args=[async_result_url, async_resp_time, result_response])
            t1.start()
        if json_check:
            return JsonResponse(response, status=response_status)
        elif xml_parse:
            xml = xdm.parseString(response)
            xml_pretty_response = xml.toprettyxml()
            return HttpResponse(xml_pretty_response, content_type='application/xml')
        else:
            return HttpResponse(response, status=response_status)
    else:
        if json_check:
            response["error"] = "No packed found that matches request"
            return JsonResponse(response, status=response_status)
        else:
            response = "No packed found that matches request"
            return HttpResponse(response, status=response_status)

@api_view(["POST"])
def GetMockResponse(request):
    api_response = {}
    api_response_status = 404
    xml_parse = False
    result_response = None
    path_striped = request.path.lstrip('/')
    json_spec_str = m.Profile.objects.get(endpoint=path_striped).json_spec
    c_d_bool = m.Profile.objects.get(endpoint=path_striped).connection_down
    i_c_i_bool = m.Profile.objects.get(endpoint=path_striped).Intermittent_connection_issues
    i_c_per = (m.Profile.objects.get(endpoint=path_striped).Intermittent_connection_per)/100
    i_c_i_chance = r.random()
    print(i_c_i_chance)
    print(i_c_per)
    async_bool = m.Profile.objects.get(endpoint=path_striped).async_func
    async_resp_time = m.Profile.objects.get(endpoint=path_striped).async_result_time_delay
    async_result_url = m.Profile.objects.get(endpoint=path_striped).async_result_url

    json_spec = json.loads(json_spec_str.replace('\r', '').replace('\t', '').replace('\n', ''))
    request_type = request.META["CONTENT_TYPE"].split('/')[1]
    if request_type == 'json':
        request_body = request.body.decode('utf-8')
        if request_body[0] == '{' and request_body[len(request_body)-1] == '}':
            request_body = json.loads(request_body)
    else:
        request_body = request.body.decode('utf-8').replace('\r', '').replace('\t', '').replace('\n', '')
    json_check = isinstance(request_body, dict)
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

    for pack in json_spec:
        if pack[0] == request_body:
            api_response = pack[1]
            api_response_status = pack[2]
            if async_bool:
                result_response = pack[3]
    if request_type == "xml":
        try:
            xdm.parseString(api_response)
            xml_parse = True
        except:
            xml_parse = False

    if not c_d_bool:
        if not i_c_i_bool:
            return pack_not_found(api_response, api_response_status, json_check, xml_parse
                                  , async_bool, async_resp_time, async_result_url, result_response)
        else:
            if i_c_i_chance <= i_c_per:
                return HttpResponse(api_c_d_response, status=404)
            else:
                return pack_not_found(api_response, api_response_status, json_check, xml_parse,
                                      async_bool, async_resp_time, async_result_url, result_response)
    elif c_d_bool:
        return HttpResponse(api_c_d_response, status=404)






