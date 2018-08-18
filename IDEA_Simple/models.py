from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ModelAutoSNA(models.Model):
    edge_remove_threshold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    node_num = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)], default=50)
    page_range = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=3)
    stop_words = models.CharField(max_length=30, blank = True)
    keyword = models.CharField(max_length=20)

class ModelAutoWC(models.Model):
    shapes = (
        ("default", "Circle"),
        ("square", "Square"),
        ("star", "Star"),
    )
    bg_colors = (
        ("white", "White"),
        ("black", "Black"),
        ("red", "Red"),
        ("blue", "Blue"),
        ("green", "Green"),
        ("yellow", "Yellow"),
        ("purple", "Purple"),
        ("gray", "Gray"),
    )
    max_word_size = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(300)], default=100)
    bg_color = models.CharField(max_length=10, default="white", choices = bg_colors)
    shape = models.CharField(max_length=10, default="default", choices = shapes)
    page_range = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=3)
    stop_words = models.CharField(max_length=30, blank = True)
    keyword = models.CharField(max_length=20)

class ModelSNA(models.Model):
    edge_remove_threshold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=0)
    node_num = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)], default=50)
    stop_words = models.CharField(max_length=30, blank = True)
    text_input = models.TextField()

class ModelWC(models.Model):
    shapes = (
        ("default", "Circle"),
        ("square", "Square"),
        ("star", "Star"),
    )
    bg_colors = (
        ("white", "White"),
        ("black", "Black"),
        ("red", "Red"),
        ("blue", "Blue"),
        ("green", "Green"),
        ("yellow", "Yellow"),
        ("purple", "Purple"),
        ("gray", "Gray"),
    )
    max_word_size = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(300)], default=100)
    bg_color = models.CharField(max_length=10, default="white", choices = bg_colors)
    shape = models.CharField(max_length=10, default="default", choices = shapes)
    stop_words = models.CharField(max_length=30, blank = True)
    text_input = models.TextField()