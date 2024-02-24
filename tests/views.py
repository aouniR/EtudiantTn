from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import student_profile_only
from .models import TestOffer, CandidateAnswer,TestResult, MCQTask,Session
import random

@login_required
@student_profile_only
def test_offers(request):
    test_offers_all = TestOffer.objects.all()
    first_question_id = None
    if test_offers_all:
        first_question_id = test_offers_all[0].questions.first().id
    context = {
        'test_offers_all': test_offers_all,
        'first_question_id': first_question_id,
    }
    return render(request, 'test_offers_main.html', context)

@login_required
@student_profile_only
def take_test(request, test_id):
    test_offer = TestOffer.objects.get(id=test_id)
    question_id= request.session.get('question_id')
    session_key=request.session.get('session_key')
    if session_key is None:
        return redirect('my_protected_view')
    if request.method == 'POST':
        submit_action = request.POST.get('action')
        question = MCQTask.objects.get(id=question_id)
        selected_answers =""
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                selected_answers+=value
        session = Session.objects.filter(key=session_key).first()
        if submit_action == 'next': 
            CandidateAnswer.objects.create(student=request.user.student_profile, question=question, answer=selected_answers,session=session)
            request.session['session_key'] = session_key
            return redirect('take_test', test_id=test_id)
        elif submit_action == 'finish':
            CandidateAnswer.objects.create(student=request.user.student_profile, question=question, answer=selected_answers,session=session)
            TestResult.objects.create(student=request.user.student_profile,test=test_offer,session=session)
            session.update_period()
            del request.session['session_key']
            del request.session['question_id']
            return redirect('dashboard')
                
    question_id = question_id+1
    request.session['question_id'] = question_id
    request.session['session_key'] = session_key
    try:
        question = MCQTask.objects.get(id=question_id)
    except MCQTask.DoesNotExist:
        session = Session.objects.get(key=session_key)
        TestResult.objects.create(student=request.user.student_profile,test=test_offer,session=session)
        session.update_period()
        del request.session['session_key']
        del request.session['question_id']
        return redirect('dashboard') 
    all_answers = list(question.mcq_task_answer.all().values_list('other_answer', flat=True))[:3]
    answers = all_answers[:3] if len(all_answers) >= 3 else all_answers
    answers.append(question.right_answer)
    random.shuffle(answers)
    duration = question.question_duration*60
    context={
            'test_offer': test_offer,
            'question':question,
            'answers':answers,
            'duration':duration
        }
    return render(request, 'test/test_page.html', context)

@login_required
@student_profile_only
def begin_test(request, test_id, question_id):
    test_offer = TestOffer.objects.get(id=test_id)
    existing_session = Session.objects.filter(test=test_offer, period=0).first()
    if existing_session:
        session_key = existing_session.key
    else:
        session = Session.objects.create(test=test_offer)
        session_key = session.key
    request.session['question_id'] = question_id-1
    request.session['session_key'] = session_key
    return redirect('take_test', test_id=test_id)

@login_required
@student_profile_only
def delete_session_key(request):
    if request.method == 'POST':
        del request.session['session_key']
