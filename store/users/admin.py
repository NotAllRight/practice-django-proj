from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)

    # Перевизначення методу, щоб при створенні користувача
    # через адмін-панель вказаний пароль зберігався в моделі,
    # як захешованний
    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        else:
            obj = CustomUser.objects.get(id=obj.id)
            form.cleaned_data['password'] = obj.password
        super().save_model(request, obj, form, change)
