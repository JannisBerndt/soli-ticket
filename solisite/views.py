from django.shortcuts import render, redirect

def landingpage_view(request):
    return render(request, 'solisite/landingpage.html', context)

def blog_view(request):
    return render(request, 'solisite/blog.html')
