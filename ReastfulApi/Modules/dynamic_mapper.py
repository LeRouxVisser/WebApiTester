from bs4 import BeautifulSoup
import ReastfulApi.modules.function_check as fc
def main(request,request_mapped=None,response_mapp=None,async_response_mapp=None):
    request_type_check = fc.CheckType(request)
    if request_type_check == 'xml':
        check_match, dynamic_request, dynamic_response, dynamic_async_response = dynamic_xml(request, request_mapped, response_mapp, async_response_mapp)
        # print(check_match)
        # print(request)
        # print(dynamic_request.prettify())
        # print(dynamic_response.prettify())
        # print(dynamic_async_response)
    elif request_type_check == 'json':
        check_match, dynamic_request, dynamic_response, dynamic_async_response = dynamic_json(request, request_mapped, response_mapp, async_response_mapp)
        # print(check_match)
        # print(request)
        # print(dynamic_request)
        # print(dynamic_response)
        # print(dynamic_async_response)
    else:
        check_match = (request == request_mapped)
        dynamic_request = request_mapped
        dynamic_response = response_mapp
        dynamic_async_response = async_response_mapp
    return check_match, dynamic_request, dynamic_response, dynamic_async_response


def dynamic_xml(xml_request, xml_request_mapped, xml_response_mapped, xml_async_response_mapp):
    soup_request = BeautifulSoup(xml_request, "xml")
    soup_request_mapped = BeautifulSoup(xml_request_mapped, "xml")
    response_check = False
    check_match = False
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
    # print(response_check)

    srm_tag_value = [tag.text for tag in soup_request_mapped.findAll()]
    srm_tag_name = [tag.name for tag in soup_request_mapped.findAll()]
    # print(srm_tag_name)
    for i in range(len(srm_tag_value)):
        if ('\n' not in srm_tag_value[i]) and ('?' == srm_tag_value[i]):
            try:
                value_check = soup_request.find(srm_tag_name[i]).text
                name_check = srm_tag_name[i]
                # print(name_check)
                soup_request_mapped.find(name=name_check).string = value_check
                check_match = (soup_request_mapped == soup_request)
                # print(check_match)
                if (check_match):
                    soup_response_mapped.find(name=name_check).string = value_check
                    # print(soup_response_mapped)
                    soup_async_response_mapp.find(name=name_check).string = value_check

            except AttributeError:
                print('Tag not in request/response')
    return check_match, soup_request_mapped, str(soup_response_mapped), str(soup_async_response_mapp)

def dynamic_json(json_request, json_request_mapp, json_response_mapp, json_async_response_mapp):
    dynamic_keys = [k for k, v in json_request_mapp.items() if '?' == v]
    response_check = False
    check_match = False
    try:
        response_keys = list(json_response_mapp.keys())
        response_check = True
        async_response_keys = list(json_async_response_mapp.keys())
    except AttributeError:
        if (response_check):
            async_response_keys = []
        else:
            response_keys = []
            async_response_keys = []
    for i in range(len(dynamic_keys)):
        request_key = dynamic_keys[i]
        try:
            request_value = json_request[dynamic_keys[i]]
            json_request_mapp[request_key] = request_value
            check_match = (json_request_mapp == json_request)
            if(check_match):
                try:
                    sub_key_str = dynamic_keys[i][dynamic_keys[i].index('_') + 1:]
                except ValueError:
                    sub_key_str = dynamic_keys[i]
                mapp_response_key = [key for key in response_keys if
                                     sub_key_str in key]
                mapp_async_response_key = [key for key in async_response_keys if
                                           sub_key_str in key]
                if mapp_response_key != []:
                    json_response_mapp[mapp_response_key[0]] = json_request[request_key]
                    if mapp_async_response_key != []:
                        json_async_response_mapp[mapp_async_response_key[0]] = json_request[request_key]
        except KeyError:
            print('Key not in request/response')
    return check_match, json_request_mapp, json_response_mapp, json_async_response_mapp

if __name__ == '__main__':
    request_json = {"test": "What"}
    request_mapp_json = {"test": "?"}
    response_mapp_json = {"response": "Success"}

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
                <req:OriginatorConversationID>125638</req:OriginatorConversationID>
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
                      <req:SecurityCredential>?grfdfg</req:SecurityCredential>
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
                <req:OriginatorConversationID>?</req:OriginatorConversationID>
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
                      <req:SecurityCredential>?grfdfg</req:SecurityCredential>
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
            <res:OriginatorConversationID/>
            <res:ConversationID/>
          </res:Header>
          <res:Body>
            <res:ResponseCode>SUCCESS</res:ResponseCode>
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
                    <res:OriginatorConversationID></res:OriginatorConversationID>
                    <res:ConversationID>AG_20210722_00006b729dd9dbd125a7</res:ConversationID>
                </res:Header>
                <res:Body>
                    <res:ResultType>0</res:ResultType>
                    <res:ResultCode>0</res:ResultCode>
                    <res:ResultDesc>Process service request successfully.</res:ResultDesc>
                    <res:TransactionResult>
                        <res:TransactionID>8GM601KBFY</res:TransactionID>
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
    # check_match, dynamic_request, dynamic_response, dynamic_async_response = main(xml_request, xml_request_mapped, xml_response_mapped, xml_asynce_response_mapped)
    check_match, dynamic_request, dynamic_response, dynamic_async_response = main(request_json, request_mapp_json, response_mapp_json)
    print(check_match)