from django import forms

from .models import KeyWord, SearchTerm, UserRating

class AddKeywordForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AddKeywordForm, self).__init__(*args, **kwargs)
        self.fields['key_word'].required = False

    class Meta:
        model = KeyWord
        fields = ["key_word"]


class AddSearchtermForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSearchtermForm, self).__init__(*args, **kwargs)
        self.fields['search_term'].required = False

    class Meta:
        model = SearchTerm
        fields = ["search_term"]


class UserRatingForm(forms.ModelForm):

    class Meta:
        model = UserRating
        fields = ["rating"]

