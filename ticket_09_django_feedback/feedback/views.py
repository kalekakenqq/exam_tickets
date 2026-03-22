from django.shortcuts import render, redirect
from .forms import FeedbackForm


def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})


def thank_you(request):
    return render(request, 'feedback/thank_you.html')
