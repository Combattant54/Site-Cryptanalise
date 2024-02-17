from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from functools import partial
import os, datetime, string, random, pytz

from django.db.models.signals import post_save
from django.dispatch import receiver

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
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        if self.slug is None:
            self.slug = slugify(self.name)
        
        return super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=build_format_function("Profiles"), verbose_name="L'avatar de l'utilisateur")
    self_presentation = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)
    
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
    categories = models.ManyToManyField(Categorie, related_name="articles")
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
        super().save(*args, **kwargs)


class Document(models.Model):
    name = models.CharField(max_length=50)
    document = models.ImageField(upload_to=build_format_function("Documents"))

    def __str__(self) -> str:
        return self.name

class Tokens(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(unique=True, max_length=30)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return f"Token for {self.url} by {self.user.username}"
    
    @staticmethod
    def generate_token(n=30):
        chars = string.ascii_letters + string.digits
        token_chars = [random.choice(chars) for _ in range(n)]
        return "".join(token_chars)
    
    def save(self, *args, **kwargs):
        if self.expiration_date is None:
            if self.creation_date is None:
                self.creation_date = datetime.datetime.now(tz=pytz.timezone("Europe/Paris"))
            self.expiration_date = self.creation_date + datetime.timedelta(minutes=10)
        
        if self.token is None or self.token == "":
            token = self.generate_token()
            while Tokens.objects.filter(token=token).first() is not None:
                token = self.generate_token()
            self.token = token
        return super().save(*args, **kwargs)



@receiver(post_save, sender=User)
def auto_create_profile(sender, instance: User, **kwargs):
    if Profile.objects.filter(user=instance).first() is None:
        profile = Profile()
        profile.user = instance
        profile.save()
    