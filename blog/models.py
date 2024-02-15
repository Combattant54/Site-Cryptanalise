from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from functools import partial
import os

def build_format_function(directory_name):
    return partial(format_image_name, directory=directory_name)
    
def format_image_name(instance, document_name, directory="documents"):
    name = os.path.splitext(document_name)[0]
    return os.path.join(directory, "{}-{}".format(instance.id, name))

# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=100)
    categorie_image = models.ImageField(
        upload_to=build_format_function("Categories"), 
        verbose_name="Image de la catégorie",
        null=True,
    )
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=build_format_function("Profiles"), verbose_name="L'avatar de l'utilisateur")
    self_presentation = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    # @property
    # def written_articles(self):
    #     return Article.objects.filter(user=self.user).all()
    
    # @property
    # def liked_articles(self):
    #     return [o.id for o in Article.objects.all() if o.stars.contains(self)]

DEFAULT_SLUG = "-default-slug-"
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    slug = models.SlugField(default=DEFAULT_SLUG)
    autor = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.RESTRICT, related_name="written_articles")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de parution")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    categories = models.ManyToManyField(Categorie)
    stars = models.ManyToManyField(Profile, related_name="liked_articles")
    article_image = models.ImageField(
        upload_to=build_format_function("Articles"), 
        verbose_name="Image de l'article",
        null=True,
        default=None
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == DEFAULT_SLUG:
            self.slug = slugify(self.title)
        super().save()


class Document(models.Model):
    name = models.CharField(max_length=50)
    document = models.ImageField(upload_to=build_format_function("Documents"))

    def __str__(self) -> str:
        return self.name