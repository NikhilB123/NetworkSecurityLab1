from django import forms
from django.contrib.auth.models import User
from .models import NewsListing, UserXtraAuth

class UpdateUserForm(forms.Form):
    update_user_select = forms.ModelChoiceField(
        label="Username",
        queryset=User.objects.filter(is_superuser=False))
    update_user_token    = forms.CharField(label="Token ID", required=False)
    update_user_secrecy  = forms.IntegerField(label="Secrecy Level")
    
    def clean(self):


        # STUDENT TODO
        # This is where the "update user" form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["update_user_secrecy"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something 
        # is wrong
        cleaned_data = super().clean()
        user_auth = UserXtraAuth.objects.get(username=cleaned_data['update_user_select'])
        if cleaned_data['update_user_secrecy'] < user_auth.secrecy:
            raise forms.ValidationError('Cannot reduce user\'s secrecy level') 
        if cleaned_data['update_user_secrecy'] > 0 and cleaned_data['update_user_token'] == "":
            raise forms.ValidationError("Users with secrecy level over 0 need token")
        return cleaned_data
        
class CreateNewsForm(forms.Form):
    new_news_query = forms.CharField(label="New Query", required=False)
    new_news_sources = forms.CharField(label="Sources", required=False)
    new_news_secrecy = forms.IntegerField(label="Secrecy Level", required=False)
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.user_secrecy = 0
    
    def clean(self):
        cleaned_data = super().clean()
        if self.user_secrecy > cleaned_data['new_news_secrecy']:
            raise forms.ValidationError("Secrecy level must be higher than user's secrecy")
        # STUDENT TODO
        # This is where newslisting update form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. Sfo, for example,
        # cleaned_data["new_news_query"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something 
        # is wrong
        
        return cleaned_data
        
class UpdateNewsForm(forms.Form):
    update_news_select = forms.ModelChoiceField(
        label="Update News",
        queryset=None,
        required=False)
    update_news_query   = forms.CharField(label="Update Query", required=False)
    update_news_sources = forms.CharField(label="Update Sources", required=False)
    update_news_secrecy = forms.IntegerField(label="Update Secrecy", required=False)
    user_secrecy_instance = 0
    
    def __init__(self, data, secrecy = -1, *args, **kargs):
        super().__init__(*args, **kargs)
        #
 
        self.fields['update_news_select'].queryset = data
        self.user_secrecy_instance = secrecy
      
        # STUDENT TODO
        # you should change the "queryset" in update_news_select to be None.
        # then, here in the constructor, you can change it to be the filtered
        # data passed in. See this page:
        # https://docs.djangoproject.com/en/3.1/ref/forms/fields/
        # Look specifically in the section "Fields which handle relationships¶"
        # where it talks about starting with an empty queryset.
        #
        # This form is constructed in views.py. Modify this constructor to
        # accept the passed-in (filtered) queryset.
    
    def clean(self, user_secrecy=0):
        cleaned_data = super().clean()
        if cleaned_data["update_news_secrecy"] and cleaned_data["update_news_secrecy"] < self.user_secrecy_instance:
            raise forms.ValidationError("Secrecy level must be higher than user's secrecy")
        if cleaned_data["update_news_secrecy"] and cleaned_data["update_news_secrecy"] < user_secrecy:
            raise forms.ValidationError("Secrecy level must be higher than user's secrecy")

        # STUDENT TODO
        # This is where newslisting update form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["new_news_query"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something 
        # is wrong
        return cleaned_data