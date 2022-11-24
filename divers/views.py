from django.shortcuts import render

def home_page (request):
    return render(request,'divers/home_page.html')
