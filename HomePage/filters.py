import django_filters
from .models import NewUser,Result,Question,Quiz,feedback

class UserFilter(django_filters.FilterSet):

    class Meta:
        model=NewUser
        fields=['Full_Name','username','College_Name','Course','Semester']