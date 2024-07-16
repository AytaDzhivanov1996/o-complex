from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    query_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    
class SearchHistory(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)