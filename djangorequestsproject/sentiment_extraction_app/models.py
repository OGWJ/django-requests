from django.db import models

class QueryRecord(models.Model):

    query = models.CharField(max_length=500, primary_key=True)
    last_updated = models.DateField()

    def __str__(self):
        return f'Query: {self.query} (last updated {self.last_updated})'


class SentimentRecord(models.Model):

    query = models.ForeignKey(QueryRecord, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self):
        return f'Query: {self.query}\nDate: {self.date}\nScore: {self.score}'
