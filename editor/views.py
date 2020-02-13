from .forms import SnippetForm
from .models import Snippet
from django.shortcuts import render, redirect
from django.http import QueryDict
import pandas as pd
from plotly.offline import plot, iplot
import plotly.graph_objects as go
import cufflinks as cf


# для запуска shell команд
import subprocess
import os
from pprint import pprint

def simple(request):

    if request.method == 'POST':
        # print(request.POST)
        query_dict = QueryDict('', mutable=True)
        query_dict.update(request.POST)

        # тут забираю код с формы и оформляю его в виде .py файла
        # print("RAW POST DATA: {}".format(request.POST['text']))
        code = request.POST['text']
        query_dict['text'] = code
        # добавляем к возвращенному run_algorithm датафрейму вызов метода сохранения его в .json
        code = code.strip() + ".to_json('perf.json')"
        # pprint(code)
        with open('temp.py', 'w', encoding='utf-8') as f:
            f.write(code)

        # выводит текущую рабочую директорию
        # print(os.path.abspath(os.getcwd()))

        # запускает python из среды zip и выполняет подготовленный скрипт
        process = subprocess.Popen (["..\Zipline\env\zip\Scripts\python.exe", "temp.py"], stdout=subprocess.PIPE)
        data = process.communicate()
        

        # выводы print() скрипта
        output = "\n".join(str(data[0]).split(r'\r\n'))[2:-2]

        form = SnippetForm(query_dict)
        # form.save()

        df = pd.read_json('perf.json')
        
        # plot_div = plot([{'x': df.index, 'y': df[col], 'name': col}  for col in df.columns], output_type='div')
        plot_div = plot([{'x': df.index, 'y': df['portfolio_value'], 'name': 'portfolio'}], output_type='div')
        
        # пример отрисовки графика с помощью plotly
        # x_data = [0,1,2,3]
        # y_data = [x**2 for x in x_data]
        # plot_div = plot([Scatter(x=x_data, y=y_data,
        #                 mode='lines', name='test',
        #                 opacity=0.8, marker_color='green')],
        #                 output_type='div')
        # return render(request, "/editor", context={'plot_div': plot_div})
        return render(request, "snippets.html", context={"form": form, "snippets": "", "output": output, "plot_div": plot_div})

    else:
        form = SnippetForm()

    snippets = []

    return render(request, "snippets.html", {
        "form": form,
        # "snippets": Snippet.objects.all(),
        "snippets": "",
        "output": "",
        "plot_div": ""
    })