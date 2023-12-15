menu = [
    {'title': 'Каталог', 'url_name': 'catalog'},
    {'title': 'Авторы', 'url_name': 'authors'},
]


def menu_processor(request):
    return {'menu': menu}
