from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from fake_csv.data_generator import generate_csv_file
from fake_csv.forms import SchemaForm, ColumnForm
from fake_csv.models import Schema, Column, DataSet


class FakeCSVMain(LoginRequiredMixin, ListView):
    """Home page view class with a list of available schemas"""
    model = Schema
    template_name = 'fake_csv/main.html'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schemas'] = Schema.objects.filter(user=self.request.user.id)
        return context


@login_required
def new_schema(request):
    """Adding a new schema"""

    if request.method == 'POST':
        schema_form = SchemaForm(request.POST, request.FILES)
        if schema_form.is_valid():
            schema = schema_form.save(commit=False)
            schema.user = request.user
            schema.save()
            return HttpResponseRedirect(f'/{schema.id}/')
        else:
            return render(request, 'fake_csv/new_schema.html',
                          {'schema_form': SchemaForm()})
    else:
        return render(request, 'fake_csv/new_schema.html',
                      {'schema_form': SchemaForm()})


@login_required
def edit_schema(request, schema_id):

    if request.method == 'POST':
        schema_form = SchemaForm(request.POST,
                                 instance=Schema.objects.get(id=schema_id))
        if schema_form.is_valid():
            schema_form.save()
            return HttpResponseRedirect(f'/')
        else:
            return HttpResponseRedirect(f'/{schema_id}')
    else:
        column_forms = {instance.id: ColumnForm(instance=instance) for instance in Column.objects.filter(schema_id=schema_id)}
        return render(request, 'fake_csv/edit_schema.html',
                      {'schema_form': SchemaForm(instance=Schema.objects.get(id=schema_id)),
                       'column_forms': column_forms,
                       'column_form': ColumnForm(),
                       'schema_id': schema_id})


@login_required
def add_column(request, schema_id):
    """Adding a new column to the schema"""

    if request.method == 'POST':
        try:
            column_form = ColumnForm(request.POST, request.FILES)
            if column_form.is_valid():
                column = column_form.save(commit=False)
                column.schema_id = Schema.objects.get(id=schema_id)
                column.save()
                return HttpResponseRedirect(f'/{schema_id}')
            else:
                return HttpResponseRedirect(f'/{schema_id}')
        except IntegrityError:
            column_forms = {instance.id: ColumnForm(instance=instance) for instance in Column.objects.filter(schema_id=schema_id)}

            return render(request, 'fake_csv/edit_schema.html',
                          {'schema_form': SchemaForm(
                              instance=Schema.objects.get(id=schema_id)
                          ),
                           'column_forms': column_forms,
                           'column_form': ColumnForm(),
                           'schema_id': schema_id,
                           'integrity_error': True})


@login_required
def edit_column(request, schema_id, column_id):

    if request.method == 'POST':
        try:
            column_form = ColumnForm(request.POST,
                                     instance=Column.objects.get(id=column_id))
            if column_form.is_valid():
                column_form.save()
                return HttpResponseRedirect(f'/{schema_id}')
            else:
                return HttpResponseRedirect(f'/{schema_id}')
        except IntegrityError:
            column_forms = [ColumnForm(instance=instance) for instance in
                            Column.objects.filter(schema_id=schema_id)]
            return render(request, 'fake_csv/edit_schema.html',
                          {'schema_form': SchemaForm(
                              instance=Schema.objects.get(id=schema_id)
                          ),
                              'column_forms': column_forms,
                              'column_form': ColumnForm(),
                              'schema_id': schema_id,
                              'integrity_error': True})


@login_required
def delete_schema(request, schema_id):
    schema = Schema.objects.get(id=schema_id)
    schema.delete()
    return redirect('main')


@login_required
def delete_column(request, schema_id, column_id):
    column = Column.objects.get(id=column_id)
    column.delete()
    return HttpResponseRedirect(f'/{schema_id}')


@login_required
def data_sets_view(request, schema_id):
    """Function to present available datasets"""
    schema = Schema.objects.get(id=schema_id)
    columns = Column.objects.filter(schema_id=schema)
    data_sets = DataSet.objects.filter(schema_id=schema)
    return render(request, 'fake_csv/data_sets.html',
                  {'schema': schema, 'columns': columns,
                   'data_sets': data_sets})


def _generate_csv(schema_id, rows):
    """The function generates a CSV file"""
    dataset = DataSet.objects.create(schema_id=Schema.objects.get(id=schema_id),
                                     status='Processing',
                                     rows=rows)
    url = generate_csv_file(schema_id=schema_id, rows=rows, dataset_id=dataset.id)
    return url


@login_required
def generate_data(request, schema_id):
    rows = int(request.GET.get('rows'))
    url = _generate_csv(schema_id, rows)
    return HttpResponse(str(url), content_type="text/html")


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'fake_csv/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            message='Неверное имя пользователя и / или пароль.'))

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('login')
