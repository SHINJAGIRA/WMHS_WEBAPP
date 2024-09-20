from .models import *
from django.shortcuts import render, redirect, get_object_or_404,reverse
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from urllib.parse import quote  
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def index(request):
    upcoming=UpcomingEvent.objects.all()
    events=Event.objects.all()
    principal=Staff.objects.filter(position='Principal').first()
    context = {
        'upcoming':upcoming,
        'events':events,
        'principal':principal
        }
    return render(request, 'main/home.html', context)

def staff_administration(request):    
    staff = Staff.objects.all()
    teacher = Teacher.objects.all()
    context = {
        'staffs': staff,
        'teachers': teacher
    }
    return render(request, 'about/school_admin.html', context)

def blog(request):
    blogs = Blog.objects.all().order_by('category')  
    categorized_blogs = {}

    for blog in blogs:
        if blog.category in categorized_blogs:
            categorized_blogs[blog.category].append(blog)
        else:
            categorized_blogs[blog.category] = [blog]

    context = {
        'categorized_blogs': categorized_blogs
    }

    return render(request, 'main/blog.html', context)

def blog_details(request,id):
    blog = get_object_or_404(Blog, id = id)
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect(request.path)
    else:
        form = CommentForm()
        return render(request,'main/blog_details.html', {'blog':blog})
    return render(request, 'main/blog.html')
def tvet(request):
    return render(request, 'main/tvet_program.html')



def homework(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = SearchForm(request.POST)
        if form.is_valid():
            trade = form.cleaned_data['trade']
            results = Homework.objects.filter(trade=trade)

            categorized_homeworks = {}
            for homework in results:
                trade_name = homework.trade.name
                if trade_name not in categorized_homeworks:
                    categorized_homeworks[trade_name] = []

                categorized_homeworks[trade_name].append({
                    'title': homework.title,
                    'levels': ', '.join([level.name for level in homework.module.level.all()]),
                    'download_url': homework.get_download_url(),  # Ensure this method exists in your model
                    'details_url': homework.get_details_url(),  # Ensure this method exists in your model
                })

            return JsonResponse({'results': categorized_homeworks})

    # If not an AJAX POST request, render the initial page with all homeworks
    homeworks = Homework.objects.all().order_by('trade')
    categorized_homeworks = {}
    for homework in homeworks:
        trade_name = homework.trade.name
        if trade_name not in categorized_homeworks:
            categorized_homeworks[trade_name] = []
        categorized_homeworks[trade_name].append(homework)

    context = {
        'homeworks': categorized_homeworks,
        'form': SearchForm(),
    }
    return render(request, 'main/homeworks.html', context)

def download_homework(request, year, month, day, title):
    homework = get_object_or_404(Homework, title=title)
    filename=f"{quote(title)}.pdf"
    response = HttpResponse(homework.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def download_pastpaper(request, year, month, day, title):
    pastpaper = get_object_or_404(PastPaper, title=title)
    filename=f"{quote(title)}.pdf"
    response = HttpResponse(pastpaper.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            subject=form.cleaned_data['subject']
            description=form.cleaned_data['description']
            email=form.cleaned_data['email']
            full_message = f"Message from {name} ({email}):\n\n{description}"
            send_mail(
                subject,
                full_message,
                email,
                ['tennodes10@gmail.com']
            )
            return HttpResponseRedirect('contact')
    else:
        Contact=ContactForm()
    return render(request,'main/contactus.html',{'form':Contact})

    
def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            msg = f'{email} has successfully subscribed to our newsletter'
            subject = "SUCCESSFULLY SUBSCRIBED TO WMHS"
            
            # Check if email already exists in the database
            is_email_stored = Subscriber.objects.filter(email=email).exists()
            
            if not is_email_stored:
                form.save()
                send_mail(
                    subject,
                    msg,
                    'tennodes10@gmail.com',
                    [email],
                )
                messages.success(request, 'You have successfully subscribed to our newsletter!')
                print('hehehe')
                return JsonResponse({'status': 'success', 'message': 'You have successfully subscribed to our newsletter!'})
            else:
                messages.info(request, 'This email is already subscribed.')
                print('hello')
                return JsonResponse({'status': 'info', 'message': 'This email is already subscribed.'})
                
        else:
            print('hehehe')
            return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})
            
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def our_history(request):
    return render(request,'main/History.html')

def download_file(request,filename):
    file_path=os.path.join(settings.MEDIA_ROOT,filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path,'rb'))
    else:
        raise Http404("file not found")


def past_papers(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = PapersSearchForm(request.POST)
        if form.is_valid():
            years = form.cleaned_data['year']
            print(years)
            results = PastPaper.objects.filter(year=str(years))
            print(results)
            categorized_pastpapers = {}
            for pastpaper in results:
                year = pastpaper.year
                if year not in categorized_pastpapers:
                    categorized_pastpapers[year] = []

                categorized_pastpapers[year].append({
                    'title': pastpaper.title,
                    'levels': ', '.join([level.name for level in pastpaper.module.level.all()]),
                    'download_url': pastpaper.get_download_url(),  # Ensure this method exists in your model
                    'details_url': pastpaper.get_details_url(),  # Ensure this method exists in your model
                })

            return JsonResponse({'results': categorized_pastpapers})
    else:
        pastpaper = PastPaper.objects.all().order_by('year')
        categorized_pastpapers = {}
        for pastpaper in pastpaper:
            year = pastpaper.year
            if year not in categorized_pastpapers:
                categorized_pastpapers[year] = []
            categorized_pastpapers[year].append(pastpaper)

        context = {
            'pastpaper': categorized_pastpapers,
            'form': PapersSearchForm(),
        }
        return render(request,'main/past_papers.html',context)

def pastpaper_details(request,id):
    pastpaper=get_object_or_404(PastPaper,id=id)
    return render(request,'main/pastpaper_details.html',{'pastpaper':pastpaper})
def homework_details(request,id):
    homework=get_object_or_404(Homework,id=id)
    return render(request,'main/homework_details.html',{'homework':homework})

def IndexVideo(request):
    videos = Video.objects.all()
    return render(request, 'main/video.html', {'videos': videos})