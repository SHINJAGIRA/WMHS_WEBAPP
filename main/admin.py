from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'position')
    list_filter = ('position', 'created_at', )
    search_fields = ('position', 'first_name', 'last_name', 'email', 'phone_number', 'created_at')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')

@admin.register(Testimonial)
class TestmonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'created_at')

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at','start_date','end_date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at','end_date')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at', )
    list_filter = ('first_name', 'last_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'created_at', )

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'name', 'description',)
    list_filter = ('teacher', 'name',  'created_at', )
    search_fields = ('teacher', 'name', 'created_at', )


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = ('name', 'level', 'created_at', )
    search_fields = ('name', 'level', 'created_at', )


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','module', 'trade')
    list_filter = ('title', 'module', 'trade', 'created_at', )
    search_fields = ('title', 'module', 'trade', 'created_at', )
    def delete_model(self,request,obj):
        obj.delete()
        
@admin.register(PastPaper)
class PastPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','category','module', 'trade','year')
    list_filter = ('title', 'module', 'trade','category', 'created_at', 'year')
    search_fields = ('title', 'module', 'trade','category', 'created_at','year' )

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','module', 'trade')
    list_filter = ('title', 'module', 'trade', 'created_at', )
    search_fields = ('title', 'module', 'trade', 'created_at', )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'attachent', 'created_at','updated_at')
    list_filter = ('title', 'created_at', )
    search_fields = ('title', 'created_at', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'commenter_name', 'content', 'created_at')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display=('email','subscribed_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display=('title','description')