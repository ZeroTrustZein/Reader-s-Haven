from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    author = models.ManyToManyField(Author) # this is so that when we delete the author his books are also deleted

    def __str__(self):
        return f"{self.title} by {self.author.name}"    # so that we have names not object()