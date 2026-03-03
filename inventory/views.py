from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from .models import Book
from .serializers import BookSerializer

@csrf_exempt
@api_view(['GET', 'POST'])
def books_api(request):
    if request.method == 'GET':
        books = Book.objects.all()
        
        search_query = request.query_params.get('search')
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) | Q(author__name__icontains=search_query)
            ).distinct()

        sort_param = request.query_params.get('sort')
        if sort_param == 'price_asc':
            books = books.order_by('price')
        elif sort_param == 'price_desc':
            books = books.order_by('-price')
        elif sort_param == 'title':
            books = books.order_by('title')

        return JsonResponse({
            "Message": "All books retrieved successfully.",
            "inventory": BookSerializer(books, many=True).data
        }, safe=False)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "Message": "Book successfully added to Reader's Haven!",
                "data": serializer.data
            }, safe=False)
        return HttpResponse(f"ERROR: A book must have valid data. {serializer.errors}", status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_api(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'GET':
        return JsonResponse(BookSerializer(book).data, safe=False)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "Message": f"Book {book_id} updated.", 
                "data": serializer.data
            }, safe=False)
        return HttpResponse("ERROR: Could not update book.", status=400)

    elif request.method == 'DELETE':
        book.delete()
        
        remaining_books = Book.objects.all()
        return JsonResponse({
            "Message": f"The book with ID {book_id} has been deleted.",
            "data": BookSerializer(remaining_books, many=True).data
        }, safe=False)