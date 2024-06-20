from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q


from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from menenger.forms import ContentForm, PublishedContentForm, SearchForm
from menenger.models import Content, Like
from menenger.services import create_stripe_price, create_stripe_subcriptions, create_stripe_session
from users.models import User, Subscription


class ContentCreateView(CreateView):
    """
    если пользователь не купил подписку на платформу
    то создание поста отправляется в не опуликованые
    """
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('menenger:home')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            if self.request.user.is_authenticated and self.request.user.is_subscribed:
                new_mat.author = self.request.user
                new_mat.published = True
                new_mat.save()
            else:
                new_mat.save()

        return super().form_valid(form)


class HomeView(ListView):
    """
    Вывод опубликовыех постов
    """
    model = Content
    template_name = 'menenger/home.html'

    paginate_by = 5

    def get_queryset(self, queryset=None):
        # Filter the queryset to include only published posts
        queryset = super().get_queryset().filter(published=True)

        # Annotate the queryset with the count of likes for each content
        queryset = queryset.annotate(like_count=Count('like'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class NoPublishView(ListView):
    """
    Вывод не опубликованных постов

    """
    model = Content
    template_name = 'menenger/home.html'
    paginate_by = 5

    def get_queryset(self, queryset=None):
        # Filter the queryset to include only published posts
        queryset = super().get_queryset().filter(published=False)

        # Annotate the queryset with the count of likes for each content
        queryset = queryset.annotate(like_count=Count('like'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class ContentDetailView(DetailView):
    """
    Вывод детальной информации о посте
    """
    model = Content

    def get_object(self, queryset=None):
        """
        Ввывод счетчика просмотров для поста
        """
        self.object = super().get_object(queryset)

        self.object.count_views += 1
        self.object.save()
        return self.object


class ContentUpdateView(UpdateView):
    """
    Вывод редактирования поста
    """
    model = Content
    form_class = ContentForm

    def get_success_url(self):
        return reverse_lazy('menenger:detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        """Получение формы для редактирования поста"""
        if self.request.user.is_superuser:
            return ContentForm
        elif self.request.user.is_staff:
            return PublishedContentForm

        elif self.request.user == self.get_object().author and self.request.user.is_subscribed:
            return ContentForm

        else:
            raise PermissionDenied


class ContentDeleteView(DeleteView):
    """
    Удаление поста из базы данных
    """
    model = Content
    success_url = reverse_lazy('menenger:home')

    def get_object(self, queryset=None):  # Получение объекта контента
        self.object = super().get_object(queryset)
        if (not self.request.user.is_authenticated or not self.request.user == self.object.author and
                self.request.user.is_subscribed):
            raise PermissionDenied("Вы не являетесь автором этого объекта.")
        return self.object


def payment_stripe(request):
    """
    Функция для создания подписки на сайт
    """
    if request.user.is_authenticated:
        if not request.user.is_subscribed:

            sub = Subscription.objects.create()
            user = User.objects.get(pk=request.user.pk)
            product_id = create_stripe_subcriptions(sub)
            price = create_stripe_price(product_id)
            session_id, payment_link = create_stripe_session(price)
            sub.payment_session = session_id
            sub.payment_url = payment_link
            sub.save()
            user.is_subscribed = sub
            user.save()
            return HttpResponsePermanentRedirect(sub.payment_url)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def like_view(request, pk, page):
    """
    Функция для лайка контента
    """
    if request.user.is_authenticated and request.user.is_subscribed:
        # Получаем объект контента на основе pk
        content = Content.objects.get(pk=pk)

        # Проверяем, поставил ли пользователь уже лайк контенту
        liked = Like.objects.filter(user=request.user, content=content).exists()

        if liked:
            # Если пользователь уже поставил лайк контенту, удаляем лайк
            Like.objects.filter(user=request.user, content=content).delete()
            # Удаляем состояние лайка из сессии для пользователя

        else:
            # Если пользователь еще не поставил лайк контенту, создаем новый лайк
            Like.objects.create(user=request.user, content=content, like=True)
            # Сохраняем состояние лайка в сессии для пользователя

        return redirect(reverse('menenger:home') + f'?page={page}')


def search_view(request):
    """
    Функция для поиска контента по запросу
    """
    if request.method == 'GET':
        search_field = SearchForm()
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data['search']
            content = Content.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
            context = {'content': content, 'search': search, 'search_field': search_field}

            return render(request, 'menenger/search.html', context)
