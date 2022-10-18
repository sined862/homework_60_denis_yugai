from django.db import models
from django.db.models import TextChoices


class CategoryChoices(TextChoices):
    OTHER = 'other', 'Разное'
    NOUTBOOK = 'noutbook', 'Ноутбуки'
    SMARTPHONE = 'smartphone', 'Смартфоны'
    TV = 'tv', 'Телевизоры'
    MONITOR = 'monitor', 'Мониторы'


class Product(models.Model):
    title = models.CharField(
        verbose_name = 'Наименование товара',
        max_length = 100,
        null = False,
        blank = False
    )
    description = models.TextField(
        verbose_name = 'Оисание товара',
        max_length = 2000,
        null = False,
        blank = False,
        default = ''
    )
    photo = models.CharField(
        verbose_name = 'Фото товара',
        max_length = 100,
        null = False,
        blank = False,
        default = ''
    )
    category = models.CharField(
        verbose_name = 'Категория',
        max_length = 20,
        choices = CategoryChoices.choices,
        null = False,
        blank = False,
        default = CategoryChoices.OTHER
    )
    balance = models.IntegerField(
        verbose_name = 'Остаток',
        null = False,
        blank = False,
        default = 0
    )
    price = models.DecimalField(
        verbose_name = 'Стоимость',
        decimal_places = 2,
        max_digits = 9,
        null = False,
        blank = False,
        default = 0
    )

    

    def __str__(self):
        return self.title


class ProductInCart(models.Model):
    product = models.ForeignKey(
        to='shop.Product',
        related_name='products_in',
        verbose_name='Продукт в корзине',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
        blank=False,
        null=False
    )

    def __str__(self):
        return str(self.quantity)
