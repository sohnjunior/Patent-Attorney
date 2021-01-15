from django.db import models


class CommonInfo(models.Model):
    app_num = models.CharField(max_length=64)
    app_name = models.CharField(max_length=64)
    agent_name = models.CharField(max_length=64)
    app_status = models.CharField(max_length=64)
    pub_date = models.CharField(max_length=64)
    pub_num = models.CharField(max_length=64)
    image_path = models.URLField()
    category = models.CharField(max_length=64, default='기타')

    class Meta:
        abstract = True


class MarkPatentInfo(CommonInfo):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.app_num


class DesignPatentInfo(CommonInfo):
    article_name = models.CharField(max_length=64)

    def __str__(self):
        return self.app_num

