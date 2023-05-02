from django.db import models
from authentication.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Post(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField(Hashtag)
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Check if the current instance is new or existing
        is_new = self.pk is None
        # Save the current instance
        super(Post, self).save(*args, **kwargs)
        # If the current instance is new
        if is_new:
            # Count the number of posts associated with the user
            # and update user's total_posts attribute
            self.user.total_posts = self.user.post_set.count()
            # Save the updated user object to the database
            self.user.save()

    def __str__(self):
        return str(self.id)


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=1, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.total_likes += self.likes
        self.post.save()

    def __str__(self):
        return f"{self.user} liked {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count_comment = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.total_comments += self.count_comment
        self.post.save()

    def __str__(self):
        return f"{self.user} commented on {self.post}: {self.content}"
