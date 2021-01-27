from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, View


def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'products'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
