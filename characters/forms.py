from django import forms

from accounts.models import User
from .models import Character

CHARACTER_FIELDS = [
    'name', 'race', 'char_class', 'level', 'background', 'alignment',
    'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma',
    'max_hp', 'current_hp', 'armor_class',
    'inventory', 'notes',
]


class CharacterForm(forms.ModelForm):
    """
    Полная форма листа персонажа — доступна владельцу (игроку).
    Позволяет в том числе назначить/сменить мастера, закреплённого за листом.
    """

    master = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.Role.MASTER),
        required=False,
        label='Мастер',
        help_text='Мастер, закреплённый за этим листом, сможет его редактировать.',
    )

    class Meta:
        model = Character
        fields = CHARACTER_FIELDS + ['master']


class CharacterMasterEditForm(forms.ModelForm):
    """
    Урезанная форма для мастера: мастер может править сам лист персонажа,
    но не может переназначить владельца или снять с себя закрепление.
    """

    class Meta:
        model = Character
        fields = CHARACTER_FIELDS
