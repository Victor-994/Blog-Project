from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Article
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.core.mail import message, send_mail
from .forms import EmailPostForm

# Create your views here.


def article_detail(request, year, month, day, slug):
    article = get_object_or_404(Article, publish__year=year, publish__day=day,
                                publish__month=month, slug=slug, status="published")

    context = {"article": article}

    return render(request, "blog/article_detail.html", context)


def article_list(request):
    object_list = Article.objects.filter(status="published")
    paginator = Paginator(object_list, 2)
    # THIS MEANS THAT THERE WOULD BE THREE POSTS IN EACH PAGE
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # THIS MEANS THAT IF THE PAGE IS NOT AN INTEGER, WE ARE GOING TO DELIVER THE FIRST PAGE
        articles = paginator.page(1)
    except EmptyPage:
        # IF THE PAGE IS OUT OF RANGE, DELIVER THE LAST PAGE OF THE RESULTS
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        'page': page
    }

    return render(request, 'blog/article_list.html', context)


def article_share(request, post_id):
    # THIS FUNCTION RETRIEVES POSTS BY ID
    articles = get_object_or_404(Article, id=post_id, status="published")
    sent = False
    if request.method == "POST":
        # THE FORM WAS SUBMITTED
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # FORM FIELDS VALIDATION
            cd = form.cleaned_data
            # SEND MAIL
            post_url = request.build_absolute_uri(articles.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f" {articles.title}"
            message = f"Read {articles.title} at {post_url} \n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"

            send_mail(subject, message, 'designedbytochi@gmail.com',
                      [cd['to']])

            sent = True
    else:
        form = EmailPostForm()

    context = {'articles': articles, "form": form, 'sent': sent}
    return render(request, "blog/share.html", context)
