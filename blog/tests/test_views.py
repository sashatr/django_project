from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User
from blog import views


class LoginViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'efwef@frvr.com', 'test123123')
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/login.html')

    def test_view_login(self):
        user = User.objects.get(username='test_user')

        self.client.force_login(user)
        resp = self.client.post('/login/', {'username': 'test_user', 'password': 'test123123'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/', fetch_redirect_response=False)

    def test_view_logout(self):
        user = User.objects.get(username='test_user')

        self.client.force_login(user)
        resp = self.client.post('/login/', {'username': 'test_user', 'password': 'test123123'})
        self.assertEqual(resp.status_code, 302)

        resp_ = self.client.get('/exit/')
        self.assertEqual(resp_.status_code, 302)
        self.assertRedirects(resp_, '/', fetch_redirect_response=False)


class RegisterViewTest(TestCase):
    def test_view_register(self):
        resp = self.client.post('/register/', {'username': 'test_user2', 'password1': 'bhuvgy123!', 'password2': 'bhuvgy123!'})
        self.assertEqual(resp.status_code, 302)

        user = User.objects.get(username='test_user2')
        self.assertEqual(user.username, 'test_user2')


class PostViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'efwef@frvr.com', 'test123123')
        user = User.objects.get(username='test_user')
        Post.objects.create(author=user, title='test1', text='text1', published=True, pk=1)
        Post.objects.create(author=user, title='test2', text='text2', published=True, pk=2)
        Post.objects.create(author=user, title='test3', text='text3', published=False, pk=3)
        resp_login = self.client.post('/login/', {'username': 'test_user', 'password': 'test123123'})
        self.assertEqual(resp_login.status_code, 302)

    def test_view_post_edit(self):
        post_ = Post.objects.get(pk=1)
        edit_titile = post_.title

        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        resp = self.client.post('/post/1/edit/', {'title': 'test1_edit', 'text': 'text1', 'published': True})
        self.assertEqual(resp.status_code, 302)

        post_ = Post.objects.get(pk=1)
        edit_titile_ = post_.title

        self.assertNotEqual(edit_titile, edit_titile_)

    def test_view_post_new(self):
        user = User.objects.get(username='test_user')
        author = user.get_username()

        self.client.force_login(user)
        resp = self.client.post('/post/new/', {'author': author, 'title': 'test4', 'text': 'text4', 'published': False})
        self.assertEqual(resp.status_code, 302)

        new_post = Post.objects.get(title='test4')
        pk = str(new_post.pk)
        resp_ = self.client.get('/post/'+pk+'/')
        self.assertEqual(resp_.status_code, 200)

    def test_view_post_list(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_list.html')
        self.assertEqual(resp.resolver_match.func, views.post_list)

        post1 = Post.objects.get(pk=1)
        post2 = Post.objects.get(pk=2)
        post3 = Post.objects.get(pk=3)

        if post1 and post2 and post3 in Post.objects.all():
            pass
        else:
            print('no necessary facilities')

    def test_view_post_delete(self):
        user = User.objects.get(username='test_user')

        self.client.force_login(user)
        resp = self.client.get('/post/2/')
        self.assertEqual(resp.status_code, 200)
        resp_ = self.client.post('/post/2/delete/')
        self.assertEqual(resp_.status_code, 302)

        resp_del = self.client.get('/post/2/')
        self.assertEqual(resp_del.status_code, 404)

    def test_view_post_detail(self):
        user = User.objects.get(username='test_user')

        self.client.force_login(user)
        resp = self.client.get('/post/3/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_detail.html')

    def test_view_post_no_show(self):
        user = User.objects.get(username='test_user')

        self.client.force_login(user)
        resp = self.client.get('/no_show/')
        self.assertEqual(resp.status_code, 200)

        resp_ = self.client.get('/exit/')
        self.assertEqual(resp_.status_code, 302)
        resp_no = self.client.get('/no_show/')
        self.assertEqual(resp_no.status_code, 401)







