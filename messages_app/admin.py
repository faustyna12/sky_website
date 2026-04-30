# Author: Faustyna Szulc (w2081508)
from django.contrib import admin
from .models import Message
class MessageAdmin(admin.ModelAdmin):
# display relevant fields in the admin list view for easier management of messages

    list_display = ('sender', 'receiver','id','message_type', 'timestamp', 'subject', 'read_status')
    list_filter = ('timestamp','message_type', 'read_status')
    search_fields = ('sender__username', 'receiver__username','subject', 'content')
# make timestamp read-only in the admin interface and order messages by most recent first
readonly_fields = ('timestamp',)
ordering = ('-timestamp',)
date_hierarchy = 'timestamp'
admin.site.register(Message, MessageAdmin)
