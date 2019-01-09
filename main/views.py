from django.views import View
from django.shortcuts import HttpResponse





class MainView(View):

    def get(self, request):
        return HttpResponse("Success")