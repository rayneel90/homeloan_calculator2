from django.views import View
from django.shortcuts import HttpResponse, render
from django.forms.models import model_to_dict
from .forms import MyForms
from .calculator import calculation
from dateutil.relativedelta import relativedelta

class MainView(View):

    def get(self, request):
        form = MyForms(auto_id="")
        return render(request, "Home.html", {'form':form})

    def post(self, request):
        form = MyForms(request.POST, auto_id="")
        if form.is_valid():
            indat = form.save()
            print(model_to_dict(indat))
            dic ={key:val for key, val in model_to_dict(indat).items() if val is not None}
            df = calculation(**dic)
            temp = relativedelta(df.date.to_list()[-1],df.date.to_list()[0])
            years = temp.years+temp.months/12
            final = df.future_value.tolist()[-1]
            initial = dic.get('prop_price',df.pos.tolist()[0] + df.extra_repaid.tolist()[0])
            print(initial)
            cagr = round(((final/initial)**(1/years) -1)*100,2)
            df.columns = ['Date', 'POS', 'EMI', 'Int Component', 'Princi Component', 'Extra Repay', 'Maintenance', 'Prop Tax',
                          'Rent', '80C Saving', 'LOHP Saving', 'Balance Unclaimed', 'Net Outflow', 'Net (Time Adj.)', 'Future Value']
            outdat = df.to_html(classes="table", index=False)

        else:
            print(form.errors, '\n'*30)
        print(cagr)
        return render(request,'Home.html', {'form':form, 'dat': outdat,
                                            "finish": df["Date"].tolist()[-1],
                                            "netWorth": '{0:,}'.format(round(final,2)),
                                            "CAGR": cagr})
