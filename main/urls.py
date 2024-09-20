from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',index,name='index'),
    path('staff_administration/', staff_administration, name='staff_administration'),
    path('blog/',blog,name='blog'),
    path('tvet',tvet,name='tvet'),
    path('homeworks/',homework,name='homework'),
    path('homeworks/<int:year>/<int:month>/<int:day>/<str:title>/', download_homework, name='download_homework'),
    path('blog/<int:id>',blog_details,name='blog_details'),
    path('contact',contact,name='contact'),
    path('subscribe/',subscribe_view,name='subscribe'),
    path('history/',our_history,name='history'),
    path('download/<str:filename>',download_file,name="download_file"),
    path('past_papers/',past_papers,name="past_papers"),
    path('homework/<int:id>',homework_details,name="homework_details"),
    path('pastpaper/<int:year>/<int:month>/<int:day>/<str:title>/', download_pastpaper, name='download_pastpaper'),
    path('gallery/videos/', IndexVideo , name='gallery_videos' ),
    path('pastpaper/<int:id>',pastpaper_details,name="pastpaper_details"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

