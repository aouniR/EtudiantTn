from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date =  models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/')
    is_featured = models.BooleanField(default=False)
    is_main_article = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
