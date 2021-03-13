from django.shortcuts import render, redirect
from .models import Task, TextModel
from .forms import TaskForm, TextsFormSecond, FiltCat
from Clasifik.parser.parser import Parser
from Clasifik.predictions.predictor import Predictor
from Clasifik.utils.constants import DATASET_FILE_PATH
from Clasifik.utils.constants import PREPARED_DATASET_FILE_PATH


def error_404_view(request, exception):
    return render(request, 'main/404.html')



# def error_404_view(request, exception):
#    return render(request, 'badword/404.html')


def index(request):
    tasks = Task.objects.all()
    count = tasks.count()
    choises = TextModel.objects.all()
    answer = ''
    kateg = ''
    if request.method == 'POST':
        answer = request.POST.get('filter_by')
        kateg = "в категории " + str(TextModel.objects.get(title=answer))
        # print(answer)
        tasks = Task.objects.filter(title=answer)
        count = tasks.count()

    formSecond = FiltCat()
    context = {
        'title': 'Главная страница сайта',
        'tasks': tasks,
        'count': count,
        'kateg': kateg,
        'choises': choises
    }
    # 'kateg': kateg,

    # tasks = Task.objects.order_by('-id')
    return render(request, 'badword/index.html', context)


def about(request):
    error = ''
    predict = ''
    classText = ''
    otvet3 = {}
    octet12 = ''
    otv = ''

    # ClassificPredict = Predictor()
    if request.method == 'POST':
        form = TextsFormSecond(request.POST)
        if form.is_valid():
            TEXT = form.cleaned_data.get("task")
            predictor = Predictor()
            predictor.train_data()
            otvet = predictor.get_sentiment_percentage(TEXT)
            # otv = f"{otvet['probability_bad']}"
            if predictor.bad_words == {}:
                otv = 'Агрессивные высказываний не обнаружено'
            else:
                otv = f"{otvet['probability_bad']}"
                otv = 'Обнаружена нецензурная лексика или агрессивный подтекст'
        # if float(otv) > 0.5:
        #     otv = 'ах ты'
        # else:
        #     otv = 'молодец'

        else:
            error = 'Форма была неверной'
    form = TaskForm()
    context = {
        'form': form,
        'error': error,
        'predict': otv

    }

    return render(request, 'badword/about.html', context)


def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форме некорректна'

    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'badword/create.html', context)
