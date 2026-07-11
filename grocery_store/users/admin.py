from django.contrib import admin

from .models import User


admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Модель пользователя в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * username - ник пользователя;
    * email - электронная почта пользователя;
    """

    list_display = ('username', 'email')
    list_filter = ('username',)
    search_fields = ('username', 'email',)
    ordering = ('username',)
