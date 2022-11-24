from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Answer, NewUser, Question, Quiz, Result, Student

# Register your models here.

class login(admin.ModelAdmin):
    list_display=('regid','name','college_name')
    list_display_links=('regid','name','college_name')
    list_filter= ('regid','name','college_name')

class user(admin.ModelAdmin):
    list_display=('Reg_Id','Full_Name','College_Name')
    # list_display_links=('regid','name','college_name','is_staff')
    # list_filter= ('regid','name','college_name','is_staff')




class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = NewUser
    list_display = ('username','Full_Name','College_Name','Roll_No','user_role', 'is_staff', 'is_active',)
    list_filter = ('username','Full_Name','College_Name','Roll_No','user_role','is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password','user_role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
        ('Information', {'fields': ('Full_Name','College_Name','Roll_No')}),
         ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', )
        })

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','user_role', 'is_staff', 'is_active','Full_Name','College_Name','Roll_No',)}
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser', )}),
         ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions', )
        })
       
    )
    search_fields = ('username','Full_Name','College_Name')
    ordering = ('username',)

class results(admin.ModelAdmin):
    model=Result
    list_display=('get_name','get_Full_Name','get_College_Name','score')

    # list_display_links=('get_name','get_Full_Name','get_College_Name','score')
    list_filter=('quiz__name','user__Full_Name','user__College_Name','score')

    def get_name(self, obj):
        return obj.quiz.name
    get_name.admin_order_field  = 'quiz'  
    get_name.short_description = 'Quiz Name'

    def get_Full_Name(self, obj):
        return obj.user.Full_Name
    get_Full_Name.admin_order_field  = 'user'  
    get_Full_Name.short_description = ' Name'

    def get_College_Name(self, obj):
        return obj.user.College_Name
    get_College_Name.admin_order_field  = 'user'  
    get_College_Name.short_description = 'College Name'



    
class quizzes(admin.ModelAdmin):
    model=Quiz
    list_display=('name','topic','time','no_of_question','difficulty')

    list_display_links=('time','no_of_question','difficulty')
    list_filter=('name','topic','time','no_of_question','difficulty')

   



class feedbacks(admin.ModelAdmin):
    model=Result
    list_display=('get_name','get_Full_Name','get_College_Name','feedback')

    # list_display_links=('get_name','get_Full_Name','get_College_Name','score')
    list_filter=('quiz__name','user__Full_Name','user__College_Name','feedback')

    def get_name(self, obj):
        return obj.quiz.name
    get_name.admin_order_field  = 'quiz'  
    get_name.short_description = 'Quiz Name'

    def get_Full_Name(self, obj):
        return obj.user.Full_Name
    get_Full_Name.admin_order_field  = 'user'  
    get_Full_Name.short_description = ' Name'

    def get_College_Name(self, obj):
        return obj.user.College_Name
    get_College_Name.admin_order_field  = 'user'  
    get_College_Name.short_description = 'College Name'


class stud(admin.ModelAdmin):
    model=Student
    list_display=('get_Username','get_Full_Name','get_College_Name')

    # list_display_links=('get_User_Name','get_Full_Name','get_College_Name')
    list_filter=('user__username','user__Full_Name','user__College_Name',)

    def get_Username(self, obj):
        return obj.user.username
    get_Username.admin_order_field  = 'user'  
    get_Username.short_description = 'user name'
    
    def get_Full_Name(self, obj):
        return obj.user.Full_Name
    get_Full_Name.admin_order_field  = 'user'  
    get_Full_Name.short_description = ' Name'

    def get_College_Name(self, obj):
        return obj.user.College_Name
    get_College_Name.admin_order_field  = 'user'  
    get_College_Name.short_description = 'College Name'

    



class AnswerInline(admin.TabularInline):
    model=Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]
    list_display=('text','get_name')

    # list_display_links=('get_name','get_Full_Name','get_College_Name','score')
    list_filter=('text','quiz__name')

    def get_name(self, obj):
        return obj.quiz.name
    get_name.admin_order_field  = 'quiz'  
    get_name.short_description = 'Quiz Name'

    
    



   

admin.site.register(NewUser, CustomUserAdmin)

# admin.site.register(models.Subject)
admin.site.register(models.Quiz,quizzes)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(models.Student,stud)
# admin.site.register(models.TakenQuiz)
admin.site.register(models.Result,results)
admin.site.register(models.feedback,feedbacks)
# admin.site.register(Questions,questions)

