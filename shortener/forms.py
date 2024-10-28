from django import forms

class URLForm(forms.Form):
    original_url = forms.URLField(label="Enter URL to shorten")
    max_requests = forms.IntegerField(label="Max requests", initial=3)
    block_duration = forms.IntegerField(label="Block duration (minutes)", initial=5)
