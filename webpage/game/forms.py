from django import forms

# Formulaire envoyer dans le frontend pour creer une game, prend les donnees json[]
# Formulaire cree dans game/views
# Pas a jour (IMGE comme ref)
#COLLE
class GameCreationForm(forms.Form):
#    your_name = forms.CharField(label="Your name", max_length=100)
    game_mode = forms.CharField(label='game_mode', max_length=10, required=True)
    game_type = forms.CharField(label='game_type', max_length=10, required=True)

    # If game is tournament, this is the id of the specific tournament to join, else it is id of specific game to join.
    event_id = forms.CharField(label='event_id', max_length=10)
