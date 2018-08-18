from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ModelAutoSNA(models.Model):
    edge_remove_threshold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)], default=2)
    node_num = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)], default=50)
    page_range = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=3)
    stop_words = models.CharField(max_length=30, blank = True)
    keyword = models.CharField(max_length=20)

class ModelAutoWC(models.Model):
    page_range = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=3)
    stop_words = models.CharField(max_length=30, blank = True)
    keyword = models.CharField(max_length=20)

class ModelSNA(models.Model):
    edge_remove_threshold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=4)
    node_num = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)], default=50)
    stop_words = models.CharField(max_length=30, blank = True)
    text_input = models.TextField()

class ModelWC(models.Model):
    stop_words = models.CharField(max_length=30, blank = True)
    text_input = models.TextField()
