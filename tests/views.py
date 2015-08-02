from django.shortcuts import render


def test(request):
    return render(request, 'tests/test.html')


def test_javascript(request):
    return render(request, 'tests/test_javascript.html')


def test_prototype(request):
    return render(request, 'tests/test_prototype.html')
