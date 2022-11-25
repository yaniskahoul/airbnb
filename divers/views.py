from django.shortcuts import render

def home_view(request):
    context = {
        'test': "Ceci est un test"
    }
    return render(request,'divers/home_page.html', context=context)


