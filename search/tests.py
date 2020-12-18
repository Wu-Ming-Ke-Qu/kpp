from django.test import TestCase
from django.test import Client
from django.urls import reverse
# Create your tests here.

# create an instance of the client for our use
client = Client()


# 视图测试
class SearchViewTests(TestCase):

    def test_search_index_with_no_course(self):
        """
        搜索课程如果没有检索到结果
        则重新定向到search-noresult页面
        """
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_search_index_with_course(self):
        """
        搜索课程如果检索到结果
        则重新定向到search-result页面
        """
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

