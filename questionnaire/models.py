from decimal import Decimal
from django.db import models
import uuid
from django.utils import timezone
from .utils import calculate_risk_profile, get_portfolio
import json


#Arxikopoihsh tou QuestionnaireModel-Django Database
class Questionnaire(models.Model):
    session_key = models.CharField(max_length=40, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
  # Προσωπικές Πληροφορίες
    AGE = models.IntegerField(default=18, verbose_name="Ηλικία")

    GENDER_CHOICES = [
        (1, 'Άνδρας'),
        (2, 'Γυναίκα'),
        
    ]
    GENDER = models.IntegerField(
        choices=GENDER_CHOICES,
        default=1,
        verbose_name="Φύλο"
    )

    MARITAL_STATUS_CHOICES = [
        (1, 'Άγαμος'),
        (2, 'Έγγαμος'),
    ]
    MARRIED = models.IntegerField(
        choices=MARITAL_STATUS_CHOICES,
        default=1,
        verbose_name="Οικογενειακή Κατάσταση"
    )

    CHILDREN_CHOICES = [
        (0, '0 παιδιά'),
        (1, '1 παιδί'),
        (2, '2 παιδιά'),
        (3, '3 παιδιά'),
        (4, '4 ή περισσότερα παιδιά'),
    ]
    KIDS = models.IntegerField(
        choices=CHILDREN_CHOICES,
        default=0,
        verbose_name="Αριθμός Παιδιών"
    )

    EDUCATION_LEVEL_CHOICES = [
        (6, 'Γυμνάσιο'),
        (8, 'Λύκειο'),
        (10, 'Πανεπιστήμιο'),
        (12, 'Μεταπτυχιακό'),
        (14, 'Διδακτορικό'),
    ]
    EDUC = models.IntegerField(
        choices=EDUCATION_LEVEL_CHOICES,
        default=2,
        verbose_name="Επίπεδο Εκπαίδευσης"
    )

    INCOME = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=10000,
        verbose_name="Ετήσιο Εισόδημα (€)"
    )
    NETWORTH = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=100000,
        verbose_name="Συνολική Καθαρή Αξία (€)"
    )

    WSAVED_CHOICES = [
        (1, 'Αποταμίευση ή Επένδυση'),
        (2, 'Κατανάλωση'),
        (3, 'Αποπληρωμή Χρεών'),
    ]
    WSAVED = models.IntegerField(
        choices=WSAVED_CHOICES,
        default=1,
        verbose_name="Αν λάβετε απροσδόκητα 1.000 ευρώ, πώς θα τα χρησιμοποιούσατε κυρίως;"
    )

    SPENDMOR_CHOICES = [
        (1, 'Θα αύξανα αρκετά τις δαπάνες'),
        (2, 'Θα αύξανα ελάχιστα τις δαπάνες'),
        (3, 'Δεν θα άλλαζα κάτι'),
        (4, 'Θα μείωνα ελάχιστα τις δαπάνες'),
        (5, 'Θα μείωνα αρκετά τις δαπάνες'),
    ]
    SPENDMOR = models.IntegerField(
        choices=SPENDMOR_CHOICES,
        default=3,
        verbose_name="Αν το νοικοκυριό σας είχε αύξηση μόνιμου εισοδήματος, πώς θα αντιδρούσατε σε σχέση με τις δαπάνες;"
    )

    SPENDLESS_CHOICES = [
        (1, 'Θα μείωνα αρκετά τις δαπάνες'),
        (2, 'Θα μείωνα ελάχιστα τις δαπάνες'),
        (3, 'Δεν θα άλλαζα κάτι'),
        (4, 'Θα αύξανα ελάχιστα τις δαπάνες'),
        (5, 'Θα αύξανα αρκετά τις δαπάνες'),
    ]
    SPENDLESS = models.IntegerField(
        choices=SPENDLESS_CHOICES,
        default=3,
        verbose_name="Αν το νοικοκυριό σας είχε μείωση μόνιμου εισοδήματος, πώς θα αντιδρούσε;"
    )

    EMERGSAV_CHOICES = [
        (0, 'Όχι, δεν έχει αποταμιεύσεις'),
        (1, 'Ναι, έχει αποταμιεύσεις')
    ]
    EMERGSAV = models.IntegerField(
        choices=EMERGSAV_CHOICES,
        default=0,
        verbose_name=" Διαθέτει το νοικοκυριό σας αποταμιεύσεις για έκτακτες ανάγκες;"
    )

    KNOWL = models.IntegerField(
        default=4,
        verbose_name=" Πόσο καλά αισθάνεστε ότι κατανοείτε βασικά χρηματοοικονομικά ζητήματα;"
    )


    # Επενδυτικός ορίζοντας
    INVESTMENT_HORIZON_CHOICES = [
        ('short', 'Βραχυπρόθεσμος (0-2 έτη)'),
        ('medium', 'Μεσοπρόθεσμος (3-5 έτη)'),
        ('long', 'Μακροπρόθεσμος (5+ έτη)'),
    ]
    investment_horizon = models.CharField(
        max_length=30,
        choices=INVESTMENT_HORIZON_CHOICES,
        default='short'
    )

    risk_profile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Προφίλ Ρίσκου"
    )

    recommended_portfolio = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Προτεινόμενο Χαρτοφυλάκιο"
    )

    def save(self, *args, **kwargs):
        
        if not self.risk_profile and self.pk:  # Only for existing instances
            self.calculate_risk()
        super().save(*args, **kwargs)
    
    def calculate_risk(self):
        print("Calculating risk profile...")
    # Convert data to floats(to be used in the model)
        form_data = {
            'AGE': float(self.AGE),
            'EDUC': float(self.EDUC),
            'MARRIED': float(self.MARRIED),
            'KIDS': float(self.KIDS),
            'RACECL': float(self.GENDER),  
            'INCOME': float(self.INCOME),
            'NETWORTH': float(self.NETWORTH),
            'WSAVED': float(self.WSAVED),
            'KNOWL': float(self.KNOWL),
            'EMERGSAV': float(self.EMERGSAV)
        }
        
        
        self.risk_profile = Decimal(calculate_risk_profile(form_data)).quantize(Decimal('0.0001'))
        self.recommended_portfolio = json.dumps(get_portfolio(float(self.risk_profile)))
        
        
    class Meta:
        verbose_name = "Ερωτηματολόγιο Πρόβλεψης Ανοχής Ρίσκου"
        verbose_name_plural = "Ερωτηματολόγια"

    def __str__(self):
        return f"Ερωτηματολόγιο #{self.id}"
