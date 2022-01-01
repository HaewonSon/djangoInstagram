from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestPosts(TestCase): # test로 시작하는 함수를 찾아 실행
    def setUp(self): # 테스트를 위한 테스트데이터 생성
        User = get_user_model()
        self.user = User.objects.create_user(
            username='jungo', email='jungo@gamil.com', password='top_secret'
        )

    def test_get_posts_page(self):
        url = reverse('posts:post_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_post_creating_posts(self): # 게시물 만들기
        login = self.client.login(username="jungo", password="top_secret") # 로그인
        self.assertTrue(login)

        url = reverse('posts:post_create') # 게시물 만들기
        image = SimpleUploadedFile("./test.jpg", b"whatevercontents")
        response = self.client.post(
            url,
            {"image": image, "caption": 'test'}
        )

        self.assertEqual(response.status_code, 200) # 정상적으로 요청되었다면 base.html로 이동
        self.assertTemplateUsed(response, "posts/base.html")

    def test_post_posts_create_not_login(self): # 로그인이 안되어있다면?
        url = reverse('posts:post_create')
        image = SimpleUploadedFile("./test.jpg", b"whatevercontents")
        response = self.client.post(
            url,
            {"image": image, "caption": 'test test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/main.html")
