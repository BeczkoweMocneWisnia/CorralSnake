import uuid

from django.db import models

from CorralSnake.utils import uuid_upload_to


class Article(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    image = models.ImageField(upload_to=uuid_upload_to('article/images'))

    def __str__(self):
        return f'{self.title} - {self.author.email}'

    def delete(self, using=None, keep_parents=False):
        if self.image.name != self.image.field.default:
            self.image.delete()

        return super().delete(using, keep_parents)
