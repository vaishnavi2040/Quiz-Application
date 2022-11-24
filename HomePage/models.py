
from email.policy import default
from enum import unique
from pyexpat import model
from socketserver import StreamRequestHandler
from tabnanny import verbose
from time import timezone
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import datetime

# from formatter import NullFormatter
from .managers import CustomUserManager


# Create your models here.
class NewUser(AbstractUser):

    CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Student', 'Student'),
        
    ]
    email=None
    Full_Name= models.CharField(max_length=100,blank=True)
    College_Name=models.CharField(max_length=100,blank=True)
    Roll_No= models.CharField(max_length=10,blank=True)
    Course =models.CharField(max_length=100,blank=True)
    Semester=models.CharField(max_length=100,blank=True)
    user_role=models.CharField(max_length=100,choices=CHOICES,default='Student')

    

    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ['user_role',]

    objects=CustomUserManager()
    def __str__(self):
       return self.username




class Subject(models.Model):
    name = models.CharField(max_length=30)
    # color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name



class Quiz(models.Model):
    options=[('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),]
    # owner = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time=models.IntegerField(help_text="duration of the quiz in minutes")
    difficulty=models.CharField(max_length=50,choices=options)
    no_of_question=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.no_of_question]
    
    class Meta:
        verbose_name_plural='Quizes'
    
      


class Question(models.Model):
    options=[('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),]
    
    text = models.TextField('Question Text')
    # difficulty=models.CharField(max_length=50,choices=options)
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,default=1,help_text="Choose Quiz")
    # created=models.DateTimeField(auto_now_add=True,blank=True,null=True)


    
   
    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all()
    
    
    
    def get_quiz_name(self):
        return self.quiz.name
    
    def get_quiz_topic(self):
        return self.quiz.topic

    def get_quiz_difficulty(self):
        return self.quiz.difficulty
    

    


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField('Correct answer', default=False)
    # created=models.DateTimeField(auto_now_add=True,default=datetime.now(),null=True)

    def get_ques_name(self):
        return self.question.text

    def __str__(self):
        return f"{self.text}"

    # def __str__(self):
    #     return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"



class Result(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE, )
    user=models.ForeignKey(NewUser,on_delete=models.CASCADE, )
    score=models.FloatField()

    def __str__(self):
        return str(self.pk)

    def get_quiz_name(self):
        return self.quiz.name
    
    def get_quiz_topic(self):
        return self.quiz.topic

    def get_Full_Name(self):
        return self.user.Full_Name
    

    def get_College_Name(self):
        return self.user.College_Name

    def get_Registration_Name(self):
        return self.user.username
    
    


    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['quiz', 'user'], name='quiz_user'
            )
        ]

class feedback(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE )
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE, )
    feedback=models.TextField(max_length=300)

    def __str__(self):
        return f"user: {self.user.Full_Name}, quiz: {self.quiz}, feedback: {self.feedback[0:20]}"

    def get_Full_Name(self):
        return self.user.Full_Name
    

    def get_College_Name(self):
        return self.user.College_Name

    def get_Registration_Name(self):
        return self.user.username

    def get_quiz_name(self):
        return self.quiz.name
    
    def get_quiz_topic(self):
        return self.quiz.topic

    def get_feedback(self):
        return self.feedback[0:5]

   






class Student(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    # interests = models.ManyToManyField(Subject, related_name='interested_students')
    
    # User reputation score.
    score = models.IntegerField(default=0)
    

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField()
    percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    log_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

































# class NewUser(AbstractUser):

#     CHOICES = [
#         ('Admin', 'Admin'),
#         ('Staff', 'Staff'),
#         ('Student', 'Student'),
        
#     ]
    
    
#     Reg_Id=models.CharField(max_length=100,unique=True)
#     Full_Name= models.CharField(max_length=100,blank=True)
#     College_Name=models.CharField(max_length=100,blank=True)
#     Roll_No= models.CharField(max_length=10,blank=True)
#     Course =models.CharField(max_length=100,blank=True)
#     Semester=models.CharField(max_length=100,blank=True)
#     user_role=models.CharField(max_length=100,choices=CHOICES,default='Student')
#     is_staff=models.BooleanField(default=False)
#     is_active=models.BooleanField(default=False)
#     is_superuser=models.BooleanField(default=False)
#     is_admin=models.BooleanField(default=False)
#     date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
#     last_login=models.DateTimeField(verbose_name='last login',auto_now=True)

#     USERNAME_FIELD='username'
#     REQUIRED_FIELDS = ['user_role','College_Name','Reg_Id']

#     objects=CustomUserManager()
#     def __str__(self):
#        return self.Full_Name



class loginuser(models.Model):
    regid=models.IntegerField(primary_key=True)
    name= models.CharField(max_length=100)
    college_name=models.CharField(max_length=100)
    roll_no= models.IntegerField()
    course =models.CharField(max_length=100)
    Semester=models.CharField(max_length=100)



# class NewUser(AbstractUser):
#     username=None
#     regid=models.IntegerField(primary_key=True,unique=True,auto_created=True)
#     name= models.CharField(max_length=100,blank=True)
#     college_name=models.CharField(max_length=100,blank=True)
#     roll_no= models.IntegerField(default=0,blank=True)
#     course =models.CharField(max_length=100,blank=True)
#     Semester=models.CharField(max_length=100,blank=True)
#     user_role=models.CharField(max_length=100)
#     # is_staff=models.BooleanField(default=False)
#     # is_active=models.BooleanField(default=False)
#     # is_superuser=models.BooleanField(default=False)
#     # is_admin=models.BooleanField(default=False)
#     # date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
#     # last_login=models.DateTimeField(verbose_name='last login',auto_now=True)
    

#     USERNAME_FIELD='regid'
#     REQUIRED_FIELDS = ['user_role','college_name']
#     objects=CustomUserManager()

#     def __str__(self):
#         return self.name

   


# class Questions(models.Model):
#     q_id=models.IntegerField(primary_key=True,auto_created=True)
#     Question=models.CharField(max_length=100)
#     op1=models.CharField(max_length=50)
#     op2=models.CharField(max_length=50)
#     op3=models.CharField(max_length=50)
#     op4=models.CharField(max_length=50)
#     ans=models.CharField(max_length=50)
#     subject=models.CharField(max_length=50)



