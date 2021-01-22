from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from .models import *
from PIL import Image
from django.utils.safestring import mark_safe


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red;">Загружайте изоброжения с расширением {}x{}</span>'.format(
                *Product.MIN_RESOLUTION))

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError(
                mark_safe('<span style="color:red;">Обьем изоброжения больше допустимого</span>'))
        if img.width < min_width or img.height < min_height:
            raise ValidationError(
                mark_safe('<span style="color:red;">Разрешение изоброжение меньше минимального</span>'))
        if img.width > max_width or img.height > max_height:
            raise ValidationError(
                mark_safe('<span style="color:red;">Разрешение изоброжение больше максимального</span>'))
        return image


class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
