from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class LatestProductsManager:
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)

        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Катекория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название продукта')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изоброжение', blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class Notebook(Product):
    diagonal = models.CharField(max_length=5, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freg = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Память')
    video = models.CharField(max_length=255, verbose_name='Видео память')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')

    def __str__(self):
        return "{} - {}".format(self.title, self.slug)


class Smartphone(Product):
    diagonal = models.CharField(max_length=5, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    ram = models.CharField(max_length=255, verbose_name='Память')
    sd = models.BooleanField(default=True)
    sd_vol_max = models.CharField(max_length=255, verbose_name='Макс.обьем встроенной памяти')
    accum_volue = models.CharField(max_length=255, verbose_name='Обьем батареи')
    main_cam_up = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_up = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} - {}".format(self.title, self.slug)


class CartProduct(models.Model):
    user = models.ForeignKey("Customer", verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qtr = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='cart_product')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    phone = models.IntegerField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адресс')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

# class Reviews(models.Model):
#     email = models.EmailField()
#     name = models.CharField(max_length=30, verbose_name='Имя')
#     text = models.CharField(max_length=1500, verbose_name='Отзыв')
#     parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
#     product = models.ForeignKey(Product, verbose_name='Название продукта', on_delete=models.CASCADE,
#                                 related_name='reviews_product')
#
#     def __str__(self):
#         return "Отзывы о {} ".format(self.product)
