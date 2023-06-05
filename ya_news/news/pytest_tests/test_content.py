import pytest

from django.urls import reverse
from django.conf import settings

from news.models import News

HOME_URL = reverse('news:home')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    ),
)
def test_create_comment_form_for_auth_user(parametrized_client,
                                           news_pk, form_in_context):
    url = reverse('news:detail', args=news_pk)
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_context


@pytest.mark.django_db
def tests_of_order_news(news_list, client):
    """
    Tests of news order.
    """
    response = client.get(HOME_URL)
    assert response.context['object_list'] == response.context['news_list']
    object_list = response.context['object_list']
    news_date = object_list[0].date
    all_dates = [news.date for news in object_list]
    assert news_date == max(all_dates)


@pytest.mark.django_db
def tests_news_count(news_list, client):
    """
    Tests of pagination.
    """
    response = client.get(HOME_URL)
    assert response.context['object_list'] == response.context['news_list']
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def tests_of_order_comments(comment_list, client, news_pk):
    """
    Tests of comments order.
    """
    url = reverse('news:detail', args=news_pk)
    response = client.get(url)
    assert isinstance(response.context['news'], News)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created <= all_comments[1].created
