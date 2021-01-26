from rest_framework.decorators import api_view
from django.http import JsonResponse, response, HttpResponse, FileResponse
import json
import users.models as m
import random as r
import xml.dom.minidom as xdm


@api_view(["POST"])
def GetMockResponse(request):
    api_response = {}
    api_response_status = 404
    path_striped = request.path.lstrip('/')
    json_spec_str = m.Profile.objects.get(endpoint=path_striped).json_spec
    c_d_bool = m.Profile.objects.get(endpoint=path_striped).connection_down
    i_c_i_bool = m.Profile.objects.get(endpoint=path_striped).Intermittent_connection_issues
    i_c_per = (m.Profile.objects.get(endpoint=path_striped).Intermittent_connection_per)/100
    i_c_i_chance = r.random()
    print(i_c_i_chance)
    print(i_c_per)
    json_spec = json.loads(json_spec_str.replace('\r', '').replace('\t', '').replace('\n', ''))
    # print(json_spec[0][0])
    request_type = request.META["CONTENT_TYPE"].split('/')[1]
    if request_type == 'json':
        request_body = request.body.decode('utf-8')
        if request_body[0] == '{' and  request_body[len(request_body)-1] == '}':
            request_body = json.loads(request_body)
    else:
        request_body = request.body.decode('utf-8').replace('\r', '').replace('\t', '').replace('\n', '')
        # body = json.loads(request_body).replace('\r', '').replace('\t', '').replace('\n', '')
        # print(request_body)
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
        # print(pack)
        if pack[0] == request_body:
            api_response = pack[1]
            api_response_status = pack[2]
    if request_type == "xml":
        xml_parse=True
        try:
            xml = xdm.parseString(api_response)
            xml_pretty_response = xml.toprettyxml()
        except:
            xml_parse = False

    if json_check and not c_d_bool:
        if not i_c_i_bool:
            if len(api_response) != 0:
                return JsonResponse(api_response, status=api_response_status)
            else:
                api_response["error"] = "No packed found that matches request"
                return JsonResponse(api_response, status=api_response_status)
        else:
            if i_c_i_chance <= i_c_per:
                return HttpResponse(api_c_d_response, status=404)
            else:
                if len(api_response) != 0:
                    return JsonResponse(api_response, status=api_response_status)
                else:
                    api_response["error"] = "No packed found that matches request"
                    return JsonResponse(api_response, status=api_response_status)
    elif (not json_check) and (not c_d_bool):
        # print(api_response)
        if i_c_i_bool:
            if i_c_i_chance <= i_c_per:
                return HttpResponse(api_c_d_response, status=404)
            else:
                if (len(api_response) != 0) and (request_type != "xml"):
                    return HttpResponse(api_response, status=api_response_status)

                elif (len(api_response) != 0) and (request_type == "xml"):
                    if xml_parse:
                        xml = xdm.parseString(api_response)
                        xml_pretty_response = xml.toprettyxml()
                    else:
                        xml_pretty_response = api_response
                    return HttpResponse(xml_pretty_response, content_type='application/xml')
                else:
                    api_response = "No packed found that matches request"
                    return HttpResponse(api_response, status=api_response_status)
        else:
            if (len(api_response) != 0) and (request_type != "xml"):
                return HttpResponse(api_response, status=api_response_status)

            elif (len(api_response) != 0) and (request_type == "xml"):
                if xml_parse:
                    xml = xdm.parseString(api_response)
                    xml_pretty_response = xml.toprettyxml()
                else:
                    xml_pretty_response = api_response
                return HttpResponse(xml_pretty_response, content_type='application/xml')
            else:
                api_response = "No packed found that matches request"
                return HttpResponse(api_response, status=api_response_status)
    elif c_d_bool:
        api_response = api_c_d_response
        return HttpResponse(api_response, status=404)
