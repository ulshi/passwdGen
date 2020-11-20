from django.shortcuts import render


def runoob(request):
    context = {}
    context['hello'] = 'Hello Python World!'
    if request.method == 'GET':
        cook = request.COOKIES
    elif request.method == 'POST':
        pass
    return render(request, 'runoob.html', context)