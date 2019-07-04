from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.contrib.auth.models import Permission, ContentType


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, telephone, password, **extra_fields):
        if not telephone:
            raise ValueError("请填入手机号码！")
        user = self.model(telephone=telephone, *extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(telephone, password)

    def create_superuser(self, telephone, password, **extra_fields):
        extra_fields['is_superuser'] = True
        return self._create_user(telephone, password)


class User(AbstractBaseUser):
    # uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True, validators=[validators.RegexValidator(r'1[3456789]\d{9}')])
    username = models.CharField(max_length=100)
    collection = models.ManyToManyField("Book", related_name="mybooks")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'telephone'
    objects = UserManager()


class Author(models.Model):
    authorname = models.CharField(max_length=20)


class State(models.Model):
    name = models.CharField(max_length=20)


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Catalog(models.Model):
    index = models.IntegerField()
    title = models.CharField(max_length=200)
    book = models.ForeignKey("Book",on_delete=models.CASCADE,related_name="books")
    content = models.ForeignKey("Content", on_delete=models.CASCADE, related_name="contents")


class Content(models.Model):
    content = models.TextField()


class Book(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to="cover")
    instruction = models.CharField(max_length=500)
    state = models.ForeignKey("State", on_delete=models.CASCADE, related_name="states",null=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="authors",null=True)
    tag = models.ManyToManyField("Tag", related_name="tags")
    # catalog = models.ForeignKey("Catalog",on_delete=models.CASCADE, related_name="catalogs",null=True)
    view_num = models.IntegerField(default=0)


    # content_type = ContentType.objects.get_for_model(Book)
    # permission = Permission.objects.create(name='可以查看的权限',codename='view_book',content_type=content_type)
