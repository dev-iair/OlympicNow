from django.shortcuts import render
import cx_Oracle as oci


def index(request):
    return render(request, 'olympicNow/index.html', {})
