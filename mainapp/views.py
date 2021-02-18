from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from .mixins import CategoryDetailsMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.object.get_categories_for_left_sidebar()
        return render(request, 'base.html', {'categories': categories})


class ProductDetailView(CategoryDetailsMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'products'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailsMixin, DetailView):
    model = Category
    queryset = Category.object.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'
