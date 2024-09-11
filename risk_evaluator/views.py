# risk_evaluator/views.py
from django.shortcuts import render
import joblib
import os
from django.conf import settings
from django.http import HttpResponse

def evaluate_risk(request):
    if request.method == 'POST':
        try:
            # Collect form data and convert to appropriate types
            age = int(request.POST.get('age', 0))
            education = int(request.POST.get('education', 0))
            sex = int(request.POST.get('sex', 0))
            is_smoking = int(request.POST.get('is_smoking', 0))
            cigs_per_day = int(request.POST.get('cigs_per_day', 0))
            bp_meds = int(request.POST.get('bp_meds', 0))
            prevalent_stroke = int(request.POST.get('prevalent_stroke', 0))
            prevalent_hyp = int(request.POST.get('prevalent_hyp', 0))
            diabetes = int(request.POST.get('diabetes', 0))
            total_cholesterol = float(request.POST.get('total_cholesterol', 0))
            systolic_bp = float(request.POST.get('systolic_bp', 0))
            diastolic_bp = float(request.POST.get('diastolic_bp', 0))
            bmi = float(request.POST.get('bmi', 0))
            heart_rate = float(request.POST.get('heart_rate', 0))

            # Prepare the input data for the model
            input_data = [[age, education, sex, is_smoking, cigs_per_day, bp_meds, prevalent_stroke,
                           prevalent_hyp, diabetes, total_cholesterol, systolic_bp, diastolic_bp, bmi, heart_rate]]
            
            # Define the path to the model
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'rf_model.pkl')
            
            # Check if the model file exists
            if not os.path.exists(model_path):
                return HttpResponse("Model file not found.", status=500)
            
            # Load the model
            model = joblib.load(model_path)

            # Make prediction
            prediction = model.predict(input_data)[0]
            prediction_proba = model.predict_proba(input_data)[0][1]  # Probability of positive class

            # Map prediction to human-readable form
            risk = "High Risk" if prediction == 1 else "Low Risk"

            context = {
                'risk': risk,
                'probability': f"{prediction_proba * 100:.2f}%",
                'input_data': input_data[0]
            }

            return render(request, 'risk_evaluator/result.html', context)
        
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    # If it's a GET request, render the form
    return render(request, 'risk_evaluator/index.html')


