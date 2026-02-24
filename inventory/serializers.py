from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']

    def create(self, validated_data):
        author_name = validated_data.pop('author')

        author_instance, created = Author.objects.get_or_create(name=author_name)

        book = Book.objects.create(author=author_instance, **validated_data)
        return book

    def update(self, instance, validated_data):
        if 'author' in validated_data:
            author_name = validated_data.pop('author')
            author_instance, created = Author.objects.get_or_create(name=author_name)
            instance.author = author_instance
        
        return super().update(instance, validated_data)