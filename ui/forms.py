from django import forms

from gestion.models import Examen


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = [
            "titre",
            "description",
            "heure_debut",
            "heure_fin",
            "statut",
            "groupes_autorises",
            "url_tests_git",
            "hash_tests",
            "pdf_examen",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "heure_debut": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "heure_fin": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "groupes_autorises": forms.CheckboxSelectMultiple(),
            "pdf_examen": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["heure_debut"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["heure_fin"].input_formats = ["%Y-%m-%dT%H:%M"]
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                continue
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()

    def clean(self):
        cleaned_data = super().clean()
        debut = cleaned_data.get("heure_debut")
        fin = cleaned_data.get("heure_fin")
        if debut and fin and fin <= debut:
            self.add_error("heure_fin", "La date de fin doit etre apres la date de debut.")

        if not self.instance.pk and not cleaned_data.get("pdf_examen"):
            self.add_error("pdf_examen", "Le PDF de l examen est obligatoire.")

        if self.instance and self.instance.pk and self.instance.statut != "BROUILLON":
            url_tests_git = cleaned_data.get("url_tests_git")
            hash_tests = cleaned_data.get("hash_tests")
            if (
                url_tests_git != self.instance.url_tests_git
                or hash_tests != self.instance.hash_tests
            ):
                self.add_error(
                    "url_tests_git",
                    "Les tests ne peuvent plus etre modifies apres publication.",
                )
        return cleaned_data
