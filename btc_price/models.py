from django.db import models

# This model will hold accepted hased API keys
class ApiKey(models.Model):
    hashed_key = models.CharField(max_length=255)
    invalid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.hashed_key

# This model will hold logged prices
class Price(models.Model):
    pair = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=25, decimal_places=8)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.pair, self.value)