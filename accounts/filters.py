import django_filters
from django_filters import CharFilter
from .models import Organiser, UserAddress


class OrganiserFilter(django_filters.FilterSet):
    # Maybe add that later:
    # organisation_name = CharFilter(field_name='organisation_name', lookup_expr='icontains', label='Name der Organisation')
    city = CharFilter(field_name='user_address__ort', lookup_expr='icontains', label='Ort')
    class Meta:
        model = Organiser
        fields = []
