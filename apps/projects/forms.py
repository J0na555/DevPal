from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    tech_stack_raw = forms.CharField(required=False, help_text='Comma separated (e.g. Django, React)')
    needed_roles_raw = forms.CharField(required=False, help_text='Comma separated (e.g. Backend, Designer)')

    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack_raw', 'needed_roles_raw']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance')
        if instance is not None:
            initial.setdefault('tech_stack_raw', ', '.join(instance.tech_stack or []))
            initial.setdefault('needed_roles_raw', ', '.join(instance.needed_roles or []))
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean_tech_stack_raw(self):
        raw = self.cleaned_data.get('tech_stack_raw', '')
        if not raw:
            return []
        return [item.strip() for item in raw.split(',') if item.strip()]

    def clean_needed_roles_raw(self):
        raw = self.cleaned_data.get('needed_roles_raw', '')
        if not raw:
            return []
        return [item.strip() for item in raw.split(',') if item.strip()]

    def save(self, commit=True, created_by=None):
        # create instance without saving many-to-many
        instance = super().save(commit=False)
        instance.tech_stack = self.cleaned_data.get('tech_stack_raw', [])
        instance.needed_roles = self.cleaned_data.get('needed_roles_raw', [])
        if created_by is not None:
            instance.created_by = created_by
        if commit:
            instance.save()
            self.save_m2m()
        return instance
