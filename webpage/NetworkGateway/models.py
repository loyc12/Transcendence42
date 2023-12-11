from django.db import models

# Create your models here.

class GameEvent:
    def __init__(self, playerID: int=0, ev_type: str=None, key=None):
        self.id = playerID
        self.type = ev_type
        self.key = key

    def __repr__(self) -> str:
        return f"GameEvent<id: {self.id}, type: {self.type}, key: {self.key}>"