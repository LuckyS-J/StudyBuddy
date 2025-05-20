from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Goal, Task, Note
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, AddGoalForm, AddTaskForm, AddNoteForm
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.


class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            goals = Goal.objects.filter(user=request.user)
        else:
            goals = None
        return render(request, 'StudyApp/index.html', {
            'goals': goals
        })


class RegisterView(FormView):
    template_name = 'StudyApp/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('LoginView')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class MyLoginView(LoginView):
    template_name = 'StudyApp/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('HomeView')

    def get_success_url(self):
        return self.success_url


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('HomeView')


class TestView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        goals = Goal.objects.all()
        return render(request, 'StudyApp/index.html', {'goals': goals})


class AddGoalView(LoginRequiredMixin, FormView):

    login_url = '/login/'
    redirect_field_name = 'next'

    template_name = 'StudyApp/add.html'
    form_class = AddGoalForm
    success_url = reverse_lazy('HomeView')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST'):
            kwargs.update({
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        try:
            obj.full_clean()
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        obj.save()
        return super().form_valid(form)


class DeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        goal = get_object_or_404(Goal, id=id)

        if goal.user != request.user:
            return HttpResponseForbidden("You do not have permission to delete this goal.")

        goal.delete()
        return redirect('HomeView')


class MyDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        goal_to_show = get_object_or_404(Goal, id=id)
        today = datetime.date.today

        if goal_to_show.user != request.user:
            return HttpResponseForbidden("You do not have permission to show this goal.")

        tasks = goal_to_show.tasks.all()
        notes = goal_to_show.notes.all()
        task_form = AddTaskForm()
        note_form = AddNoteForm()

        return render(request, 'StudyApp/goal-details.html', {
            'goal': goal_to_show,
            'tasks': tasks,
            'notes': notes,
            'task_form': task_form,
            'note_form': note_form,
            'today': today
        })

    def post(self, request, id):
        goal = get_object_or_404(Goal, id=id)
        today = datetime.date.today

        if goal.user != request.user:
            return HttpResponseForbidden("You do not have permission to modify this goal.")

        if 'submit_task' in request.POST:
            task_form = AddTaskForm(request.POST)
            note_form = AddNoteForm()
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.goal = goal
                task.save()
                return redirect(request.path)

        elif 'submit_note' in request.POST:
            note_form = AddNoteForm(request.POST)
            task_form = AddTaskForm()
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.goal = goal
                note.save()
                return redirect(request.path)

        tasks = goal.tasks.all()
        notes = goal.notes.all()

        return render(request, 'StudyApp/goal-details.html', {
            'goal': goal,
            'tasks': tasks,
            'notes': notes,
            'task_form': task_form,
            'note_form': note_form,
            'today': today
        })


@require_POST
@login_required
def toggle_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.goal.user != request.user:
        return HttpResponseForbidden("You do not have permission to modify this task.")

    task.is_done = not task.is_done
    task.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if task.goal.user != request.user:
        return HttpResponseForbidden("You do not have permission to modify this task.")

    task.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id)

    if note.goal.user != request.user:
        return HttpResponseForbidden("You do not have permission to modify this note.")

    note.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
@login_required
def change_goal_status(request, id):
    goal = get_object_or_404(Goal, id=id)
    new_status = request.POST.get('status')

    if goal.user != request.user:
        return HttpResponseForbidden("You do not have permission to modify this goal.")

    if new_status in dict(Goal.STATUS_CHOICES):
        goal.status = new_status
        goal.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
