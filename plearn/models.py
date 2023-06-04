from django.db import models
from django.contrib.auth.models import User, Group
from ckeditor.fields import RichTextField

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=255, null=True)
    content = RichTextField(blank=True, null=True)
    video = models.CharField(max_length=999, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def NumberOfDiscussions(self):
        return Discussion.objects.filter(section = self).count()
    
    def NumberOfReplies(self):
        discussions = Discussion.objects.filter(section = self)
        return Reply.objects.filter(discussion__in = discussions).count()

class Discussion(models.Model):
    message = models.CharField(max_length=999, null=True)
    date = models.DateField(null=True)
    learner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message}"

    def NumberOfReplies(self):
        return Reply.objects.filter(discussion = self).count()

    def getRepliedUsers(self):
        return User.objects.filter(id__in = Reply.objects.filter(discussion = self).values('editor'))



class Reply(models.Model):
    response = models.CharField(max_length=999,null=True)
    date = models.DateField(null=True)
    editor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)