from django.db import models

# Create your models here.
class Entry(models.Model):
    """A Entry that user is gonna write about"""
    topic=models.CharField(max_length=200)
    content=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """Returns a string Representation of the model"""
        return self.topic





