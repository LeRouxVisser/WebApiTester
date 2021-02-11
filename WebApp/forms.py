from django import forms
import users.models as m
import json
import xml.dom.minidom as xdm

class SpecsUpdateForm(forms.ModelForm):
    endpoint = forms.Field()
    class Meta:
        model = m.Profile
        fields = ['endpoint', 'async_func', 'async_result_url', 'async_result_time_delay', 'json_spec']
        labels = {
            'async_func': 'Async',
            'async_result_time_delay': '',
            'async_result_url': ''
        }

    def clean_json_spec(self):
        async_func = self.cleaned_data['async_func']
        json_spec = self.cleaned_data['json_spec']
        print(async_func)
        try:
            # print(json_spec)
            json_spec_check = json.loads(json_spec.replace('\r', '').replace('\t', '').replace('\n', ''))

            for pack in json_spec_check:
                if (async_func):
                     self.validator(pack, 4)
                else:
                    self.validator(pack, 3)
            # print(json_spec_check)
        except json.decoder.JSONDecodeError:
            raise forms.ValidationError('''Please enter a valid jason object list using " as quotations for keys and values and ' inside request and respond packets where quotes are needed''')
        return json_spec

    def is_int(self, s):
        check = False
        try:
            int(s)
            check = True
            return check
        except ValueError:
            return check

    def validator(self, pack, length):
        if len(pack) != length:
            raise forms.ValidationError(f'''Please make sure each list inside the jason object contains {length} elements.''')
        if not self.is_int(pack[2]):
            raise forms.ValidationError('Please specify a valid response status code')

class DefectsUpdateForm(forms.ModelForm):
    endpoint = forms.Field(required=False, disabled="disabled")
    class Meta:
        model = m.Profile
        fields = ['endpoint', 'connection_down', 'Intermittent_connection_issues', 'Intermittent_connection_per']


class TestApi(forms.Form):
    api_type_choices = [('XML', 'XML'), ('JSON', 'JSON')]
    api_request_type_choices = [('POST', 'POST'), ('PUT', 'PUT')]
    api_url = forms.URLField(label='Url')
    api_header = forms.JSONField(label='Header')
    api_request_type = forms.ChoiceField(choices=api_type_choices, label='Request type')
    api_type = forms.ChoiceField(choices=api_request_type_choices, label='Content type')
    api_body = forms.CharField(widget=forms.Textarea, label='Body')

    def clean_api_body(self):
        api_request_type = self.cleaned_data['api_request_type']
        api_body = self.cleaned_data['api_body']
        if api_request_type == "JSON":
            try:
                json.loads(api_body)
            except json.decoder.JSONDecodeError:
                raise forms.ValidationError(
                    '''Please enter a valid jason object list using " as quotations for keys and values and ' inside request and respond packets where quotes are needed''')
        else:
            try:
                xdm.parseString(api_body)
            except xdm.xml.parsers.expat.ExpatError:
                raise forms.ValidationError(
                    '''Please enter a valid xml packet''')