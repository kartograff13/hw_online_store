from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу 'Модератор продуктов' и назначает права can_unpublish_product и delete_product"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        content_type = ContentType.objects.get_for_model(Product)
        unpublish_permission = Permission.objects.get(codename="can_unpublish_product", content_type=content_type)
        delete_permission = Permission.objects.get(codename="delete_product", content_type=content_type)
        group.permissions.add(unpublish_permission, delete_permission)
        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' успешно создана/обновлена"))
