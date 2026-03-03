from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(child=serializers.CharField(), write_only=True)
    author_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'author_names', 'price']

    def get_author_names(self, obj):
        return [author.name for author in obj.author.all()]

    def create(self, validated_data):
        author_names = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        for name in author_names:
            author_instance, _ = Author.objects.get_or_create(name=name)
            book.author.add(author_instance)
        return book

    def update(self, instance, validated_data):
        author_names = validated_data.pop('authors', None)
        instance = super().update(instance, validated_data)
        if author_names is not None:
            author_instances = [Author.objects.get_or_create(name=name)[0] for name in author_names]
            instance.author.set(author_instances)
        return instance