from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import LoginForm, RegisterUserForm, ProfileForm, UserForm, UserPasswordChangeForm
from .models import *
from .utils import DataMixin

sort_list = [
    {'name': 'Книгам', 'value': 'title'},
    {'name': 'Авторам', 'value': 'authors'},
    {'name': 'Жанрам', 'value': 'genre'},
    {'name': 'Языкам', 'value': 'languages'},
    {'name': 'Издательствам', 'value': 'publisher'},
]


def index(request):
    return render(request, 'book/index.html', {'title': 'Читай-город'})


class BookListView(DataMixin, ListView):
    model = Book
    context_object_name = 'books'
    title_page = 'Каталог книг'

    def get_ordering(self):
        return self.request.GET.get('orderby') or 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, sort_list=sort_list, current_orderby=self.get_ordering())


class BookDetailView(DataMixin, DetailView):
    model = Book
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f"Книга: {context['book'].title}")

    def post(self, request, *args, **kwargs):
        if request.POST.get('download'):
            book = Book.objects.get(pk=kwargs['pk'])
            book.downloads_count = book.downloads_count + 1
            book.save()
        if request.POST.get('favorite'):
            if request.POST.get('favorite') == "1":
                book = Book.objects.get(pk=kwargs['pk'])
                my_user = Profile.objects.get(user=request.user.id)
                book.favorite_users.add(my_user)
                book.save()
            elif request.POST.get('favorite') == "0":
                book = Book.objects.get(pk=kwargs['pk'])
                my_user = Profile.objects.get(user=request.user.id)
                book.favorite_users.remove(my_user)
                book.save()
        return HttpResponseRedirect(reverse('book', kwargs={'pk': book.pk}))


class AuthorListView(DataMixin, ListView):
    model = Author
    context_object_name = 'authors'
    title_page = 'Авторы'


class AuthorDetailView(DataMixin, DetailView):
    model = Author
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f"Автор: {context['author'].name}")


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'book/profile.html',
                  {'profile_form': profile_form, 'user_form': user_form, 'title': "Профиль"})


class RegisterUser(DataMixin, FormView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    title_page = 'Регистрация'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')


class UserPasswordChange(DataMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("profile")
    template_name = "book/password_change_form.html"
    title_page = "Изменение пароля"


class FavoritesView(DataMixin, ListView):
    model = Book
    context_object_name = 'books'
    title_page = "Каталог избранных книг"
    extra_context = {'favorite': True}

    def get_queryset(self):
        return Profile.objects.get(user=self.request.user).favorite_books.all()
