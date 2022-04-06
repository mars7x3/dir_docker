from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, request

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


from dir.forms import AddResumeForm, UpdateResumeForm, AddReviewForm
from dir.models import Resume, Category, Review
from django.db.models import Q
from cart.forms import CartAddProductForm


class CategoryListView(ListView):
    model = Category
    template_name = 'obyavleniya.html'
    context_object_name = 'category'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['resume_count'] = Resume.objects.all().count()
        return context


class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'detail.html'
    context_object_name = 'resume'
    pk_url_kwarg = 'resume_id'


    def recommendation(self):
        resumes = Resume.objects.filter(category=self.object.category)
        return resumes[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_form'] = CartAddProductForm()
        context['recommendation'] = self.recommendation()
        return context


class ResumeHome(ListView):
    model = Resume
    template_name = 'resume.html'
    context_object_name = 'resumes'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['resume_count'] = Resume.objects.all().count()
        return context

    def get_queryset(self):
        return Resume.objects.filter(status='Могу сделать')


class WorkHome(ListView):
    model = Resume
    template_name = 'works.html'
    context_object_name = 'resumes'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['resume_count'] = Resume.objects.all().count()
        return context

    def get_queryset(self):
        return Resume.objects.filter(status='Надо сделать')


@login_required(login_url='login')
def add_resume(request):
    if request.method == 'POST':
        form = AddResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user
            form.save()
            return redirect('profile')
    else:
        form = AddResumeForm()

    return render(request, 'add_resume.html', locals())


class ResumeUpdateView(UpdateView):
    model = Resume
    template_name = 'update_resume.html'
    form_class = UpdateResumeForm
    pk_url_kwarg = 'pk'
    context_object_name = 'resume'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_form'] = self.get_form(self.get_form_class())
        return context


class ResumeDeleteView(DeleteView):
    model = Resume
    template_name = 'delete_resume.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'resume'

    def get_success_url(self):
        from django.urls import reverse
        return reverse('profile')


class SearchListView(ListView):
    model = Resume
    template_name = 'search.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['resume_count'] = Resume.objects.all().count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset


@login_required(login_url='login')
def reviews(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    review = resume.resumes.all()
    if request.method == 'POST':
        form = AddReviewForm(request.POST or None)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.username = request.user
            rev.resume_id = resume
            rev.save()
            return HttpResponseRedirect(request.build_absolute_uri('/resume/' + str(pk)))
    else:
        form = AddReviewForm

    return render(request, 'detail.html', {'resume': resume, 'form': form, 'review': review})


def delete_comment(request, pk):
    review = get_object_or_404(Review, id=pk)
    resume_id = review.resume_id
    if request.user == review.username:
        try:
            review.delete()
        except:
            review.text = '***Сообщение удалено***'
            review.save()
            return redirect(resume_id.get_absolut_url())
        return redirect(resume_id.get_absolut_url())
    messages.error(request, 'У вас нет доступа для удаления данного комментария', extra_tags='reviews')
    return redirect(resume_id.get_absolut_url())


class FilterHome(DetailView):
    model = Category
    template_name = 'filter.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        activities = self.get_related_activities()
        context['categories'] = self.model.objects.all()
        context['resumes'] = activities
        context['page_obj'] = activities
        context['slug'] = self.kwargs['slug']
        context['resume_count'] = Resume.objects.all().count()
        return context

    def get_related_activities(self):
        queryset = self.object.resume.all()
        paginator = Paginator(queryset, 2)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities
