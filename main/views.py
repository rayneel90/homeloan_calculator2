from django.views import View
from django.shortcuts import HttpResponse, render
from django.forms.models import model_to_dict
from .forms import MyForms
from .calculator import calculation


class MainView(View):

    def get(self, request):
        form = MyForms(auto_id="")
        return render(request, "Home.html", {'form':form})

    def post(self, request):
        form = MyForms(request.POST, auto_id="")
        if form.is_valid():
            indat = form.save()
            print(model_to_dict(indat))
            dic ={key:val for key, val in model_to_dict(indat).items() if val}
            df = calculation(**dic)
            df.columns = ['Date', 'POS', 'EMI', 'Int Component', 'Princi Component', 'Extra Repay', 'Maintenance', 'Prop Tax',
                          'Rent', '80C Saving', 'LOHP Saving', 'Balance Unclaimed', 'Net Outflow', 'Net (Time Adj.)', 'Future Value']
            outdat = df.to_html(classes="table", index=False)

        else:
            print(form.errors, '\n'*30)
        return render(request,'Home.html', {'form':form, 'dat': outdat,
                                            "finish": df["Date"].tolist()[-1],
                                            "netWorth": df['Future Value'].tolist()[-1]})
