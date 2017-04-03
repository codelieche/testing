from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class IndexView(View):
    """
    网站首页View
    """
    def get(self, request):
        return render(request, 'project/list.html')
