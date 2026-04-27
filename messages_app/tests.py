import django
from django.test import TestCase

from sky_website import messages_app

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from sky_website.messages_app.models import Message


class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="testpass123"
        )

    def test_create_message(self):
        """Test that a message can be created successfully"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject="Test Subject",
            body="This is a test message",
            status="sent"
        )

        self.assertEqual(message.subject, "Test Subject")
        self.assertEqual(message.body, "This is a test message")
        self.assertEqual(message.sender.username, "sender")
        self.assertEqual(message.receiver.username, "receiver")
        self.assertEqual(message.status, "sent")


class MessageViewTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="testpass123"
        )

        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject="Hello",
            body="Test message body",
            status="sent"
        )

    def test_inbox_view_logged_in(self):
        """Test inbox page loads for logged-in user"""
        self.client.login(username="receiver", password="testpass123")
        response = self.client.get(reverse("inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")

    def test_sent_view_logged_in(self):
        """Test sent page loads for logged-in user"""
        self.client.login(username="sender", password="testpass123")
        response = self.client.get(reverse("sent_messages"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")

    def test_draft_view_logged_in(self):
        """Test draft page loads"""
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject="Draft Test",
            body="Draft body",
            status="draft"
        )

        self.client.login(username="sender", password="testpass123")
        response = self.client.get(reverse("draft_messages"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Test")

    def test_user_cannot_see_others_messages(self):
        """Users should only see their own inbox"""
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )

        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(reverse("inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Hello")


class SendMessageTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="testpass123"
        )

    def test_send_new_message(self):
        """Test sending a new message"""
        self.client.login(username="sender", password="testpass123")

        response = self.client.post(reverse("new_message"), {
            "receiver": self.receiver.id,
            "subject": "New Test Message",
            "body": "This is a new message",
            "status": "sent"
        })

        self.assertEqual(response.status_code, 302)  # Redirect after send
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.first()
        self.assertEqual(message.subject, "New Test Message")
        self.assertEqual(message.status, "sent")

    def test_save_draft_message(self):
        """Test saving a message as draft"""
        self.client.login(username="sender", password="testpass123")

        response = self.client.post(reverse("new_message"), {
            "receiver": self.receiver.id,
            "subject": "Draft Message",
            "body": "Saved as draft",
            "status": "draft"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.first()
        self.assertEqual(message.status, "draft")
                                      
                                  