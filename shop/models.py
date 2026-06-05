from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('Slug', max_length=150, unique=True)
    description = models.TextField('Описание', blank=True)
    weight = models.CharField('Вес / объём', max_length=50, blank=True)
    price = models.DecimalField('Цена, ₽', max_digits=8, decimal_places=2)
    image = models.ImageField('Фото', upload_to='products/', blank=True)
    is_hit = models.BooleanField('Хит продаж', default=False)
    is_spicy = models.BooleanField('Острое', default=False)
    available = models.BooleanField('В наличии', default=True)
    created = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Меню'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличными при получении'),
        ('card', 'Картой при получении'),
    ]
    DELIVERY_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    ]

    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=30)
    address = models.CharField('Адрес доставки', max_length=255, blank=True)
    delivery = models.CharField('Способ получения', max_length=20,
                                choices=DELIVERY_CHOICES, default='delivery')
    payment = models.CharField('Оплата', max_length=20,
                               choices=PAYMENT_CHOICES, default='cash')
    comment = models.TextField('Комментарий', blank=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    paid = models.BooleanField('Оплачен', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return f'Заказ №{self.id} — {self.name}'

    def get_total(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.PROTECT)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f'{self.product} × {self.quantity}'

    def get_cost(self):
        return self.price * self.quantity
