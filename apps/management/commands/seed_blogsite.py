from django.core.management.base import BaseCommand
from apps.models import Category, Blog, User, Tag


class Command(BaseCommand):
    help = "BlogSite uchun test ma'lumotlarini yaratadi (6 ta kategoriya, har biriga 5 tadan blog)."

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin12345",
            )
            self.stdout.write(self.style.WARNING(
                "Superuser yaratildi: admin / admin12345"
            ))

        category_names = [
            "Texnologiya",
            "Ta'lim",
            "Sog'liq",
            "Sayohat",
            "Biznes",
            "Madaniyat",
        ]

        categories = []
        for name in category_names:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={'description': f"{name} bo‘yicha foydali maqolalar."}
            )
            categories.append(category)

        tag_names = ["Trend", "Maslahat", "Boshlovchi", "Professional", "Qiziqarli", "Foydali"]
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        sample_paragraph = (
            "Bu blogdagi maqola qisqacha kirish bo‘lib, mavzuga doir asosiy fikrlarni "
            "o‘z ichiga oladi. Maqola davomida foydali misollar va amaliy tavsiyalar "
            "beriladi. Oxirida esa qisqa xulosa va keyingi o‘qishlar uchun yo‘nalishlar "
            "keltiriladi."
        )

        created_count = 0
        for category in categories:
            existing = Blog.objects.filter(author=admin, category=category).count()
            to_create = max(0, 5 - existing)
            for i in range(to_create):
                title = f"{category.name} bo‘yicha maqola {existing + i + 1}"
                blog = Blog.objects.create(
                    title=title,
                    content=sample_paragraph,
                    author=admin,
                    category=category,
                    img_url=f"https://picsum.photos/seed/{category.id}-{existing + i + 1}/800/600",
                    status='published',
                )
                blog.tags.set(tags[:3])
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Yakunlandi: {len(categories)} ta kategoriya, {created_count} ta blog yaratildi."
        ))
