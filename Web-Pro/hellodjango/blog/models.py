from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=70)
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='修改时间')

    excerpt = models.CharField(verbose_name='摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
    
    def save(self, *args, **kwargs):
        # 没有使用字段约束 auto_now 主要是为了后期修改更新时间方便
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
