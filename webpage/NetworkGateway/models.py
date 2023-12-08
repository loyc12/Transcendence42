from django.db import models

# Create your models here.

class GameEvent:
    def __init__(self, playerID: int=0, ev_type: str=None, key=None):
        self.id = playerID
        self.type = ev_type
        self.key = key