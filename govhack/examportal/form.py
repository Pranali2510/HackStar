from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Candidate,Institute

class CandidateSignUpForm(UserCreationForm):
    username=forms.CharField()
    full_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    pincode = forms.CharField(required=True)
    mother_name = forms.CharField(required=True)
    father_name = forms.CharField(required=True)
    gender = forms.CharField(required=True)
    mobileno = forms.CharField(required=True)
    email=forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_candidate = True
        # user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')

        user.save()
        candidate = Candidate.objects.create(user=user)
        candidate.full_name=self.cleaned_data.get('full_name')
        candidate.address=self.cleaned_data.get('address')
        candidate.pincode=self.cleaned_data.get('pincode')
        candidate.mother_name=self.cleaned_data.get('mother_name')
        candidate.father_name=self.cleaned_data.get('father_name')
        candidate.gender=self.cleaned_data.get('gender')
        candidate.mobileno=self.cleaned_data.get('mobileno')
        candidate.email=self.cleaned_data.get('email')

        candidate.save()
        return user

class InstituteSignUpForm(UserCreationForm):
    Institute_Name = forms.CharField(required=True)
    Location = forms.CharField(required=True)
    Institute_Number = forms.CharField(required=True)
    ContactNo = forms.CharField(required=True)
    Website = forms.CharField(required=True)
    email=forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_retailer = True
        # user.is_staff = True
        # user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')

        user.save()
        institute = Institute.objects.create(user=user)
        institute.Institute_Name=self.cleaned_data.get('Institute_Name')
        institute.Location=self.cleaned_data.get('Location')
        institute.Institute_Number=self.cleaned_data.get('Institute_Number')
        institute.ContactNo=self.cleaned_data.get('ContactNo')
        institute.Website=self.cleaned_data.get('Website')
        institute.email=self.cleaned_data.get('email')

        institute.save()
        return user



class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'email']