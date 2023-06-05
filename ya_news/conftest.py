import pytest
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from news.models import News, Comment
from news.forms import BAD_WORDS


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок новости', text='Текст новости')
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def news_pk(news):
    return news.pk,


@pytest.fixture
def form_data():
    return {'text': 'Новый текст комментария'}


@pytest.fixture
def bad_words_data():
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.fixture
def news_list(news):
    today = timezone.now()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Текст новости',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    news_list = News.objects.bulk_create(all_news)
    return news_list


@pytest.fixture
def comment_list(author, news):
    comment = Comment.objects.bulk_create(
        Comment(news=news, author=author, text=f'Текст комментария {index}')
        for index in range(2)
    )
    return comment
