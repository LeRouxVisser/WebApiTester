from django import forms
import users.models as m
import json

class SpecsUpdateForm(forms.ModelForm):
    endpoint = forms.Field()
    class Meta:
        model = m.Profile
        fields = ['endpoint', 'json_spec']

    def clean_json_spec(self):
        json_spec = self.cleaned_data['json_spec']
        try:
            print(json_spec)
            json_spec_check = json.loads(json_spec.replace('\r', '').replace('\t', '').replace('\n', ''))
            for pack in json_spec_check:
                if len(pack) != 3:
                    raise forms.ValidationError(
                        'Please make sure each list inside the jason object contains 3 elements one request packet, one response packet and a response status code')
                if not self.is_int(pack[2]):
                    raise forms.ValidationError(
                        'Please specify a valid response status code')
            print(json_spec_check)
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

class DefectsUpdateForm(forms.ModelForm):
    endpoint = forms.Field(required=False, disabled="disabled")
    class Meta:
        model = m.Profile
        fields = ['endpoint', 'connection_down', 'Intermittent_connection_issues','Intermittent_connection_per']


