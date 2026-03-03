from django.test import TestCase
import json
from .models import Book, Author

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create a test author and book
        self.author = Author.objects.create(name="Zein Dergham")
        self.book = Book.objects.create(title="Mastering Leipzig Networks", price=35.00)
        self.book.author.add(self.author)

    def test_get_all_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mastering Leipzig Networks", str(response.content))

    def test_add_new_book(self):
        data = {"title": "Secure Coding", "price": "50.00", "authors": ["Dr. Nono"]}
        response = self.client.post('/api/books/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Book.objects.filter(title="Secure Coding").exists())

    def test_delete_book(self):
        # 1. The robot picks the ID of the book we made in setUp
        book_id = self.book.id
        
        # 2. It hits the Delete URL
        response = self.client.delete(f'/api/books/{book_id}/')
        
        # 3. It checks if the server says OK
        self.assertEqual(response.status_code, 200)
        
        # 4. It checks the database to make sure that ID is GONE
        self.assertFalse(Book.objects.filter(id=book_id).exists())