from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    author = models.ManyToManyField(Author) 

    def __str__(self):
        author_names = ", ".join([a.name for a in self.author.all()])
        return f"{self.title} by {author_names}"