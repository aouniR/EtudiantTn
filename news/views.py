from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from users.decorators import student_profile_only
from .models import News

@login_required
@student_profile_only
def news(request):
    featured_news_all = News.objects.filter(is_featured=True)
    featured_news = featured_news_all.first()
    non_featured_news = News.objects.filter(is_featured=False)[:2] 
    recent_news_articles = featured_news_all[:5]  
    try:
        main_article = News.objects.filter(is_main_article=True).latest('pub_date')
    except News.DoesNotExist:
        main_article = None

    context = {
        'featured_news': featured_news,
        'news_articles': non_featured_news,
        'recent_news_articles': recent_news_articles,
        'main_article':main_article
    }

    return render(request, 'news/news.html', context)

@login_required
@student_profile_only
def detail_news(request, pk):
    news_article = get_object_or_404(News, pk=pk)
    return render(request, 'news/detail_news.html', {'news_article': news_article})

@login_required
@student_profile_only
def next_news(request, pk):
    next_article = News.objects.filter(pk__gt=pk).order_by('pk').first()
    if next_article:
        return detail_news(request, next_article.pk)
    else:
        return detail_news(request, pk)

@login_required
@student_profile_only
def previous_news(request, pk):
    previous_article = News.objects.filter(pk__lt=pk).order_by('-pk').first()
    if previous_article:
        return detail_news(request, previous_article.pk)
    else:
        return detail_news(request, pk)
