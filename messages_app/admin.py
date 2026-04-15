from django.contrib import admin
from .models import Message
class MessageAdmin(admin.ModelAdmin):

    list_display = ('sender', 'receiver','id','message_type', 'timestamp', 'subject', 'read_status')
    list_filter = ('timestamp','message_type', 'read_status')
    search_fields = ('sender__username', 'receiver__username','subject', 'content')

readonly_fields = ('timestamp',)
ordering = ('-timestamp',)
date_hierarchy = 'timestamp'
admin.site.register(Message, MessageAdmin)
