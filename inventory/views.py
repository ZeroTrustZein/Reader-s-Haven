from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

@api_view(['GET', 'POST'])
def books_api(request):
    
    if request.method == 'GET':
        books = Book.objects.all()

        search_query = request.query_params.get('search')
        if search_query:
            books = books.filter(title__icontains=search_query)

        sort_param = request.query_params.get('sort')
        if sort_param == 'price_asc':
            books = books.order_by('price')
        elif sort_param == 'price_desc':
            books = books.order_by('-price')
        elif sort_param == 'title':
            books = books.order_by('title')

        author_query = request.query_params.get('author')
        if author_query:
            books = books.filter(author__name__icontains=author_query)

        serializer = BookSerializer(books, many=True)
        return Response({"inventory": serializer.data})

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book added!", "data": serializer.data})
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_api(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated!", "data": serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return Response({"message": "Book deleted successfully!"})