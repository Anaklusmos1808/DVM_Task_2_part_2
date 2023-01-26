from django.contrib import admin
from .models import Quiz, Question, Answer, Marks_Of_User, CustomUser, NumericalAnswer, TrueFalseAnswer
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

admin.site.register(Quiz)

class AnswerInLine(admin.TabularInline):
    model = Answer

class NumericalAnswerInLine(admin.TabularInline):
    model = NumericalAnswer

class TrueFalseAnswerInLine(admin.TabularInline):
    model = TrueFalseAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine, NumericalAnswerInLine, TrueFalseAnswerInLine]

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Role',
            {
                'fields':(
                    'is_QM',
                    'is_QT',
                )
            }
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(NumericalAnswer)
admin.site.register(TrueFalseAnswer)
admin.site.register(Marks_Of_User)

