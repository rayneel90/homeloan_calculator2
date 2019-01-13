from django.views import View
from django.shortcuts import HttpResponse, render
from django.forms.models import model_to_dict
from .forms import MyForms
from .script import calculation


class MainView(View):

    def get(self, request):
        form = MyForms(auto_id="")
        return render(request, "Home.html", {'form':form})

    def post(self, request):
        form = MyForms(request.POST, auto_id="")
        if form.is_valid():
            indat = form.save()
            outdat = calculation(**model_to_dict(indat))
        else:
            print(form.errors, '\n'*30)
        return render(request,'Home.html', {'form':form, 'dat': outdat})
