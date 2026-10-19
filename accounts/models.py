from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Пользователь системы. Может быть игроком или мастером (ведущим игры).
    Роль определяет права:
      - игрок может создавать и редактировать только свои листы персонажей;
      - мастер дополнительно может редактировать листы персонажей,
        которые игроки закрепили именно за ним.
    """

    class Role(models.TextChoices):
        PLAYER = 'player', 'Игрок'
        MASTER = 'master', 'Мастер'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PLAYER,
        verbose_name='Роль',
    )

    @property
    def is_master(self) -> bool:
        return self.role == self.Role.MASTER

    @property
    def is_player(self) -> bool:
        return self.role == self.Role.PLAYER

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
