from django import forms
from .models import *
from .models import yearchoice

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commenter_name', 'content']


class ContactForm(forms.Form):
    name=forms.CharField( max_length=40, required=True,
    widget=forms.TextInput(attrs={
    'placeholder':'enter your name',
    'class':'w-full outline-none bg-gray-100 p-2.5 font-mono  border-none my-3 focus:ring-2 rounded-md focus:ring-secondary'
    })
    )
    email=forms.EmailField(max_length=30,required=True,
    widget=forms.EmailInput(attrs={
        'placeholder':'enter your email',
        'class':'w-full outline-none bg-gray-100 p-2.5 font-mono  border-none my-3 focus:ring-2 rounded-md focus:ring-secondary'
    }))
    subject=forms.CharField(max_length=100,
    widget=forms.TextInput(attrs={
        'placeholder': 'enter your Subject', 
        'class': 'w-full outline-none bg-gray-100 p-2.5 font-mono border-none my-3 focus:ring-2 rounded-md focus:ring-secondary'
        
    })
    )
    description=forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'enter the description', 
            'class': 'w-full outline-none bg-gray-100 p-2.5 font-mono border-none my-3 focus:ring-2 rounded-md focus:ring-secondary',
            'rows': 4
        })
)

class SubscriberForm(forms.ModelForm):
    # email=forms.EmailField(widget=forms.EmailInput(attrs={
    #     'class':'rounded-sm text-secondary border-none h-10 outline-none w-60 placeholder-opacity-50 italic text-sm',
    # }))
    class Meta:
        model=Subscriber
        fields=['email']

class SearchForm(forms.Form):
    trade = forms.ModelChoiceField(queryset=Trade.objects.all(), required=False,)

class PapersSearchForm(forms.Form):
    year = forms.ChoiceField(choices=yearchoice(), required=False,)