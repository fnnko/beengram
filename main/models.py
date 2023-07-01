from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from datetime import timedelta




class User(AbstractUser):
    username = models.CharField("ユーザー名", max_length=20, unique=True)
    email = models.EmailField("メールアドレス", unique=True)
    profile = models.CharField(max_length=150)
    follow = models.ManyToManyField("User", related_name="followed")
    icon = models.ImageField(upload_to="icons/", blank=True)
    like = models.ManyToManyField("Post", related_name="liked_users")

    def __str__(self):
        return self.username

    @property
    def icon_url(self):
        if self.icon:
            return self.icon.url
        return static("main/img/default-icon.svg")


class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts"
    )
    img = models.ImageField(upload_to="posts/")
    note = models.CharField(max_length=300, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.post_date}"


class Comment(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE,related_name="comments"
    )
    text = models.CharField(max_length=150)
    published_date = models.DateTimeField(auto_now_add=True)
    
    def get_elapsed_time(self):
        delta = timezone.now() - self.published_date

        zero = timedelta()
        one_hour = timedelta(hours=1)
        one_day = timedelta(days=1)
        one_week = timedelta(days=5)

        if delta < zero:
            raise ValueError("未来の時刻です。")

        if delta < one_hour:
            return f"{delta.seconds // 60} 分前"
        
        elif delta < one_day:
            return f"{delta.seconds // 3600} 時間前"

        elif delta < one_week:
            return f"{delta.days} 日前"

        else:
            return self.published_date.strftime("%Y年%m月%d日")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

    # def __str__(self):
    #     return f"{self.user.username} → (self{self.post}) : {self.post_date}"

    
    