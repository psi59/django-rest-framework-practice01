from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ", " + self.email + ", " + self.password


class Board(models.Model):
    author = models.ForeignKey('users.User')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateField()

    # def __str__(self):
    #     return self.author + ", " + self.title + ", " + self.content + ", " + \
    #            self.created_date.strftime('%Y-%m-%d %H:%M:%S')