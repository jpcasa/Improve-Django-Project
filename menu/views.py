from operator import attrgetter
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from . import models
from . import forms


def menu_list(request):
    menus = models.Menu.objects.prefetch_related(
        'items'
    ).filter(
        expiration_date__gte=datetime.now()
    )
    return render(request, 'menu/list_all_current_menus.html', {
        'menus': menus
    })


def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {
        'menu': menu
    })


def item_detail(request, pk):
    try:
        item = models.Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'menu/detail_item.html', {
        'item': item
    })


def create_new_menu(request):
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    else:
        form =forms.MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    form = forms.MenuForm(instance=menu)

    if request.method == "POST":
        form = forms.MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            msg = "Updated {}!".format(form.cleaned_data['season'])
            messages.success(request, msg)
            return redirect('menu:menu_detail', pk=menu.pk)

    return render(request, 'menu/menu_edit.html', {'form': form})
