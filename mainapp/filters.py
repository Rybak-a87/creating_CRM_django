from django_filters import FilterSet

from .models import Interaction


class InteractionFilter(FilterSet):
    class Meta:
        model = Interaction
        fields = ("project", "company", "manager")


def custom_search(words, objects):
    """
    функция поиска ключевых слов с описании взаимодействия
    """
    result = []
    for word in words.split():
        for obj in objects:
            if word in obj.about:
                result.append(obj)
    return result
