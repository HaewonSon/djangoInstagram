from django.db import models
from djangogram.users import models as user_model

# 자주 사용하는 시간 클래스를 만들어두고 사용
class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta: # 이 클래스에 대해 테이블이 만들어지지 않도록 함
        abstract = True


class Post(TimeStamedModel):
    # 작성자 : 외래키 사용
    author = models.ForeignKey(
        user_model.User,
        null=True,
        on_delete=models.CASCADE,  # 외래키를 갖는 유저가 삭제되면 어떻게 처리될것인지 명시
        related_name='post_author'
    )
    image = models.ImageField(blank=False)
    caption = models.TextField(blank=False)
    image_likes = models.ManyToManyField(
        user_model.User,
        blank=True,
        related_name='post_image_likes'
    )

    def __str__(self):
        return f"{self.author}: {self.caption}"


class Comment(TimeStamedModel):
    author = models.ForeignKey(
        user_model.User,
        null=True,
        on_delete=models.CASCADE,  # 외래키를 갖는 유저가 삭제되면 어떻게 처리될것인지 명시
        related_name='comment_author'
    )
    post = models.ForeignKey(
        Post,
        null=False,
        on_delete=models.CASCADE,  # 외래키를 갖는 유저가 삭제되면 어떻게 처리될것인지 명시
        related_name='comment_post'
    )
    contents = models.TextField(blank=True)

    def __str__(self):
        return f"{self.author}: {self.contents}"



