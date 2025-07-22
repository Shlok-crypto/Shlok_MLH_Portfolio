# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        # Clear existing data to ensure isolation
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "About Me" in html

    def test_timeline(self):
        # Test GET when empty
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Test POST
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test post'
        }
        post_response = self.client.post("/api/timeline_post", data=post_data)
        assert post_response.status_code == 200
        new_post = post_response.get_json()
        assert new_post['name'] == 'Test User'
        assert new_post['email'] == 'test@example.com'
        assert new_post['content'] == 'This is a test post'

        # Test GET again — now it should have one post
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]['name'] == 'Test User'

    def test_timeline_page(self):
        # Manually insert a post into the database
        TimelinePost.create(
            name="Alice",
            email="alice@example.com",
            content="Hello from Alice!"
        )

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert "Share Your Story" in html
        assert "timeline-form" in html
        assert "timeline-posts" in html or "Hello from Alice" in html
    
    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data=
            {"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data=
            {"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
            {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


