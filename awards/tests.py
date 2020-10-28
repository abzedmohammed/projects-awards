from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from .models import *
import datetime as dt

class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testusereres', password='12345')
        
        self.profile = Profile(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
                
    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))
        
class FollowTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        
        Follow.objects.create(follower=user, following=user)
        
        self.follower = Follow(follower=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.follower,Follow))
        
    def tearDown(self):
        Follow.objects.all().delete()
        
class StreamTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='12345')
        screenshots = Screenshot(image_1='image.jpg', image_2='image.jpg', image_3='image.jpg')
        profile = Profile(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        post = Project(user=user, image='image.jpg', project_name='Simba', description='king', screenshots=screenshots, date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        self.stream = Stream(following=user, user=user, project=post, date='2012-09-04 06:00:00.000000-08:00')
        
        # self.following = Stream(following=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.stream,Stream))
 
class LikesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        screenshots = Screenshot(image_1='image.jpg', image_2='image.jpg', image_3='image.jpg')

        profile = Profile(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        post = Project(user=user, image='image.jpg', project_name='Simba', description='king', screenshots=screenshots, date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)        
        self.like = Likes(user=user, project=post)
        
        # self.user = Likes(user=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.like,Likes))
        
class CommentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        screenshots = Screenshot(image_1='image.jpg', image_2='image.jpg', image_3='image.jpg')
        profile = Profile(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        post = Project(user=user, image='image.jpg', project_name='Simba', description='king', screenshots=screenshots, date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        self.comment = Comment(comment='its testing!!!', profile=profile, date='2012-09-04 06:00:00.000000-08:00', project=post)
        # self.comment = Comment(comment='its testing!!!')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comment))
    
class TestProject(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        screenshots = Screenshot(image_1='image.jpg', image_2='image.jpg', image_3='image.jpg')
        profile = Profile(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        self.post_test = Project(user=user, image='image.jpg', project_name='Simba', description='king', screenshots=screenshots, date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)

    def test_instance(self):
        self.assertTrue(isinstance(self.post_test, Project))

    def test_delete_image(self):
        self.post_test.delete_image()
        image = Project.objects.all()
        self.assertTrue(len(image) == 0)

    def tearDown(self):
        Project.objects.all().delete()
      
