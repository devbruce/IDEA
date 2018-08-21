from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ModelAutoSNA(models.Model):
    isolated_node_on_off = (
        ("on", "On"),
        ("off", "Off")
    )
    layouts = (
        ("FR", "Fruchterman Reingold"),
        ("FA2", "ForceAtlas2"),
    )
    edge_remove_threshold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=2)
    node_num = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)], default=30)
    page_range = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=2)
    stop_words = models.CharField(max_length=100, blank=True)
    remove_isolated_node = models.CharField(max_length=5, default=True, choices=isolated_node_on_off)
    layout = models.CharField(max_length=25, default="FR", choices=layouts)
    fr_k = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    fr_iter = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)], default=50)
    fa2_1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=2)
    fa2_2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], default=100)
    fa2_iter = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)], default=50)
    keyword = models.CharField(max_length=20)

class ModelAutoWC(models.Model):
    page_range = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=3)
    stop_words = models.CharField(max_length=100, blank=True)
    keyword = models.CharField(max_length=20)

class ModelSNA(models.Model):
    isolated_node_on_off = (
        ("on", "On"),
        ("off", "Off")
    )
    layouts = (
        ("FR", "Fruchterman Reingold"),
        ("FA2", "ForceAtlas2"),
    )
    edge_remove_threshold = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)], default=2)
    node_num = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)], default=30)
    stop_words = models.CharField(max_length=100, blank=True)
    remove_isolated_node = models.CharField(max_length=5, default=True, choices=isolated_node_on_off)
    layout = models.CharField(max_length=25, default="FR", choices=layouts)
    fr_k = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    fr_iter = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)], default=50)
    fa2_1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=2)
    fa2_2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], default=100)
    fa2_iter = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)], default=50)
    text_input = models.TextField()

class ModelWC(models.Model):
    stop_words = models.CharField(max_length=100, blank=True)
    text_input = models.TextField()
