import django_filters
from django_filters import CharFilter
#from django_filters.groups import CombinedGroup

from .models import Organiser, UserAddress

class OrganiserFilter(django_filters.FilterSet):
    organisation_name = CharFilter(field_name='organisation_name', lookup_expr='icontains', label='Name der Organisation')
    city = CharFilter(field_name='user_address__ort', lookup_expr='icontains', label='Ort')
    class Meta:
        model = Organiser
        fields = []#['organisation_name', 'user_address__ort']
        #groups = [
        #    CombinedGroup(filters=['organisation_name', 'user_address__ort'], combine=operator.or_),
        #]
