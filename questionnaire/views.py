from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Questionnaire
from .forms import QuestionnaireForm
import uuid
from .utils import calculate_risk_profile, get_portfolio
import json
import numpy as np


def questionnaire(request):
    try:
        if request.method == 'POST':
            form = QuestionnaireForm(request.POST)
            print("Form initialized")
            if form.is_valid():
                print("Form is valid")
               

                questionnaire = form.save(commit=False)
                questionnaire.session_key = request.session.session_key
                questionnaire.unique_id = uuid.uuid4()
                questionnaire.calculate_risk()
                questionnaire.save()
                return redirect('results', uuid=str(questionnaire.unique_id))
            else:
                print("Form is invalid")
                print("Errors:", form.errors)
        else:
            if not request.session.session_key:
                request.session.create()
            form = QuestionnaireForm()
    except Exception as e:
        print("Error in questionnaire view:", str(e))
        form = QuestionnaireForm()  

    return render(request, 'questionnaire/form.html', {'form': form})

def results_view(request, uuid):
    try:
        questionnaire = Questionnaire.objects.get(unique_id=uuid)
        portfolio_dict = json.loads(questionnaire.recommended_portfolio) if questionnaire.recommended_portfolio else {}
        
        return render(request, 'questionnaire/results.html', {
            'risk_profile': questionnaire.risk_profile,
            'portfolio': portfolio_dict,
            'questionnaire': questionnaire
        })
    except Questionnaire.DoesNotExist:
        return redirect('questionnaire')