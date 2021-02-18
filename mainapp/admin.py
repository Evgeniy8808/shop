from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from .models import *
from PIL import Image
from django.utils.safestring import mark_safe

from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)


class EntityAdmin(admin.ModelAdmin):
    list_filter = (
        ('a_charfield', DropdownFilter),
        ('a_choicefield', ChoiceDropdownFilter),
        ('a_foreignkey_field', RelatedDropdownFilter),
    )


class SmartphoneAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_vol_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray;'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_vol_max'] = None
        return self.cleaned_data


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red;">Загружайте изоброжения с расширением {}x{}</span>'.format(
                *Product.MIN_RESOLUTION))

    # -----------------------Вставляем изоброжение с ограничением-----------------
    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError(
                mark_safe('<span style="color:red;">Обьем изоброжения больше 6мб</span>'))
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
            return ModelChoiceField(Category.objects.filter(slug='notebook'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
