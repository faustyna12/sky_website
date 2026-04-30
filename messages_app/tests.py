# Author: Faustyna Szulc (w2081508)
import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Message


class MessageModelTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user( #creating test sender user
            username="sender",
            password="testpass123"
        )
        self.receiver = User.objects.create_user( #creating test receiver user
            username="receiver",
            password="testpass123"
        )

    def test_message_can_be_created(self): #testing that a message can be created with the expected fields and default values
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject="Test Subject",
            content="This is a test message",
            message_type="sent",
            status="sent"
        )

        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.subject, "Test Subject")
        self.assertEqual(message.content, "This is a test message")
        self.assertEqual(message.message_type, "sent")
        self.assertEqual(message.status, "sent")
        self.assertFalse(message.read_status)

    def test_message_string_returns_subject(self): #testing that the string representation of a message returns the subject field
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject="My Message",
            content="Message content"
        )

        self.assertEqual(str(message), "My Message")


class MessageViewsTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user( #creating test sender user
            username="sender",
            password="testpass123"
        )
        self.receiver = User.objects.create_user( #creating test receiver user
            username="receiver",
            password="testpass123"
        )

        self.sent_message = Message.objects.create( #creating a test sent message
            sender=self.sender,
            receiver=self.receiver,
            subject="Sent Test",
            content="This is a sent message",
            message_type="sent",
            status="sent"
        )

        self.draft_message = Message.objects.create( #creating a test draft message
            sender=self.sender,
            receiver=self.receiver,
            subject="Draft Test",
            content="This is a draft message",
            message_type="draft",
            status="draft"
        )

    def test_inbox_page_loads(self): #testing that the inbox page loads correctly for a logged-in user
        self.client.login(username="receiver", password="testpass123")

        response = self.client.get(reverse("inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/inbox.html")
        self.assertContains(response, "Sent Test")

    def test_sent_messages_page_loads(self): #testing that the sent messages page loads correctly for a logged-in user
        self.client.login(username="sender", password="testpass123")

        response = self.client.get(reverse("sent_messages"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/sent.html")
        self.assertContains(response, "Sent Test")

    def test_drafts_page_loads(self): #testing that the drafts page loads correctly for a logged-in user
        self.client.login(username="sender", password="testpass123")

        response = self.client.get(reverse("drafts"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/drafts.html")
        self.assertContains(response, "Draft Test")

    def test_compose_page_loads(self): #testing that the compose message page loads correctly for a logged-in user
        self.client.login(username="sender", password="testpass123")

        response = self.client.get(reverse("compose_message"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/compose.html")

    def test_user_cannot_see_other_users_inbox_message(self): #testing that a user cannot see messages in their inbox that are not addressed to them
        other_user = User.objects.create_user(
            username="other",
            password="testpass123"
        )

        self.client.login(username="other", password="testpass123")

        response = self.client.get(reverse("inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sent Test")


class ComposeMessageTest(TestCase):

    def setUp(self): #setting up test sender and receiver users for testing the compose message functionality
        self.sender = User.objects.create_user(
            username="sender",
            password="testpass123"
        )
        self.receiver = User.objects.create_user( #creating test receiver user
            username="receiver",
            password="testpass123"
        )

    def test_send_new_message(self):
        self.client.login(username="sender", password="testpass123")

        response = self.client.post(reverse("compose_message"), { 
            "recipient": [self.receiver.id],
            "subject": "New Message",
            "body": "Hello receiver",
            "status": "sent"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.first()
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.subject, "New Message")
        self.assertEqual(message.content, "Hello receiver")
        self.assertEqual(message.status, "sent")

    def test_save_message_as_draft(self): #testing that a new message can be saved as a draft successfully and is saved with the expected fields and values
        self.client.login(username="sender", password="testpass123")

        response = self.client.post(reverse("compose_message"), { 
            "subject": "Draft Message",
            "body": "This is a draft",
            "status": "draft"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.first() #testing that the message is saved with the expected fields and values for a draft message
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.subject, "Draft Message")
        self.assertEqual(message.content, "This is a draft")
        self.assertEqual(message.status, "draft")