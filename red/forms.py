#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: forms.py
# @Date: 2011年03月10日 星期四 08时34分17秒

from django import forms
from django.template.defaultfilters import filesizeformat

import datetime


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 2621440


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, help_text="Not necessary", required=False)
    tags = forms.CharField(max_length=50, help_text="Not necessary", required=False)
    date = forms.DateField(initial=datetime.date.today, help_text="Not necessary", required=False)
    content = forms.FileField(help_text="**required**")
    save = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked': 'checked',}),
                              label='Save to DB',
                              required=False)

    def clean_content(self):
        content = self.cleaned_data['content']
        content_type = content.content_type.split('/')[0]
        if content_type in ('text',):
            if content._size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('Please keep filesize under %s. Current filesize %' %
                                           (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError('File type is not supported')
        return content
