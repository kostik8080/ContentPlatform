from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView

from menenger.forms import ContentForm, PublishedContentForm
from menenger.models import Content, Like
from menenger.services import create_stripe_price, create_stripe_subcriptions, create_stripe_session
from users.models import User, Subscription


class ContentCreateView(CreateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('menenger:home')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            if self.request.user.is_authenticated:
                new_mat.author = self.request.user
                new_mat.published = True
                new_mat.save()
            else:
                new_mat.save()

        return super().form_valid(form)


class HomeView(ListView):
    model = Content
    template_name = 'menenger/home.html'
    paginate_by = 3

    def get_queryset(self, queryset=None):
        # Filter the queryset to include only published posts
        queryset = super().get_queryset().filter(published=True)

        # Annotate the queryset with the count of likes for each content
        queryset = queryset.annotate(like_count=Count('like'))

        return queryset


class NoPublishView(ListView):
    model = Content
    template_name = 'menenger/home.html'

    def get_queryset(self, queryset=None):
        # Filter the queryset to include only published posts
        queryset = super().get_queryset().filter(published=False)

        # Annotate the queryset with the count of likes for each content
        queryset = queryset.annotate(like_count=Count('like'))

        return queryset


class ContentDetailView(DetailView):
    model = Content

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        self.object.count_views += 1
        self.object.save()
        return self.object


class ContentUpdateView(UpdateView):
    model = Content
    form_class = ContentForm

    def get_success_url(self):
        return reverse_lazy('menenger:detail', kwargs={'pk': self.object.pk})


    def get_form_class(self):
        """Получение формы для редактирования продукта"""
        if self.request.user.is_superuser:
            return ContentForm
        elif self.request.user.is_staff:
            return PublishedContentForm

        elif self.request.user == self.get_object().author:
            return ContentForm

        else:
            raise PermissionDenied

class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy('menenger:home')


def payment_stripe(request):
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


def like_view(request, pk):
    if request.user.is_authenticated:
        # Получаем объект контента на основе pk
        content = Content.objects.get(pk=pk)

        # Проверяем, поставил ли пользователь уже лайк контенту
        liked = Like.objects.filter(user=request.user, content=content).exists()

        if liked:
            # Если пользователь уже поставил лайк контенту, удаляем лайк
            Like.objects.filter(user=request.user, content=content).delete()
            # Удаляем состояние лайка из сессии для пользователя
            del request.session['isLiked_' + str(request.user.pk)]
        else:
            # Если пользователь еще не поставил лайк контенту, создаем новый лайк
            Like.objects.create(user=request.user, content=content, like=True)
            # Сохраняем состояние лайка в сессии для пользователя
            request.session['isLiked_' + str(request.user.pk)] = 'true'

        # Пересчитываем количество лайков
        like_count = Like.objects.filter(content=content).count()

        return redirect(reverse('menenger:home'))
