from bs4 import BeautifulSoup
import ReastfulApi.modules.function_check as fc
def Main(request,request_mapped=None,response_mapp=None,async_response_mapp=None):
    request_type_check = fc.CheckType(request)
    if request_type_check == 'xml':
        check_match, dynamic_request, dynamic_response, dynamic_async_response = DynamicXml(request, request_mapped, response_mapp, async_response_mapp)

    elif request_type_check == 'json':
        check_match, dynamic_request, dynamic_response, dynamic_async_response = DynamicJson(request, request_mapped, response_mapp, async_response_mapp)

    else:
        check_match = (request == request_mapped)
        dynamic_request = request_mapped
        dynamic_response = response_mapp
        dynamic_async_response = async_response_mapp
    return check_match, dynamic_request, dynamic_response, dynamic_async_response


def DynamicXml(xml_request, xml_request_mapped, xml_response_mapped, xml_async_response_mapp):
    soup_request = BeautifulSoup(xml_request, "xml")
    soup_request_mapped = BeautifulSoup(xml_request_mapped, "xml")
    response_check = False
    check_match = False
    value_map_dic = {}
    try:
        soup_response_mapped = BeautifulSoup(xml_response_mapped, "xml")
        response_check = True
        soup_async_response_mapp = BeautifulSoup(xml_async_response_mapp, "xml")
    except TypeError:
        if (response_check):
            soup_async_response_mapp = xml_async_response_mapp
        else:
            soup_response_mapped = xml_response_mapped
            soup_async_response_mapp = xml_async_response_mapp

    srm_tag_value = [tag.text for tag in soup_request_mapped.findAll()]
    srm_tag_name = [tag.name for tag in soup_request_mapped.findAll()]
    for i in range(len(srm_tag_value)):
        if ('\n' not in srm_tag_value[i]) and (' ' not in srm_tag_value[i]) and ('?' in srm_tag_value[i]):
            try:
                request_value = soup_request.find(srm_tag_name[i]).text
                value_map_dic[srm_tag_value[i]] = request_value
                print(value_map_dic)
            except AttributeError:
                print('Tag not in request/response')
    names_mapping_srm = [[srm_tag_name[ix], value_map_dic[srm_tag_value[ix]]] for ix in range(len(srm_tag_value)) if
                 srm_tag_value[ix] in list(value_map_dic.keys())]
    try:
        for name in names_mapping_srm:
            print(name[0])
            soup_request_mapped.find(name=name[0]).string = name[1]
        check_match = (soup_request_mapped == soup_request)
    except AttributeError:
        print('Tag not in request/response')
    print(check_match)
    if (check_match):
        try:
            srsm_tag_value = [tag.text for tag in soup_response_mapped.findAll()]
            srsm_tag_name = [tag.name for tag in soup_response_mapped.findAll()]
            names_mapping_srsm = [[srsm_tag_name[ix], value_map_dic[srsm_tag_value[ix]]] for ix in range(len(srsm_tag_value)) if
                          srsm_tag_value[ix] in list(value_map_dic.keys())]
            for name in names_mapping_srsm:
                soup_response_mapped.find(name=name[0]).string = name[1]

            sarsm_tag_value = [tag.text for tag in soup_async_response_mapp.findAll()]
            sarsm_tag_name = [tag.name for tag in soup_async_response_mapp.findAll()]
            names_mapping_sarsm = [[sarsm_tag_name[ix], value_map_dic[sarsm_tag_value[ix]]] for ix in
                           range(len(sarsm_tag_value)) if
                           sarsm_tag_value[ix] in list(value_map_dic.keys())]
            for name in names_mapping_sarsm:
                soup_async_response_mapp.find(name=name[0]).string = name[1]
        except AttributeError:
            print('Tag not in request/response')

    return check_match, soup_request_mapped, str(soup_response_mapped), str(soup_async_response_mapp)


def DynamicJson(json_request, json_request_mapp, json_response_mapp, json_async_response_mapp):
    value_map_dic = {}
    for k, v in json_request_mapp.items():
        if '?' in v:
            try:
                request_value = json_request[k]
                value_map_dic[v] = request_value
            except KeyError:
                print('Key not in request/response')
    names_mapping_srm = [[kx, value_map_dic[vx]] for kx, vx in json_request_mapp.items() if
                     vx in list(value_map_dic.keys())]
    for name in names_mapping_srm:
        json_request_mapp[name[0]] = name[1]
    check_match = (json_request_mapp == json_request)

    if (check_match):
        try:
            names_mapping_srsm = [[kx, value_map_dic[vx]] for kx, vx in json_response_mapp.items() if
                     vx in list(value_map_dic.keys())]
            for name in names_mapping_srsm:
                json_response_mapp[name[0]] = name[1]
            names_mapping_sarsm = [[kx, value_map_dic[vx]] for kx, vx in json_async_response_mapp.items() if
                                  vx in list(value_map_dic.keys())]
            for name in names_mapping_sarsm:
                json_async_response_mapp[name[0]] = name[1]
        except (KeyError, AttributeError):
                print('Key not in request/response')

    return check_match, json_request_mapp, json_response_mapp, json_async_response_mapp

if __name__ == '__main__':
    request_json = {
			"input_Amount": "0.36",
			"input_Country": "223311",
			"input_Currency": "GHS",
			"input_PrimaryPartyCode": "151515",
			"input_ReceiverPartyCode": "223311",
			"input_ThirdPartyConversationID": "1119585566543",
			"input_TransactionReference": "cpt80960034356",
			"input_PurchasedItemsDesc": "Shoes"
            }
    request_mapp_json = {
			"input_Amount": "0.36",
			"input_Country": "?1",
			"input_Currency": "GHS",
			"input_PrimaryPartyCode": "151515",
			"input_ReceiverPartyCode": "?1",
			"input_ThirdPartyConversationID": "1119585566543",
			"input_TransactionReference": "cpt80960034356",
			"input_PurchasedItemsDesc": "Shoes"
            }
    response_mapp_json = {
              "output_ResponseCode": "INS-0",
              "output_ResponseDesc": "Request processed successfully",
              "output_TransactionID": "?1",
              "output_ConversationID": "?2",
              "output_ThirdPartyConversationID": "1119585566543"
            }

    asynce_response_mapp_json = {
        "input_OriginalConversationID": "5b28bbba9e7a420d93b47813d11ba080",
        "input_TransactionID": "resultReverse.res:ReceiptNumber",
        "input_ResultCode": "INS-resultMain.res:ResultCode",
        "input_ResultDesc": "resultMain.res:ResultDesc",
        "input_ThirdPartyConversationID": "",
        "input_ResponseTransactionStatus": None
}

    xml_request = '''
    <soapenv:Envelope 
    xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
    xmlns:api='http://cps.huawei.com/cpsinterface/api_requestmgr' 
    xmlns:com='http://cps.huawei.com/cpsinterface/common'
    xmlns:req='http://cps.huawei.com/cpsinterface/request'>
       <soapenv:Header />
       <soapenv:Body>
          <api:Request>
             <req:Header>
                <req:Version>1.0</req:Version>
                <req:CommandID>TEST_MOCK_G2</req:CommandID>
                <req:OriginatorConversationID>2</req:OriginatorConversationID>
                <req:Caller>
                   <req:CallerType>2</req:CallerType>
                   <req:ThirdPartyID>12</req:ThirdPartyID>
                   <req:Password>=dsmoedmowsedf</req:Password>
                   <req:ResultURL>https://www.google.com</req:ResultURL>
                </req:Caller>
                <req:KeyOwner>1</req:KeyOwner>
                <req:Timestamp>12</req:Timestamp>
             </req:Header>
             <req:Body>
                <req:Identity>
                   <req:Initiator>
                      <req:IdentifierType>1</req:IdentifierType>
                      <req:Identifier>sdsfd</req:Identifier>
                      <req:SecurityCredential>grfdfg</req:SecurityCredential>
                   </req:Initiator>
                   <req:ReceiverParty>
                      <req:IdentifierType>4</req:IdentifierType>
                      <req:Identifier>dfgc</req:Identifier>
                   </req:ReceiverParty>
                </req:Identity>
                <req:TransactionRequest>
                   <req:Parameters>
                      <req:Parameter>
                         <com:Key>BillReferenceNumber</com:Key>
                         <com:Value>234erf</com:Value>
                      </req:Parameter>
                      <req:Amount>340</req:Amount>
                      <req:Currency>LSL</req:Currency>
                   </req:Parameters>
                </req:TransactionRequest>
             </req:Body>
          </api:Request>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
    xml_request_mapped = '''
    <soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:api='http://cps.huawei.com/cpsinterface/api_requestmgr' xmlns:com='http://cps.huawei.com/cpsinterface/common' xmlns:req='http://cps.huawei.com/cpsinterfa
ce/request'>       <soapenv:Header/>       <soapenv:Body>          <api:Request>             <req:Header>                <req:Version>1.0</req:Version>                <req:CommandID>TEST_MOCK_G2</req:CommandID>                <req:Orig
inatorConversationID>?1</req:OriginatorConversationID>                <req:Caller>                   <req:CallerType>?1</req:CallerType>                   <req:ThirdPartyID>?2</req:ThirdPartyID>                   <req:Password>=dsmoedm
owsedf</req:Password>                   <req:ResultURL>https://www.google.com</req:ResultURL>                </req:Caller>                <req:KeyOwner>1</req:KeyOwner>                <req:Timestamp>12</req:Timestamp>             </req
:Header>             <req:Body>                <req:Identity>                   <req:Initiator>                      <req:IdentifierType>1</req:IdentifierType>                      <req:Identifier>sdsfd</req:Identifier>
      <req:SecurityCredential>grfdfg</req:SecurityCredential>                   </req:Initiator>                   <req:ReceiverParty>                      <req:IdentifierType>4</req:IdentifierType>                      <req:Identifier
>dfgc</req:Identifier>                   </req:ReceiverParty>                </req:Identity>                <req:TransactionRequest>                   <req:Parameters>                      <req:Parameter>                         <com:K
ey>BillReferenceNumber</com:Key>                         <com:Value>234erf</com:Value>                      </req:Parameter>                      <req:Amount>340</req:Amount>                      <req:Currency>LSL</req:Currency>
            </req:Parameters>                </req:TransactionRequest>             </req:Body>          </api:Request>       </soapenv:Body>    </soapenv:Envelope>
    '''
    xml_response_mapped = '''
    <?xml version="1.0" ?>
    <soapenv:Envelope
      xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Body>
        <api:Response
          xmlns:api="http://cps.huawei.com/cpsinterface/api_requestmgr"
          xmlns:res="http://cps.huawei.com/cpsinterface/response">
          <res:Header>
            <res:Version>1.0</res:Version>
            <res:OriginatorConversationID>1</res:OriginatorConversationID>
            <res:ConversationID/>
          </res:Header>
          <res:Body>
            <res:ResponseCode>1</res:ResponseCode>
            <res:ResponseDesc>SUCCESSFULL RESPONSE</res:ResponseDesc>
            <res:ServiceStatus>999</res:ServiceStatus>
          </res:Body>
        </api:Response>
      </soapenv:Body>
    </soapenv:Envelope>
    '''

    xml_asynce_response_mapped = '''
    <?xml version='1.0' encoding='utf-8'?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
            <api:Result xmlns:api="http://cps.huawei.com/cpsinterface/api_resultmgr" xmlns:com="http://cps.huawei.com/cpsinterface/common" xmlns:res="http://cps.huawei.com/cpsinterface/result">
                <res:Header>
                    <res:Version>1.0</res:Version>
                    <res:OriginatorConversationID>?1</res:OriginatorConversationID>
                    <res:ConversationID>AG_20210722_00006b729dd9dbd125a7</res:ConversationID>
                </res:Header>
                <res:Body>
                    <res:ResultType>0</res:ResultType>
                    <res:ResultCode>0</res:ResultCode>
                    <res:ResultDesc>Process service request successfully.</res:ResultDesc>
                    <res:TransactionResult>
                        <res:TransactionID>?2</res:TransactionID>
                    </res:TransactionResult>
                    <res:ReferenceData>
                        <res:ReferenceItem>
                            <com:Key>Comment2Customer</com:Key>
                            <com:Value>Salary payment</com:Value>
                        </res:ReferenceItem>
                        <res:ReferenceItem>
                            <com:Key>OpenAPITransactionReference</com:Key>
                            <com:Value>290922251</com:Value>
                        </res:ReferenceItem>
                    </res:ReferenceData>
                </res:Body>
            </api:Result>
        </soapenv:Body>
    </soapenv:Envelope>
    '''
    check_match, dynamic_request, dynamic_response, dynamic_async_response = Main(xml_request, xml_request_mapped, xml_response_mapped, xml_asynce_response_mapped)
    # check_match, dynamic_request, dynamic_response, dynamic_async_response = Main(request_json, request_mapp_json, response_mapp_json)
    # print(check_match)
    # print(dynamic_request)
    # print(dynamic_response)