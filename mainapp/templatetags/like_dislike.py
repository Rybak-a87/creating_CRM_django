from django import template

from mainapp.models import RatingInteraction


register = template.Library()


@register.simple_tag(takes_context=True)    # takes_context=True - если нужен доступ к request
def is_liked(context, interaction_id):
    request = context["request"]
    try:
        interaction_likes = RatingInteraction.objects.get(
            interaction__id=interaction_id, manager_id=request.user.id
        ).like
    except Exception as ex:
        interaction_likes = False
    return interaction_likes


@register.simple_tag()
def count_likes(interaction_id):
    return RatingInteraction.objects.filter(interaction__id=interaction_id, like=True).count()


@register.simple_tag(takes_context=True)
def interaction_likes_id(context, interaction_id):
    request = context["request"]
    return RatingInteraction.objects.get(
        interaction__id=interaction_id, manager_id=request.user.id
    ).id
