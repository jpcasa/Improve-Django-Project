import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User

from . import models
from . import forms

def add_time(num_years):
    weeks = num_years * 52
    return timezone.now() + timezone.timedelta(weeks=weeks)

menu1 = {
    'season': 'Halloween',
    'expiration_date': add_time(2),
}

menu2 = {
    'season': 'Christmas',
    'expiration_date': add_time(4),
}


class MenuViewsTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user',
            email='testemail@gmail.com',
            password='testing'
        )
        self.menu1 = models.Menu.objects.create(**menu1)
        self.menu2 = models.Menu.objects.create(**menu2)
        self.item = models.Item(
            name='Item',
            description='Description Item Testing',
            chef=self.test_user
        )
        self.item.save()
        self.ing1 = models.Ingredient(name='pistachio')
        self.ing2 = models.Ingredient(name='nutella')
        self.ing3 = models.Ingredient(name='raspberry')


    def test_delete_user(self):
        self.test_user.delete()


    def test_menu_name(self):
        self.assertEqual(str(self.menu1), self.menu1.season)


    def test_item_name(self):
        self.assertEqual(str(self.item), self.item.name)


    def test_ingredient_name(self):
        self.assertEqual(str(self.ing1), self.ing1.name)


    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context['menus'])
        self.assertIn(self.menu2, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu1.season)


    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu:menu_detail',
            kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, self.menu1.season)


    def test_item_detail_view(self):
        resp = self.client.get(reverse('menu:item_detail',
            kwargs={'pk': self.item.pk}))
        resp2 = self.client.get(reverse('menu:item_detail',
            kwargs={'pk': 1985656}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.status_code, 404)
        self.assertEqual(self.item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertContains(resp, self.item.name)


    def test_create_new_menu_view_get(self):
        resp = self.client.get(reverse('menu:menu_new'))
        self.assertEqual(resp.status_code, 200)


    def test_create_new_menu_view_post(self):
        resp = self.client.post(reverse('menu:menu_new'))
        self.assertEqual(resp.status_code, 200)


    def test_create_edit_menu_view_get(self):
        resp = self.client.get(reverse('menu:menu_edit',
            kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)


    def test_create_edit_menu_view_post(self):
        resp = self.client.post(reverse('menu:menu_edit',
            kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)


class MenuFormTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user2',
            email='testemail2@gmail.com',
            password='testing'
        )
        self.item = models.Item(
            name='Item',
            description='Description Item Testing',
            chef=self.test_user
        )
        self.item.save()

    def test_menu_create(self):
        form_data = {
            'season': 'Christmas',
            'items': [self.item],
            'expiration_date': '12/12/2023'
        }
        form = forms.MenuForm(data=form_data)
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Christmas')
