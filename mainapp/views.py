from django.shortcuts import render, redirect
from .models import Product
from django.views.generic import ListView, DetailView,View

# class mainappView(View):
#     def __get__(self, instance, owner):

def test_view(request):
    return render(request, 'base.html', {})