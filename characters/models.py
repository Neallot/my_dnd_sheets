from django.conf import settings
from django.db import models


class Character(models.Model):
    """Лист персонажа настольной ролевой игры (D&D-подобной)."""

    # Владелец листа — игрок, который его создал. Только он может удалить лист
    # и передать/сменить мастера.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='characters',
        on_delete=models.CASCADE,
        verbose_name='Владелец (игрок)',
    )

    # Мастер, за которым закреплён персонаж. Только пользователь с ролью
    # "мастер" может быть выбран, и только он получает право редактировать
    # этот лист (наравне с владельцем).
    master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='mastered_characters',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'master'},
        verbose_name='Мастер',
    )

    name = models.CharField('Имя персонажа', max_length=150)
    race = models.CharField('Раса', max_length=100, blank=True)
    char_class = models.CharField('Класс', max_length=100, blank=True)
    level = models.PositiveSmallIntegerField('Уровень', default=1)
    background = models.CharField('Предыстория', max_length=200, blank=True)
    alignment = models.CharField('Мировоззрение', max_length=100, blank=True)

    # Характеристики
    strength = models.PositiveSmallIntegerField('Сила', default=10)
    dexterity = models.PositiveSmallIntegerField('Ловкость', default=10)
    constitution = models.PositiveSmallIntegerField('Телосложение', default=10)
    intelligence = models.PositiveSmallIntegerField('Интеллект', default=10)
    wisdom = models.PositiveSmallIntegerField('Мудрость', default=10)
    charisma = models.PositiveSmallIntegerField('Харизма', default=10)

    max_hp = models.PositiveSmallIntegerField('Максимум ХП', default=10)
    current_hp = models.PositiveSmallIntegerField('Текущие ХП', default=10)
    armor_class = models.PositiveSmallIntegerField('Класс брони (AC)', default=10)

    inventory = models.TextField('Инвентарь', blank=True)
    notes = models.TextField('Заметки', blank=True)

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True)

    class Meta:
        verbose_name = 'Лист персонажа'
        verbose_name_plural = 'Листы персонажей'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.name} (ур. {self.level})'

    def can_view(self, user) -> bool:
        if not user.is_authenticated:
            return False
        return user_id_matches(user, self.owner_id) or user_id_matches(user, self.master_id)

    def can_edit(self, user) -> bool:
        """
        Редактировать лист может:
          - владелец (игрок, создавший персонажа);
          - мастер, за которым этот персонаж закреплён (только если он
            действительно назначен на данный лист).
        """
        if not user.is_authenticated:
            return False
        if user_id_matches(user, self.owner_id):
            return True
        if self.master_id is not None and user_id_matches(user, self.master_id) and getattr(user, 'is_master', False):
            return True
        return False

    def can_delete(self, user) -> bool:
        # Удалять лист может только его владелец.
        return user.is_authenticated and user_id_matches(user, self.owner_id)


def user_id_matches(user, other_id) -> bool:
    return other_id is not None and user.id == other_id
