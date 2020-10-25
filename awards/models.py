from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from phone_field import PhoneField
from django.dispatch import receiver
import uuid

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.profile.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    job_title = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=120, null=True)
    avatar = CloudinaryField('image')
    whatsapp = PhoneField(blank=True, null=True)
    facebook = models.URLField(max_length=250, null=True, blank=True)
    linkedin = models.URLField(max_length=250, null=True, blank=True)
    twitter = models.URLField(max_length=250, null=True, blank=True)
    github = models.URLField(max_length=250, null=True, blank=True)
    skills = TaggableManager(blank=True)
    
    def __str__(self):
        return self.user.username
    
    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)
        
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    image = models.ImageField(upload_to=user_directory_path, verbose_name='project_pic', null=True)
    project_name = models.CharField(max_length=120, null=True)
    description = models.TextField(max_length=1000, verbose_name='project_description', null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_profile')
    like = models.IntegerField(default=0)
    #tags = TaggableManager(blank=True)
    
    # class Meta:
    #     ordering = ['-date',]
    
    def __str__(self):
        return self.project_name
    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_projects(cls,search_term):
        posts = Project.objects.filter(project_name__name__icontains=search_term)
        return posts
        
    def delete_image(self):
        self.delete()  
        
class Screenshot(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE)
    image_1 = models.FileField(upload_to='images/', verbose_name='pics', null=True)  
    image_2 = models.FileField(upload_to='image_2/', verbose_name='pics_2', null=True)  
    image_3 = models.FileField(upload_to='image_3/', verbose_name='pics_3', null=True)  
    def __str__(self):
        return self.project.project_name
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def add_project(sender,instance,*args,**kwargs):
        project = instance
        user = project.user
        followers = Follow.objects.all().filter(following=user)
        
        for follower in followers:
            stream = Stream(project=project, user=follower.follower, date=project.date, following=user)
            stream.save()
            
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='post_like')

class Comment(models.Model):
    comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='post_comment')
            
post_save.connect(Stream.add_project, sender=Project)
    

