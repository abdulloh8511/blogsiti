from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify

# User(AbstractUser),
# Category, Blog, Comment, Like

class User(AbstractUser):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:60]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    img_url = models.URLField(max_length=200, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = (self.content or '')[:300]
        super().save(*args, **kwargs)

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        if self.img_url:
            return self.img_url
        return ''

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.blog.title}"


class BlogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'blog'], name='unique_blog_like')
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.blog.title}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profile_avatars/', 
        default='profile_avatars/default.jpg', 
        blank=True, 
        null=True
    )
    bio = models.TextField(max_length=500, blank=True)           # ixtiyoriy
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    # Profile modeliga
    total_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Har bir yangi user yaratilganda avtomatik Profile yaratib berish
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    
