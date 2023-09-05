from django.shortcuts import render

def custom_view(request):
    return render(request, 'master_data.html', {})
