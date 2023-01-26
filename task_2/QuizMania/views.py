from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django_tables2.views import SingleTableView
from django_tables2.export.views import ExportMixin
from .tables import ResultsTable

from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory
from .decorators import QM_required, QT_required


def home(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "home.html", para)

def signup_redirect(request):
    messages.error(request, "The given email already has an account")
    return redirect('home')

@login_required(login_url = '/login')
@QT_required
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    if quiz.private == True:
        return render(request, "privatequiz.html", {'quiz':quiz})

    return render(request, "quiz.html", {'quiz': quiz})

def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data' : questions,
    })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def save_quiz_view(request, myid):
    if is_ajax(request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None
        
        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                if question.category == 'MCQ':
                    question_answers = Answer.objects.filter(question=q)
                    for a in question_answers:
                        if a_selected == a.content:
                            if a.correct:
                                score += quiz.positive_marks
                                correct_answer = a.content
                            else:
                                score -= quiz.negative_marks
                        else:
                            if a.correct:
                                correct_answer = a.content
                elif question.category == 'Numerical':
                    question_answers = NumericalAnswer.objects.filter(question=q)
                    for a in question_answers:
                        if a_selected == a.correct:
                                score += quiz.positive_marks
                                correct_answer = a.content
                            #else:
                                #score -= Quiz.objects.negative_marks
                        else:
                            if a.correct:
                                correct_answer = a.content

                        
                    marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})

        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)

        return JsonResponse({'passed': True, 'score': score, 'marks': marks})


def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method== "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        role = request.POST['role']
        

        if password != confirm_password:
            return redirect('/register')
                 
        
        user = CustomUser.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.role  = role
        user.save()

        if user.role == 'QM':
            user.is_QM = True
            user.is_QT = False

        if user.role == 'QT':
            user.is_QM = False
            user.is_QT = True
        
        #if user.role != 'QM' or 'QT':
            #return redirect('/register')

        user.save()
    
        return render(request, 'login.html')
    return render(request, "signup.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html")
    return render(request, "login.html")

def privatequiz(request, myid):
    pin = Quiz.pin.get(id=myid)
    quiz = Quiz.objects.get(id=myid)
    if request.method== "POST":
        input_pin = request.POST['input_pin']
    
    if pin != input_pin:
        return render(request, 'privatequiz.html')
    
    else:
        return render(request, 'quiz.html', {'quiz': quiz})


def Logout(request):
    logout(request)
    return redirect('/')

@QM_required
def add_quiz(request):
    if request.method=="POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            obj = form.instance
            return render(request, "add_quiz.html", {'obj': obj})

    else:
        form=QuizForm()
    return render(request, "add_quiz.html", {'form': form})

@QM_required
def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_question.html")
    else:
        form=QuestionForm()
    return render(request, "add_question.html",  {'form': form, 'questions': questions})

@QM_required
def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "delete_question.html", {'question': question})

@QM_required
def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content', 'correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            save_status = True
            return render(request, "add_options.html", {'save_status': save_status})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_options.html", {'formset': formset, 'question': question})

@QM_required
def add_integer(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, NumericalAnswer, fields=('correct', 'question'))
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            save_status = True
            return render(request, "add_integer.html", {'save_status': save_status})
    else:
        formset = QuestionFormSet(instance=question)
    return render(request, "add_integer.html", {'formset': formset, 'question': question})

@QM_required
def add_boolean(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, TrueFalseAnswer, fields=('correct', 'question'))
    
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            save_status = True
            return render(request, "add_boolean.html", {'save_status': save_status})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_boolean.html", {'formset': formset, 'question': question})



def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "results.html", {'marks': marks})



class ResultsList(ExportMixin, SingleTableView):
    model = Marks_Of_User
    table_class = ResultsTable
    export_name = 'Results'
    template_name = 'results_list.html'

def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/results')
    return render(request, "delete_result.html", {'marks': marks})

  
def leaderboard(request):
    leaders = Marks_Of_User.objects.all().order_by('-score')[:10]

    return render(request, 'leaderboard.html', {'leaders': leaders})


    
