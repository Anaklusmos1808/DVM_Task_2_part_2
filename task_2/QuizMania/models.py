from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_QM = models.BooleanField(default=False)
    is_QT = models.BooleanField(default=False)



class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    number_of_questions = models.IntegerField(default=1)
    positive_marks = models.IntegerField(default=1)
    negative_marks = models.IntegerField(default=0)
    private = models.BooleanField(default=False)
    pin = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    
    def get_questions(self):
        return self.question_set.all()

class Question(models.Model):
    content = models.CharField(max_length=300)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default='MCQ')
    
    
    def __str__(self):
        return self.content

    def get_answers(self):
        return self.answer_set.all()
    
class Answer(models.Model):
    content = models.CharField(max_length=300)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"


class NumericalAnswer(models.Model):
    correct = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE )

    def __str__(self):
        return f"question: {self.question.content}, correct: {self.correct}"


class TrueFalseAnswer(models.Model):
    option_1 = models.CharField(max_length=100, default='True', editable=False)
    option_2 = models.CharField(max_length=100, default='False', editable=False)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.content}, True: {self.option_1}, False: {self.option_2}, correct:{self.correct}"

    



class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)
        