from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model

# User = get_user_model()
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    # picture = models.ImageField(upload_to='images')
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    pass


class Chat(models.Model):
    first_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='chats1')
    second_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='chats2')

    class Meta:
        unique_together = ('first_user','second_user')
    # def __str__(self) -> str:
    #     return f'{self.first_user}, {self.second_user}'

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='messages')
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.text

# Create your models here.
