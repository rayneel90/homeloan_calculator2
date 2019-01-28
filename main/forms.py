from django import forms
from .models import Query
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Fieldset, MultiField, Div, ButtonHolder, Submit, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText


class MyForms(forms.ModelForm):
    class Meta:
        model = Query
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class':'datepicker'}),
        }
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    PrependedText('prop_price', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('other_cost', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    AppendedText('ltv', '%'),
                    css_class="col-4"
                ),
                Div(
                    AppendedText('roi','%'),
                    css_class="col-4"
                ),
                Div(
                    AppendedText('tenure','Months'),
                    css_class="col-4"
                ),
                Div(
                    PrependedText('annual_early_repay', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    'date_of_purchase',
                    css_class="col-6"
                ),
                Div(
                    PrependedText('months_to_possession', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('monthly_rent_earning', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('annual_maintenance', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('annual_prop_tax', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('limit_80c', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('self_pf_contri', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('int_rebate_limit', '&#8377'),
                    css_class="col-6"
                ),
                Div(
                    PrependedText('rd_rate', '&#8377'),
                    css_class="col-6"
                ),
                css_class='row'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        super(MyForms, self).__init__(*args, **kwargs)
