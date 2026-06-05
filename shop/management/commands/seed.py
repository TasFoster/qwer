from django.core.management.base import BaseCommand

from shop.models import Category, Product


CATEGORIES = [
    ('Шаурма', 'shaurma', 1),
    ('Шашлык', 'shashlyk', 2),
    ('Напитки', 'napitki', 3),
    ('Соусы', 'sousy', 4),
]

PRODUCTS = [
    # (category_slug, name, slug, weight, price, desc, hit, spicy)
    ('shaurma', 'Шаурма классическая', 'shaurma-klassicheskaya', '350 г', 320,
     'Сочная курица на углях, свежие овощи, фирменный чесночный соус в тонком лаваше.', True, False),
    ('shaurma', 'Шаурма по-кавказски', 'shaurma-po-kavkazski', '400 г', 390,
     'Маринованная баранина, лук с зеленью, аджика и кисломолочный соус — рецепт Элтаджа.', True, True),
    ('shaurma', 'Шаурма с говядиной', 'shaurma-s-govyadinoy', '380 г', 410,
     'Нежная говядина с углей, томаты, маринованный огурец, соус барбекю.', False, False),
    ('shaurma', 'Шаурма острая «Огонь»', 'shaurma-ognennaya', '360 г', 360,
     'Для любителей погорячее: двойная аджика, перец халапеньо и острый соус.', False, True),
    ('shaurma', 'Вегетарианская шаурма', 'shaurma-veg', '330 г', 290,
     'Гриль-овощи, фалафель, хумус и свежая зелень в тёплом лаваше.', False, False),

    ('shashlyk', 'Шашлык из баранины', 'shashlyk-baranina', '250 г', 590,
     'Молодая баранина, маринованная 12 часов, на живых углях. Подаётся с луком и лавашом.', True, False),
    ('shashlyk', 'Шашлык из курицы', 'shashlyk-kuritsa', '250 г', 390,
     'Куриное бедро в ароматном маринаде, прожаренное до золотистой корочки.', False, False),
    ('shashlyk', 'Шашлык из свинины', 'shashlyk-svinina', '250 г', 450,
     'Сочная свиная шейка на углях с дымком. Классика, которую любят все.', True, False),
    ('shashlyk', 'Люля-кебаб', 'lyulya-kebab', '220 г', 420,
     'Рубленая баранина со специями и зеленью на шампуре. Подаётся с соусом наршараб.', False, True),
    ('shashlyk', 'Овощи на мангале', 'ovoshchi-mangal', '300 г', 280,
     'Запечённые на углях баклажан, перец, томаты и лук. Идеальный гарнир.', False, False),

    ('napitki', 'Айран', 'ayran', '0,5 л', 120,
     'Освежающий кисломолочный напиток — лучший друг шашлыка.', False, False),
    ('napitki', 'Лимонад тархун', 'limonad-tarhun', '0,5 л', 150,
     'Домашний лимонад на травах, в меру сладкий и очень освежающий.', False, False),
    ('napitki', 'Чай чёрный', 'chay-chyornyy', '0,4 л', 100,
     'Крепкий горячий чай с чабрецом по-кавказски.', False, False),

    ('sousy', 'Соус чесночный', 'sous-chesnochnyy', '50 г', 50,
     'Нежный сливочно-чесночный соус собственного приготовления.', False, False),
    ('sousy', 'Аджика острая', 'adzhika-ostraya', '50 г', 50,
     'Огненная аджика для тех, кто любит погорячее.', False, True),
    ('sousy', 'Соус наршараб', 'sous-narsharab', '50 г', 60,
     'Гранатовый соус — классическое дополнение к шашлыку.', False, False),
]


class Command(BaseCommand):
    help = 'Заполняет каталог демонстрационными блюдами'

    def handle(self, *args, **options):
        cats = {}
        for name, slug, order in CATEGORIES:
            cat, _ = Category.objects.update_or_create(
                slug=slug, defaults={'name': name, 'order': order})
            cats[slug] = cat

        created = 0
        for cslug, name, slug, weight, price, desc, hit, spicy in PRODUCTS:
            _, was_created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'category': cats[cslug],
                    'name': name,
                    'description': desc,
                    'weight': weight,
                    'price': price,
                    'is_hit': hit,
                    'is_spicy': spicy,
                    'available': True,
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: {len(cats)} категорий, {len(PRODUCTS)} блюд '
            f'({created} новых).'))
