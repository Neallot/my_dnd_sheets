from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CharacterForm, CharacterMasterEditForm
from .models import Character


class CharacterListView(LoginRequiredMixin, ListView):
    """
    Список персонажей текущего пользователя:
      - свои листы (если пользователь — игрок);
      - листы, которые ведёт пользователь (если он — мастер).
    """

    model = Character
    template_name = 'characters/character_list.html'
    context_object_name = 'characters'

    def get_queryset(self):
        user = self.request.user
        return Character.objects.filter(
            Q(owner=user) | Q(master=user)
        ).select_related('owner', 'master')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['owned'] = [c for c in ctx['characters'] if c.owner_id == user.id]
        ctx['mastered'] = [c for c in ctx['characters'] if c.master_id == user.id and c.owner_id != user.id]
        return ctx


class CharacterDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Character
    template_name = 'characters/character_detail.html'
    context_object_name = 'character'

    def test_func(self):
        return self.get_object().can_view(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет доступа к этому персонажу.')
        return redirect('character-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['can_edit'] = self.object.can_edit(self.request.user)
        ctx['can_delete'] = self.object.can_delete(self.request.user)
        return ctx


class CharacterCreateView(LoginRequiredMixin, CreateView):
    """Создать персонажа может любой авторизованный пользователь (обычно — игрок)."""

    model = Character
    form_class = CharacterForm
    template_name = 'characters/character_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Персонаж создан.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('character-detail', kwargs={'pk': self.object.pk})


class CharacterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование листа персонажа.
    Владелец видит полную форму (в т.ч. смену мастера).
    Закреплённый мастер видит форму без смены владельца/мастера.
    """

    model = Character

    def test_func(self):
        return self.get_object().can_edit(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на редактирование этого персонажа.')
        return redirect('character-list')

    def get_form_class(self):
        character = self.get_object()
        if character.owner_id == self.request.user.id:
            return CharacterForm
        return CharacterMasterEditForm

    def get_template_names(self):
        return ['characters/character_form.html']

    def form_valid(self, form):
        messages.success(self.request, 'Изменения сохранены.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('character-detail', kwargs={'pk': self.object.pk})


class CharacterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Character
    template_name = 'characters/character_confirm_delete.html'
    success_url = reverse_lazy('character-list')

    def test_func(self):
        return self.get_object().can_delete(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, 'Удалить персонажа может только его владелец.')
        return redirect('character-list')
