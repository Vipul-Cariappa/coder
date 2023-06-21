import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from markdown import markdown

from .forms import AnswerForm, QuestionForm
from .functions import prepare_test_case, run_code
from .models import Answer, Question


# Create your views here.
@login_required
def create_question(request):
    active_user = request.user
    
    if request.method == "POST":
        post = json.loads(request.body.decode("utf-8"))
        
        test_case = prepare_test_case(post["test_case"])
        solution = post["solution"]

        code_run_result = run_code(solution, test_case)["run"]
        
        if code_run_result["code"] == 0:
            Question(
                title=post["title"],
                question=post["question"],
                questionHTML=markdown(post["question"]),
                solution=post["solution"],
                test_case=post["test_case"],
                start_snippet=post["start_snippet"],
                created_by=active_user,
                difficulty=post["difficulty"],
            )#.save()
            
            return redirect("home") # FIXME: detail question page
        else:
            return JsonResponse(code_run_result)
    
    form = QuestionForm()
    return render(request, "challenge/new_question.html", {"form": form})

def list_questions(request):
    context = {
        "questions": Question.objects.all(),
    }
    return render(request, "challenge/list_questions.html", context)

def list_answers(request, question_id):
    context = {
        "answers": Answer.objects.filter(question_id=question_id),
        "question": Question.objects.get(pk=question_id),
    }
    return render(request, "challenge/list_answers.html", context)

@login_required
def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    active_user = request.user
    
    if request.method == "POST":
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = active_user
            post.question = question
            post.save()
            return redirect("challenge:list_question")
        
    context = {
        "form": AnswerForm(),
        "question": question
    }
    
    
    return render(request, "challenge/answer.html", context)
    
@login_required
def update_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    active_user = request.user
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        
        if answer.user == active_user and form.is_valid():
            form.save()
            return redirect("challenge:list_question")
    
    question = get_object_or_404(Question, pk=answer.question.pk)
    
    context = {
        "form": AnswerForm(request.POST or None, instance=answer),
        "question": question
    }
    
    return render(request, "challenge/answer.html", context)
