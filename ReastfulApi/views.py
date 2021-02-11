from rest_framework.decorators import api_view
from django.http import JsonResponse, response, HttpResponse
import json
import users.models as m
import random as r
import xml.dom.minidom as xdm
import time
import threading
import requests

def CheckType(packet):
    packet_type = None
    if (isinstance(packet, dict)):
        packet_type = 'json'
    else:
        try:
            xdm.parseString(packet)
            packet_type = 'xml'
        except xdm.xml.parsers.expat.ExpatError:
            pass
    return packet_type


def AsyncCall(result_url, sleep_time, result_response):
    time.sleep(sleep_time)
    result_response_type = CheckType(result_response)
    if result_response_type == "json":
        result_header = {'Content-type': 'application/json'}
    elif result_response_type == "xml":
        result_header = {'Content-type': 'application/xml'}
    else:
        result_header = None
    print(result_header)
    response = requests.post(url=result_url, data=result_response, headers=result_header)
    print(result_response)
    print(response)

def GetResponse(response, response_status, response_type,
                   async_bool, async_resp_time, async_result_url, result_response):
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
    api_response = {}
    api_response_status = 404
    result_response = None
    api_response_type = None
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
        if request_body[0] == '{' and request_body[len(request_body)-1] == '}':
            request_body = json.loads(request_body)
    else:
        request_body = request.body.decode('utf-8').replace('\r', '').replace('\t', '').replace('\n', '')

    for pack in json_spec:
        if pack[0] == request_body:
            api_response = pack[1]
            api_response_status = pack[2]
            api_response_type = CheckType(api_response)
            if async_bool:
                result_response = pack[3]

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






