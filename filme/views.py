from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
#def homepage(request):
    #return render(request,"homepage.html")


#def homefilmes(request):
   #context = {}
    #lista_filmes = Filme.objects.all()
    #context['lista_filmes'] = lista_filmes
    #return render(request, "homefilmes.html", context)

class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')



class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # listview retorna object_list

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme


    def get(self, request, *args, **kwargs):
        #descobrir qual filme o usuario está acessando
        filme = self.get_object()
        # adicionar +1 nas visualizacões do filme e salvar no banco
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)

        return super().get(request, *args, **kwargs) # redireciona o usuario para a url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        #filtrar a minha tabela de filmes de acordo com a categoria
        #self.get_object() <- é o objeto usado no html
        filmes_relacionados = Filme.objects.filter(categoria = self.get_object().categoria)

        context["filmes_relacionados"] = filmes_relacionados

        return context




class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme
    # editando oque vai retornar(object_list) para o usuario
    def get_queryset(self):
        pesquisa = self.request.GET.get("query")
        if pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=pesquisa)
            return object_list

        else:
            return None

class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name','last_name','email']

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user_atual = self.request.user
        if user_atual != user:
            return redirect('filme:editarperfil', pk=self.request.user.id)
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('filme:homefilmes')
class Criarconta(FormView):
    template_name = 'criarconta.html'
    model = Filme
    form_class = CriarContaForm

    def form_valid(self, form):  # funçao pra salvar no banco de dados
        form.save()
        return super().form_valid(form)

    def get_success_url(self): # tem que redirecionar o link da pagina (reverse)
        return reverse('filme:login')