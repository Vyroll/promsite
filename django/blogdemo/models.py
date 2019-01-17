from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    creator = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=280)

    def __str__(self):
        return self.text[:30]