from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Загружает начальные данные из фикстур"

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("Очистка базы данных..."))

        from catalog.models import Category, Contact, Product

        Product.objects.all().delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("База данных очищена."))

        self.stdout.write(self.style.HTTP_INFO("Загрузка данных из фикстур..."))

        try:
            call_command("loaddata", "catalog/fixtures/category_fixture.json")
            self.stdout.write("Категории загружены.")

            call_command("loaddata", "catalog/fixtures/product_fixture.json")
            self.stdout.write("Продукты загружены.")

            call_command("loaddata", "catalog/fixtures/contact_fixture.json")
            self.stdout.write("Контакты загружены.")

            from catalog.models import Category, Contact, Product

            self.stdout.write(f"Статистика:")
            self.stdout.write(f"   Категорий: {Category.objects.count()}")
            self.stdout.write(f"   Продуктов: {Product.objects.count()}")
            self.stdout.write(f"   Контактов: {Contact.objects.count()}")

            self.stdout.write(self.style.SUCCESS("\nДанные успешно загружены!"))

        except Exception as e:
            self.stderr.write(f"Ошибка при загрузке данных: {e}")
            import traceback
            traceback.print_exc()
