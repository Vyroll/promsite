from django.shortcuts import render
from django.views import View

class IndexView(View):
    template_name = 'promo/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)