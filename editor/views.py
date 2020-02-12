from .forms import SnippetForm
from .models import Snippet
from django.shortcuts import render, redirect
from django.http import QueryDict

# для запуска shell команд
import subprocess
import os

def simple(request):
    if request.method == 'POST':
        # print(request.POST)
        query_dict = QueryDict('', mutable=True)
        query_dict.update(request.POST)




        # тут забираю код с формы и оформляю его в виде .py файла
        # print("RAW POST DATA: {}".format(request.POST['text']))
        code = request.POST['text']
        with open('temp.py', 'w', encoding='utf-8') as f:
            f.write(code)

        # выводит текущаю рабочую директорию
        # print(os.path.abspath(os.getcwd()))

        # запускает python из среды zip и выполняет подготовленный скрипт
        process = subprocess.Popen (["..\Zipline\env\zip\Scripts\python.exe", "temp.py"], stdout=subprocess.PIPE)
        data = process.communicate()
        print(data)
        query_dict['text'] = data

        form = SnippetForm(query_dict)
        form.save()

        return redirect('/editor')
    else:
        form = SnippetForm()
    return render(request, "snippets.html", {
        "form": form,
        "snippets": Snippet.objects.all()
    })