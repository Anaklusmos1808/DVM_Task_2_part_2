import django_tables2 as tables
from .models import Marks_Of_User

class ResultsTable(tables.Table):
    export_formats = ['xls', 'xlsx']
    class Meta:
        model = Marks_Of_User
        fields = ('quiz', 'user', 'score')