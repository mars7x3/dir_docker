from decimal import Decimal
from django.conf import settings
from dir.models import Resume


class Cart:

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, resume, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        resume_id = str(resume.id)
        self.cart[resume_id] = {
            'id': resume_id,
            'image': resume.image.url,
            'title': resume.title,
            'create_time': resume.create_time.strftime("%m/%d/%Y, %H:%M:%S")
            }
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, resume):
        """
        Удаление товара из корзины.
        """
        resume_id = str(resume.id)
        if resume_id in self.cart:
            del self.cart[resume_id]
            self.save()
    
    def __iter__(self):
        """
        Перебор элементов в корзине и получение resumes из базы данных.
        """
        resume_ids = self.cart.keys()
        # получение объектов Resume и добавление их в корзину
        resumes = Resume.objects.filter(id__in=resume_ids)
        for resume in resumes:
            self.cart[str(resume.id)]['resume'] = resume

        for item in self.cart.values():
            # item['price'] = Decimal(item['price'])
            yield item

    def clear(self):
        """
        удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
