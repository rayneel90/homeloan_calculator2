from django import forms
from .models import Query
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Fieldset, MultiField, Div, ButtonHolder, Submit, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText


class MyForms(forms.ModelForm):
    class Meta:
        model = Query
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    PrependedText('price', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('downpay', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    AppendedText('roi','%'),
                    css_class="col-5"
                ),
                Div(
                    AppendedText('tenure','Months'),
                    css_class="col-7"
                ),
                Div(
                    PrependedText('early_repay', '&#8377'),
                    css_class="col-7"
                ),
                css_class='row'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        super(MyForms, self).__init__(*args, **kwargs)
