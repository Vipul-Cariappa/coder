import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from markdown import markdown

from .forms import AnswerForm, QuestionForm
from .functions import prepare_test_case, run_code
from .models import Answer, Question


# Create your views here.
@login_required
def question_submit(request):
    active_user = request.user

    if request.method == "POST":
        post = json.loads(request.body.decode("utf-8"))

        test_case = prepare_test_case(post["test_case"])
        solution = post["solution"]

        code_run_result = run_code(solution, test_case)["run"]

        if code_run_result["code"] == 0:
            question = Question(
                title=post["title"],
                question=post["question"],
                questionHTML=markdown(post["question"]),
                solution=post["solution"],
                test_case=post["test_case"],
                start_snippet=post["start_snippet"],
                created_by=active_user,
                difficulty=post["difficulty"],
            )
            question.save()

            messages.success(request, "Question Added Successfully")
            return redirect("challenge:question_view", question.pk)

        else:
            return JsonResponse(code_run_result)

    form = QuestionForm()
    return render(request, "challenge/question_submit.html", {"form": form})


def questions_list(request):
    context = {
        "questions": Question.objects.all(),
    }
    return render(request, "challenge/questions_list.html", context)


def question_view(request, question_id):
    active_user = request.user

    question = get_object_or_404(Question, pk=question_id)

    context = {
        "question": question,
        "users_attempted": question.users_attempted.all().count(),
        "users_completed": question.users_completed.all().count(),
    }

    if question.users_completed.contains(active_user):
        context["solved"] = True
        context["answer"] = Answer.objects.filter(
            question__pk=question_id, user=active_user
        ).first()
    else:
        context["solved"] = False

    return render(request, "challenge/question_single.html", context)


@login_required
def answers_list(request, question_id):
    context = {
        "answers": Answer.objects.filter(question_id=question_id),
        "question": Question.objects.get(pk=question_id),
    }
    return render(request, "challenge/answers_list.html", context)


@login_required
def answer_view(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = get_object_or_404(Question, pk=answer.question.pk)
    return render(
        request,
        "challenge/answer_single.html",
        {
            "answer": answer,
            "question": question,
            "active_user": request.user,
        },
    )


@login_required
def answer_submit(request, question_id):
    # FIXME: repetition of code
    question = get_object_or_404(Question, pk=question_id)
    active_user = request.user

    if request.method == "POST":
        question.users_attempted.add(active_user)

        # Extract details from the POST request
        post = json.loads(request.body.decode("utf-8"))

        test_case = prepare_test_case(question.test_case)
        answer = post["answer"]
        pk = post["pk"]

        # run code
        code_run_result = run_code(answer, test_case)["run"]

        if code_run_result["code"] == 0:
            # all tests pass
            question.users_completed.add(active_user)

            if pk == -1:
                # create new answer
                answer_object = Answer(
                    question=question, answer=answer, user=active_user, tests_pass=True
                )
                answer_object.save()

                code_run_result["pk"] = answer_object.pk

            else:
                # update existing answer
                answer_object = get_object_or_404(Answer, pk=pk)
                answer_object.answer = answer
                answer_object.tests_pass = True
                answer_object.save()

            messages.success(
                request, "Congratulations  🎉🎊\nYou have Solved the given Question"
            )
            return redirect("challenge:answer_view", answer_object.pk)
        else:
            # tests dont pass but save the code
            if pk == -1:
                # create new answer
                new_ans = Answer(
                    question=question, answer=answer, user=active_user, tests_pass=False
                )
                new_ans.save()

                code_run_result["pk"] = new_ans.pk

            else:
                # update existing answer
                answer_object = get_object_or_404(Answer, pk=pk)
                answer_object.answer = answer
                answer_object.tests_pass = False
                answer_object.save()

                code_run_result["pk"] = answer_object.pk
                # question.users_completed.remove(active_user)

            return JsonResponse(code_run_result)

    # get request processing
    context = {"form": AnswerForm(), "question": question}

    try:
        context["answer"] = Answer.objects.get(user=active_user, question=question)
    except ObjectDoesNotExist:
        context["answer"] = None

    return render(request, "challenge/answer_submit.html", context)
