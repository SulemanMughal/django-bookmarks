from django.contrib import admin
from .models import  *

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link','user')
    list_filter = ('user', )
    ordering = ('title', )
    search_fields = ('title', )

admin.site.register(Link)
admin.site.register(Tag)
admin.site.register(SharedBookmark)
admin.site.register(Friendship)
admin.site.register(Invitation)
admin.site.register(Bookmark, BookmarkAdmin)