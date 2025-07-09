from django import forms
from .models import Questionnaire

#Arxikopoihsh tou QuestionnaireForm(typoi dedomenwn)
class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = '__all__'
        widgets = {
            'session_key': forms.HiddenInput(),
            'risk_profile': forms.HiddenInput(),
            'recommended_portfolio': forms.HiddenInput(),
            'AGE': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '18',
                'max': '95'
            }),
            'GENDER': forms.Select(attrs={
                'class': 'form-control'
            }),
            'KIDS': forms.Select(attrs={
                'class': 'form-control'
            }),
            'EDUC': forms.Select(attrs={
                'class': 'form-control'
            }),
            'INCOME': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0'
            }),
            'NETWORTH': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0'
            }),
            'WSAVED': forms.Select(attrs={
                'class': 'form-control',
            }),
            'EMERGSAV': forms.Select(attrs={
                'class': 'form-control', 
            }),
            'KNOWL': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max' : '10'
            }),
            'investment_horizon': forms.Select(attrs={
                'class': 'form-control'
            }),
            'MARRIED': forms.Select(attrs={
                'class': 'form-control'
            }),
           'SPENDMOR':forms.Select(attrs={
                'class': 'form-control'
            }),
            'SPENDLESS':forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'AGE': "Ηλικία",
            'GENDER': "Φύλο",
            'KIDS': "Αριθμός παιδιών",
            'EDUC': "Επίπεδο εκπαίδευσης",
            'INCOME': "Ετήσιος Μισθός (€)",
            'NETWORTH': "Συνολική Καθαρή Αξία (€)",
            'WSAVED':"Αν λάβετε απροσδόκητα 1.000 ευρώ, πώς θα τα χρησιμοποιούσατε κυρίως;",
            'EMERGSAV': "Διαθέτει το νοικοκυριό σας αποταμιεύσεις για έκτακτες ανάγκες;",
            'KNOWL': "Πόσο καλά αισθάνεστε ότι κατανοείτε βασικά χρηματοοικονομικά ζητήματα;",
            'SPENDMOR':"Αν το νοικοκυριό σας είχε αύξηση μόνιμου εισοδήματος, πώς θα αντιδρούσατε σε σχέση με τις δαπάνες;",
            'SPENDLESS':"Αν το νοικοκυριό σας είχε μείωση μόνιμου εισοδήματος, πώς θα αντιδρούσε;",
            'investment_horizon': "Επενδυτικός ορίζοντας",
            'MARRIED': "Οικογενειακή Κατάσταση",
        }
        help_texts = {
            'NETWORTH': "Συμπεριλαμβάνοντας καταθέσεις, επενδύσεις και άλλα περιουσιακά στοιχεία",
            'EMERGSAV': "Χρήματα που έχετε άμεσα διαθέσιμα για έκτακτες ανάγκες",
            'KNOWL' : "1 : Καθόλου γνώση  -  10 : Άριστη γνώση"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add HTML5 required attribute to required fields
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'