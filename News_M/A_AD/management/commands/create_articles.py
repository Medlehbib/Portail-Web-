from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
from A_AD.models import Article, Categorie  # غيّر a_ad إذا تطبيقك مختلف


class Command(BaseCommand):
    help = "Créer 10 articles automatiquement avec image et vidéo factices"

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        categories = list(Categorie.objects.all())

        if not categories:
            self.stdout.write(self.style.ERROR("⚠️ Pas de catégories trouvées. Ajoutez-en au moins une."))
            return

        for i in range(10):
            article = Article.objects.create(
                titre=fake.sentence(nb_words=6),
                contenu=fake.paragraph(nb_sentences=10),
                categorie=random.choice(categories),
            )

            # ==== Ajouter une image factice ====
            img_url = f"https://picsum.photos/600/400?random={i}"
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                article.image.save(f"article_{i}.jpg", ContentFile(img_response.content), save=True)

            # ==== Ajouter une "fausse vidéo" ====
            # مبدئياً نحط ملف فارغ (لأن توليد فيديو صعب) – تقدر تحط فيديو حقيقي من عندك
            fake_video = ContentFile(b"Fake video content")
            article.video.save(f"video_{i}.mp4", fake_video, save=True)

        self.stdout.write(self.style.SUCCESS("✅ 10 articles avec images et vidéos ont été ajoutés !"))
