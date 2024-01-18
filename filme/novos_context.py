from .models import Filme

def lista_filmes_recentes(request):
    lista_filme = Filme.objects.all().order_by("-data_de_criacao")[0:10]
    return {"lista_filmes_recentes": lista_filme}

def lista_filmes_em_alta(request):
    lista_filme = Filme.objects.all().order_by("-visualizacoes")[0:10]
    return {"lista_filmes_em_alta": lista_filme}

def filme_destaque(request):
    lista_filme = Filme.objects.order_by('-visualizacoes')
    if lista_filme:
        filme = lista_filme[0]
    else:
        filme = None

    return {'filme_destaque': filme}