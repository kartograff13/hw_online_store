from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import BlogPost


class Command(BaseCommand):
    help = "Создаёт группу 'Контент-менеджер' с правами доступа на управление блогом"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Контент-менеджер")
        content_type = ContentType.objects.get_for_model(BlogPost)
        permissions = Permission.objects.filter(
            content_type=content_type, codename__in=["add_blogpost", "change_blogpost", "delete_blogpost"]
        )
        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS("Группа 'Контент-менеджер' успешно создана/обновлена"))
