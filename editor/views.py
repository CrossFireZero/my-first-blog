from .forms import SnippetForm
from .models import Snippet
from django.shortcuts import render, redirect

# для запуска shell команд
import subprocess


def simple(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()

            # тут забираю код с формы и оформляю его в виде .py файла
            print("RAW POST DATA: {}".format(request.POST['text']))
            lines = request.POST['text'].split('\n')
            with open('temp.py', 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line)
                
            subprocess.run(["python", "temp.py"])
            

            return redirect('/editor')
    else:
        form = SnippetForm()
    return render(request, "snippets.html", {
        "form": form,
        "snippets": Snippet.objects.all()
    })