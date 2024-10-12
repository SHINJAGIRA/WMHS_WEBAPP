from django.db import models
from django.utils import timezone
import os
from django.core.files.base import ContentFile
import io
import PyPDF2
from django.utils.translation import gettext_lazy as _
import datetime
from django.urls import reverse

def staff_pic(instance, filename):
    return f"staff/{instance.first_name}_{instance.last_name}/{filename}"

def blog_pic(instance, filename):
    return f"blog/{filename}"

def gallery(filename):
    return f"gallery/{filename + timezone.now()}"

def comment_pic(instance, filename):
    return f"blog_comments/{instance.blog.title}/{filename}"

CATEGORY_CHOICES = (
    ('Sports','Sports'),
    ('Education','Education'),
    ('Entertainment','Entertainment'),
    ('Media','Media'),
    ('Religion','Religion'),
    ('Business','Business')
)
TRADE_CHOICES=(
    ('SOD',"SOD"),
    ('NIT','NIT'),
    ('MMP',"MMP")
    )

CLASS_CHOICES = (
    ('Level 3 SOD A','Level 3 SOD A'),
    ('Level 3 SOD B','Level 3 SOD B'),
    ('Level 3 SOD','Level 3 SOD'),
    ('Level 3 NIT ','Level 3 NIT'),
    ('Level 3 MM','Level 3 MM'),
    ('Level 4 SOD A','Level 4 SOD A'),
    ('Level 4 SOD B','Level 4 SOD B'),
    ('Level 4 SOD','Level 4 SOD'),
    ('Level 4 NIT','Level 4 NIT'),
    ('Level 4 MM','Level 4 MM'),
    ('Level 5 SOD','Level 5 SOD'),
    ('Level 5 NIT','Leve 5 NIT'),
    ('Level 5 MM','Level 5 MM')
    )

def yearchoice():
    current_year=datetime.date.today().year
    return [(str(year),str(year)) for year in range(2018,current_year+1)]



class Staff(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(max_length=100, null=True, blank=True, upload_to=staff_pic)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(max_length=100, null=True, blank=True, upload_to=staff_pic)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class_teacher = models.CharField(max_length=20,choices=CLASS_CHOICES,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Level(models.Model):
    name = models.CharField(max_length=100, choices=CLASS_CHOICES)
    
    def __str__(self):
        return self.name


class Module(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name='modules')
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.ManyToManyField(Level)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Trade(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.ManyToManyField(Level)
    modules = models.ManyToManyField(Module)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class UpcomingEventManager(models.Manager):
    def move_expired_to_events(self):
        today = timezone.now().date()
        expired_events = self.filter(start_date__lte=today)
        
        for event in expired_events:
            Event.objects.create(
                title=event.title,
                description=event.description,
                image=event.image,
                end_date=event.end_date
            )
            event.delete()

class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='upcomingevents/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    objects = UpcomingEventManager()


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/%Y/%m/%d/', blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PastPaper(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category=models.CharField(max_length=200)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='past')
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='past')
    year=models.CharField(_("Year"),choices=yearchoice(),max_length=200,null=True,default="no year")
    thumbnail = models.ImageField(upload_to='pastpaper_thumbnails/', null=True, blank=True)
    file = models.FileField(upload_to='past_paper/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def get_download_url(self):
        return reverse('download_pastpaper', args=[self.created_at.year, self.created_at.month, self.created_at.day, self.title])

    def get_details_url(self):
        return reverse('pastpaper_details', args=[self.id])
class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='homeworks')
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='homeworks')
    file = models.FileField(upload_to='homeworks/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='homeworks_thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_download_url(self):
        return reverse('download_homework', args=[self.created_at.year, self.created_at.month, self.created_at.day, self.title])

    def get_details_url(self):
        return reverse('homework_details', args=[self.id])
    def save(self, *args, **kwargs):
        # Save the instance first to ensure `file.path` is available
        super().save(*args, **kwargs)

        # Check if a thumbnail needs to be generated
        if self.file and (self.pk is None or not self.thumbnail):
            self.generate_thumbnail()
            # Save again to store the thumbnail
            super().save(*args, **kwargs)


    def delete(self,*args, **kwargs):
        PastPaper.objects.create(
            title=self.title,
            description=self.description,
            category='Homework',
            module=self.module,
            trade=self.trade,
            file=self.file,
            thumbnail=self.thumbnail,

        )
        return super(Homework,self).delete(*args,**kwargs)
    def generate_thumbnail(self):
        try:
            import PyPDF2
            from pdf2image import convert_from_path
        except ImportError as e:
            print(f"Error importing required libraries: {e}")
            return

        pdf_path = self.file.path
        if not os.path.exists(pdf_path):
            print(f"PDF file does not exist: {pdf_path}")
            return

        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                print(f"Successfully opened PDF. Number of pages: {num_pages}")

            images = convert_from_path(pdf_path, first_page=1, last_page=1)

            if images:
                image = images[0]
                thumbnail_io = io.BytesIO()
                image.save(thumbnail_io, format="JPEG")
                thumbnail_name = f'{self.title}_thumbnail.jpg'
                self.thumbnail.save(thumbnail_name, ContentFile(thumbnail_io.getvalue()), save=False)
                print(f"Thumbnail generated: {thumbnail_name}")
            else:
                print("No images were generated from the PDF")

        except Exception as e:
            print(f"Failed to process PDF: {str(e)}")

class Testimonial(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/%Y/%m/%d/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or "Anonymous"


class Announcement(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField(blank=True,null=True)
    attachment = models.FileField(blank=True,null=True,upload_to='announcements/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Untitled"


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='notes')
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='notes/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.CharField(max_length=100,null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,)
    attachent = models.FileField(upload_to=blog_pic,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    commenter_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.commenter_name} on {self.blog.title}"

class Gallery(models.Model):
    title = models.CharField(null=True,max_length=100,blank=True)
    content = models.TextField(null = True, blank=True)
    file = models.FileField(upload_to=gallery)


class Subscriber(models.Model):
    email=models.EmailField(null=False,max_length=100,unique=True)
    subscribed_at=models.DateTimeField(auto_now=True)


class Image(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='static/images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="videos/poster/")
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/videos/' , max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
