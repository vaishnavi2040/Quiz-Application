from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django import forms
from .models import NewUser,Answer,Question,StudentAnswer,Quiz
from django.contrib.auth import authenticate
from django.forms import inlineformset_factory
from django import forms

from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from django.utils.translation import gettext as _


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = NewUser
        fields = ('username','password','user_role')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = NewUser
        fields = ('username','password','user_role')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', ) 

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=('text','quiz')
    

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields =  '__all__'

AnswersFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm,
    extra=1, can_delete=True, can_delete_extra=True
)










# AnswersFormSet = inlineformset_factory(Question,  # parent form
#                                                   Answer,  # inline-form
#                                                   fields=['text', 'correct'], # inline-form fields
#                                                   # labels for the fields
#                                                   labels={
#                                                         'text': _(u'Answer Text '
#                                                                           u'deliverable'),
#                                                         'correct': _(u'answer is correct '
#                                                                    u'marks'),
#                                                   },
#                                                   # help texts for the fields
#                                                   help_texts={
#                                                         'text': None,
#                                                         'correct': None,
#                                                   },
#                                                   # set to false because cant' delete an non-exsitant instance
#                                                   can_delete=False,
#                                                   # how many inline-forms are sent to the template by default
#                                                   extra=1)











# class LogInForm(forms.ModelForm):
    
	

# 	class Meta:
# 		model = NewUser
# 		fields = ('username', 'password')

# 	def clean(self):
# 		if self.is_valid():
# 			username = self.cleaned_data['username']
# 			password = self.cleaned_data['password']
# 			if not authenticate(username=username, password=password):
# 				raise forms.ValidationError("Invalid login")








# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model=NewUser
#         fields=('regid',)
    
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model=NewUser
#         fields=('regid',)

# class LogInForm(forms.Form):
#     class Meta:
#         model=NewUser
#         fields=('regid',)

   