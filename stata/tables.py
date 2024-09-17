import django_tables2 as tables
from django.db.models import F
from django.db.models.functions import Round

from .models import Activities


class ActivitiesTable(tables.Table):
    class Meta:
        model = Activities
        template_name = "django_tables2/bootstrap4.html"
        exclude = ('id',)

    distance = tables.Column()
    name = tables.Column(orderable=False)
    average_speed = tables.Column()
    location = tables.Column(orderable=False)

    def render_distance(self, value):
        return round(value / 1000, 2)

    def render_average_speed(self, value):
        return round(value * 3.6, 2)

    # def get_queryset(self):
    #     return Activities.objects.order_by('-date').annotate(
    #         distance_km=
    #         Round(F('distance') / 1000),
    #         average_speed_km_h=
    #         Round(F('average_speed') * 3.6)
    #     )
