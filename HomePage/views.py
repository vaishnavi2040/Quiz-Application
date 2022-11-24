from ast import Pass
from unittest import result
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from. models import Question, Subject, feedback, loginuser,NewUser,Quiz,TakenQuiz,Result,Answer,Student
from django.db.models import Count, Sum
from django.http import JsonResponse
import mysql.connector as db
import mysql
from django.db import IntegrityError
from django.db import transaction
from mysql import connector
from operator import itemgetter
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth import get_user_model as us
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import TakeQuizForm,QuestionForm,AnswersFormSet
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import (
    CreateView, UpdateView
)
from .filters import UserFilter
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import unauthenticated_user,allowed_users,unauthenticated_staff
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# from .auth_backend import PasswordlessAuthBackend as au





# Create your views here.

def index(request):
    return render(request ,"index.html")


def log_out(request):
    logout(request)
    # messages.info(request,"you are logged out now")
    return redirect('index')


@unauthenticated_user
def log_in(request):
    
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('main-view')

                    # if user.is_active==True and user.user_role =="Student":
                    #     # messages.info(request, f"You are now logged in as {username}")
                    #     return redirect('main-view')
                    #     # return render(request, "dashboard_student.html")
                    # elif (user.is_active==True and user.user_role=="Staff" ) or (user.is_active==True and user.user_role=='Staff' and user.is_superuser==True):
                    #     return redirect('home_view')
                    
                    # # elif (user.is_active & user.user_role=='Admin' & user.is_superuser==True) :
                    # #     return render(request, "dashboard_admin.html")

                else:
                    messages.error(request, "Invalid username or password.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
        form = AuthenticationForm()
        return render(request = request,
                    template_name = "newlogin.html",
                    context={"form":form})





@login_required(login_url='login')
class QuizListView(ListView):
    model=Quiz
    template_name='quizList.html'


@login_required(login_url='login')
def quiz_List(request):
    quiz=Quiz.objects.filter(is_active=True)
    
    # page = request.GET.get('page', 1)
    # paginator = Paginator(qu, 4)
    # try:
    #     quiz = paginator.page(page)
    # except PageNotAnInteger:
    #     quiz = paginator.page(1)
    # except EmptyPage:
    #     quiz = paginator.page(paginator.num_pages)  

    # context={}
    
    # student=UserFilter(request.GET, queryset= NewUser.objects.filter(user_role="Student"))
    # context={'student':student}
    # context['quiz']=quiz
    return render(request, "quizList.html",{'quiz': quiz})

@login_required(login_url='login')
def quiz_View(request,pk):
    quiz=Quiz.objects.get(pk=pk)
    return render(request, "quiz.html",{'obj': quiz})
    # return render(request, "dashboard_student.html",{'quizs': quizs})
    # return render(request, "dashboard_student.html")


@login_required(login_url='login')
def quiz_data_view(request,pk):
    quiz=Quiz.objects.get(pk=pk)
    

    questions=[]
    for q in quiz.get_questions():
        answers=[]
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q):answers})
    return JsonResponse({

        'data':questions,
        'time':quiz.time,
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='login')
def save_quiz_view(request, pk):
    
        if is_ajax(request):
            questions = []
            data = request.POST
            data_ = dict(data.lists())

            data_.pop('csrfmiddlewaretoken')

            for k in data_.keys():
                print('key: ', k)
                question = Question.objects.get(text=k)
                questions.append(question)
            print(questions)

            user = request.user
            quiz = Quiz.objects.get(pk=pk)
            Stud=Student.object.get(user=request.user)
            Stud.quizzes=quiz


            score = 0
            multiplier = 100 / quiz.no_of_question
            results = []
            correct_answer = None

            for q in questions:
                a_selected = request.POST.get(q.text)

                if a_selected != "":
                    question_answers = Answer.objects.filter(question=q)
                    for a in question_answers:
                        if a_selected == a.text:
                            if a.correct:
                                score += 1
                                correct_answer = a.text
                        else:
                            if a.correct:
                                correct_answer = a.text

                    results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
                else:
                    results.append({str(q): 'not answered'})
                
            score_ = score * multiplier
            Result.objects.create(quiz=quiz, user=user, score=score_)
            Stud.score=score_

        
            return JsonResponse({'score': score_, 'results': results})
        
                    # return render(request, "feedback.html",{'user': user})

        # if score_ >= quiz.required_score_to_pass:
        #     return JsonResponse({'passed': True, 'score': score_, 'results': results})
        # else:
        #     return JsonResponse({'passed': False, 'score': score_, 'results': results})

@login_required(login_url='login')
def feedback_view(request,pk):
    # return render(request, "feedback.html" ,{{'pk':pk}})
    quiz=Quiz.objects.get(pk=pk)
    return render(request, "feedback.html",{'obj': quiz})


@login_required(login_url='login')
def save_feedback_view(request,pk):
    if request.method == 'POST':
        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        
        feed=request.POST.get('feedback_area')
        en=feedback(quiz=quiz, user=user, feedback=feed)
        en.save()
    return redirect("main-view")







# STAFFF SECTION

@unauthenticated_staff
def log_in_staff(request):
    
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home_view')

                    # if user.is_active==True and user.user_role =="Student":
                    #     # messages.info(request, f"You are now logged in as {username}")
                    #     return redirect('main-view')
                    #     # return render(request, "dashboard_student.html")
                    # elif (user.is_active==True and user.user_role=="Staff" ) or (user.is_active==True and user.user_role=='Staff' and user.is_superuser==True):
                    #     return redirect('home_view')
                    
                    # # elif (user.is_active & user.user_role=='Admin' & user.is_superuser==True) :
                    # #     return render(request, "dashboard_admin.html")

                else:
                    messages.error(request, "Invalid username or password.")
                    return redirect('login_staff')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login_staff')
        form = AuthenticationForm()
        return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

def log_out_staff(request): 
    logout(request)
    # messages.info(request,"you are logged out now")
    return redirect('index')


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def staff_home(request):
    cs=NewUser.objects.filter(user_role="Student").count()
    cr=Result.objects.all().count()
    cquiz=Quiz.objects.all().count()
    cq=Question.objects.all().count()
    cf=feedback.objects.all().count()
    print(cs)
    context={'student':cs,'result':cr,'quiz':cquiz,'ques':cq,'fed':cf}
    return render(request,'dashboard_staff.html',context=context)


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def studentList(request):
    
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(Full_Name__icontains=q) | Q(username__icontains=q) | Q(College_Name__icontains=q) | Q(Course__icontains=q) | Q(Semester__icontains=q)  )
        stud= NewUser.objects.filter(multiple_q , user_role="Student")

    else:
        stud=NewUser.objects.filter(user_role="Student") 

    
    page = request.GET.get('page', 1)
    paginator = Paginator(stud, 5)
    try:
        student = paginator.page(page)
    except PageNotAnInteger:
        student = paginator.page(1)
    except EmptyPage:
        student = paginator.page(paginator.num_pages)  

    context={}
    
    # student=UserFilter(request.GET, queryset= NewUser.objects.filter(user_role="Student"))
    # context={'student':student}
    context['student']=student
    return render(request,'view_studentList_staff.html',context=context)


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def student_add(request):
    if request.method=="POST":
        name=request.POST.get('name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        college_name=request.POST.get('college_name')
        course=request.POST.get('course')
        semester=request.POST.get('semester')
        new_user=NewUser.objects.create_user(username=username,password=password,
        Full_Name=name,College_Name=college_name,
        Course=course,
        user_role="Student",
        Semester=semester,
        )
    return redirect('student_List')



@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def student_edit(request):
    student=NewUser.objects.filter(user_role="Student")
    context={'student':student}
    return render(request,'view_studentList_staff.html',context)



@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def student_update(request,id):
    if request.method=="POST":
        name=request.POST.get('name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        college_name=request.POST.get('college_name')
        course=request.POST.get('course')
        semester=request.POST.get('semester')

        new_user=NewUser.objects.create_user(id=id,username=username,password=password,
        Full_Name=name,College_Name=college_name,
        Course=course,
        user_role="Student",
        Semester=semester,
        )
        return redirect('student_List')



@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def student_delete(request,id):
    stud=NewUser.objects.filter(id=id,user_role="Student")
    stud.delete()
    # context={'student':student}
    return redirect('student_List')


    
    


#Results

@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def ResultList(request):
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(user__Full_Name__icontains=q) | Q(user__username__icontains=q) | Q(user__College_Name__icontains=q) | Q(quiz__name__icontains=q) | Q(quiz__topic__icontains=q)| Q(score__icontains=q)  )
        res= Result.objects.filter(multiple_q)

    else:
        res=Result.objects.all()

    # order_by = request.GET.get('order_by', 'score')
    # res.order_by(order_by)
    page = request.GET.get('page', 1)
    paginator = Paginator(res, 5)
    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        res = paginator.page(paginator.num_pages)  

    
    context={"result":res}
    return render(request,'view_result_staff.html',context) 

#feedback
@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def feedbackList(request):
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(user__Full_Name__icontains=q) | Q(user__username__icontains=q) | Q(user__College_Name__icontains=q) | Q(quiz__name__icontains=q) | Q(quiz__topic__icontains=q) | Q(feedback__icontains=q) )
        fed= feedback.objects.filter(multiple_q)

    else:
       fed=feedback.objects.all()
    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(fed, 5 )
    try:
        fed = paginator.page(page)
    except PageNotAnInteger:
        fed = paginator.page(1)
    except EmptyPage:
        fed = paginator.page(paginator.num_pages)  

    
    context={"feedback":fed}
    return render(request,'view_feedback_staff.html',context) 

    

#quizListStaff,quiz_add,quiz_edit,quiz_update,quiz_delete
@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def quizListStaff(request):
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(name__icontains=q) | Q(topic__icontains=q) | Q(difficulty__icontains=q) | Q(no_of_question__icontains=q) | Q(time__icontains=q)| Q(is_active__icontains=q)  )
        quiz= Quiz.objects.filter(multiple_q)

    else:
        quiz=Quiz.objects.all()
    
     
    page = request.GET.get('page', 1)
    paginator = Paginator(quiz, 10)
    try:
        quiz = paginator.page(page)
    except PageNotAnInteger:
        quiz = paginator.page(1)
    except EmptyPage:
        quiz = paginator.page(paginator.num_pages)  

    
    context={'quiz':quiz}
    return render(request,'view_Quizes_staff.html',context)


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def quiz_add(request):
        if request.method=="POST":
            name=request.POST.get('name')
            topic=request.POST.get('topic')
            time=request.POST.get('time')
            difficulty=request.POST.get('difficulty')
            no_of_question=request.POST.get('no_of_question')
            active_status=request.POST.get('active')
            print (type(active_status))
            if active_status == 'true':
                active_status = True
            else:
                active_status = False

            new_quiz=Quiz(name=name,topic=topic,
            time=time,difficulty=difficulty,
            no_of_question=no_of_question,
            is_active=active_status,
            
            )
            new_quiz.save()
        return redirect('quiz_List_staff') 


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def quiz_edit(request):
    quiz=Quiz.objects.all()
    context={'quiz':quiz}
    return render(request,'view_Quizes_staff.html',context) 


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def quiz_update(request,id):
    if request.method=="POST":
            name=request.POST.get('name')
            topic=request.POST.get('topic')
            time=request.POST.get('time')
            difficulty=request.POST.get('difficulty')
            no_of_question=request.POST.get('no_of_question')
            active_status=request.POST.get('active')
            print ((active_status))
            print("hello")
            if active_status == 'true':
                active_status = True
            else:
                active_status = False

            new_quiz=Quiz(id=id,name=name,topic=topic,
            time=time,difficulty=difficulty,
            no_of_question=no_of_question,
            is_active=active_status,
            
            )
            new_quiz.save()
    return redirect('quiz_List_staff') 


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])    
def quiz_delete(request,id):
    quiz=Quiz(id=id)
    quiz.delete()
    # context={'student':student}
    return redirect('quiz_List_staff')




# questionListStaff,question_add,question_edit,question_update,question_delete


@login_required(login_url='login_staff')
@allowed_users(allowed_roles=['Admin','Staff'])
def questionListStaff(request):
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(text__icontains=q) | Q(quiz__name__icontains=q) | Q(quiz__difficulty__icontains=q) | Q(quiz__topic__icontains=q) )
        data= Question.objects.filter(multiple_q)

    else:
        data=Question.objects.all()

    
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)  


    context={'data':data}
    return render(request,'view_questions_staff.html',context) 


# def question_add(request):
#     if request.method == "POST":
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('question_List_staff')
#     else:
#         form=QuestionForm()
#         return render(request,"add_questions_staff.html",{'form':form})

def question_edit(request):
    pass

def question_update(request):
    pass

def question_delete(request,id):
    q=Question(id=id)
    q.delete()
    # context={'student':student}
    return redirect('question_List_staff')




# class QuestionCreateView(CreateView):
#     form_class = QuestionForm
#     template_name = 'test_ques.html'
#     def get_context_data(self, **kwargs):
#         context = super(QuestionCreateView, self).get_context_data(**kwargs)
#         context['answers_formset'] = AnswersFormSet()
#         return context
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         answers_formset = AnswersFormSet(self.request.POST)
#         if form.is_valid() and answers_formset.is_valid():
#             return self.form_valid(form, answers_formset)
#         else:
#             return self.form_invalid(form, answers_formset)
#     def form_valid(self, form, answers_formset):
#         self.object = form.save(commit=False)
#         self.object.save()
#         # saving ProductMeta Instances
#         answers = answers_formset.save(commit=False)
#         for ans in answers:
#             ans.question = self.object
#             ans.save()
#         return redirect(reverse("question_List_staff"))
#     def form_invalid(self, form, answers_formset):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   answers_formset=answers_formset
#                                   )
#         )


# class QuestionCreateView(CreateView):
#     model = Question
#     template_name = 'add_questions_staff.html'
#     form_class = QuestionForm
#     object = None

#     def get(self, request, *args, **kwargs):
#         """
#         Handles GET requests and instantiates blank versions of the form
#         and its inline formsets.
#         """
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         question_answer_form = AnswersFormSet()
#         return self.render_to_response(
#                   self.get_context_data(form=form,
#                                         question_answer_form=question_answer_form,
#                                         )
#                                      )

#     def post(self, request, *args, **kwargs):
#         """
#         Handles POST requests, instantiating a form instance and its inline
#         formsets with the passed POST variables and then checking them for
#         validity.
#         """
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         question_answer_form = AnswersFormSet(self.request.POST)
#         if form.is_valid() and question_answer_form.is_valid():
#             return self.form_valid(form, question_answer_form)
#         else:
#             return self.form_invalid(form, question_answer_form)

#     def form_valid(self, form, question_answer_form):
#         """
#         Called if all forms are valid. Creates Assignment instance along with the
#         associated AssignmentQuestion instances then redirects to success url
#         Args:
#             form: Assignment Form
#             assignment_question_form: Assignment Question Form

#         Returns: an HttpResponse to success url

#         """
#         self.object = form.save(commit=False)
#         # pre-processing for Assignment instance here...
#         self.object.save()

#         # saving AssignmentQuestion Instances
#         question_answer = question_answer_form.save(commit=False)
#         for aq in question_answer:
#             #  change the AssignmentQuestion instance values here
#             #  aq.some_field = some_value
#             aq.save()

#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, question_answer_form):
#         """
#         Called if a form is invalid. Re-renders the context data with the
#         data-filled forms and errors.

#         Args:
#             form: Assignment Form
#             assignment_question_form: Assignment Question Form
#         """
#         return self.render_to_response(
#                  self.get_context_data(form=form,
#                                        question_answer_form=question_answer_form
#                                        )
#         )



















class QuestionInline():
    form_class = QuestionForm
    model = Question
    template_name = "add_questions_staff.html"
    
 
    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('question_List_staff')

    
    

    
    def formset_answers_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        answers = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for answer in answers:
            answer.question = self.object
            answer.save()








@method_decorator(login_required(login_url="login_staff"),
                  name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Admin','Staff']), name='dispatch')
class QuestionCreate(QuestionInline, CreateView):

    
    def get_context_data(self, **kwargs):
        ctx = super(QuestionCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                
                'answers': AnswersFormSet(prefix='answers'),
            }
        else:
            return {
                # 'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                'answers': AnswersFormSet(self.request.POST or None, self.request.FILES or None, prefix='answers'),
            }



@method_decorator(login_required(login_url="login_staff"),
                  name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Admin','Staff']), name='dispatch')
class QuestionUpdate(QuestionInline, UpdateView):
    
    
    def get_context_data(self, **kwargs):
        ctx = super(QuestionUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

   
    def get_named_formsets(self):
        return {
            # 'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
            'answers': AnswersFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='answers'),
        }

# views.py

@allowed_users(allowed_roles=['Admin','Staff'])
@login_required(login_url="login_staff")
def delete_answer(request, pk):
    try:
        answer = Answer.objects.get(id=pk)
    except Answer.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_question', pk=answer.question.id)

    answer.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('update_question', pk=answer.question.id)















# def quiz_Questions(request,id):
#     quiz=get_object_or_404(Quiz, id=id)
#     student = request.user.student
#     questions=Question.objects.all()
#     # questi ons=Question.objects.filter(subject = quiz.subject , difficulty=quiz.difficulty)
#     print(questions)
#     total_questions = questions.count()
#     unanswered_questions = student.get_unanswered_questions(quiz)
#     total_unanswered_questions = unanswered_questions.count()
#     # if request.method == 'POST':
#     #     form = TakeQuizForm(question=questions, data=request.POST)
#     #     if form.is_valid():
#     #         with transaction.atomic():
#     #             student_answer = form.save(commit=False)
#     #             student_answer.student = student
#     #             student_answer.save()
#     #             if student.get_unanswered_questions(quiz).exists():
#     #                 return redirect('students:take_quiz', id)
#     #             else:
#     #                 correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
#     #                 percentage = round((correct_answers / total_questions) * 100.0, 2)
#     #                 TakenQuiz.objects.create(student=student, quiz=quiz, score=correct_answers, percentage= percentage)
#     #                 student.score = TakenQuiz.objects.filter(student=student).aggregate(Sum('score'))['score__sum']
#     #                 student.save()
#     #                 messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, percentage))
                    
#     #                 return redirect('students:student_quiz_results', id)
#     # else:
#     #     form = TakeQuizForm(question=questions)


#     return render(request, 'students/take_quiz_form.html', {
#         'quiz': quiz,
#         'question': questions,
#         'answered_questions': total_questions - total_unanswered_questions,
#         'total_questions': total_questions
#     })




    




