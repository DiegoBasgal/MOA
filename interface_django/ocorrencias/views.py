from datetime import datetime
import os.path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def ocorrencias_view(request, *args, **kwargs):
    
    nlinhas = 5
    if int(request.GET.get('nlinhas', 0)) > 5:
        nlinhas = int(request.GET.get('nlinhas', 0))
        
    rawlog = []
    with open('/usr/local/operacao-autonoma/logs/MOA.log') as fp:
        rawlog = fp.readlines()

    log = []
    for line in rawlog:
        try:
            log.append({'datahora': datetime.strptime(' '.join(line.split()[0:2]), '%Y-%m-%d %H:%M:%S,%f').strftime('%d/%m/%Y\n%H:%M:%S'),
                        'severidade': line.split('] [')[1],
                        'conteudo': '[' + ''.join(line.split('] [')[2:]),
            })
            nlinhas -= 1
            if nlinhas == 0:
                break
        except:
            log.append({
                'conteudo': ''.join(line),
            })

    context = {'log': log}

    return render(request, 'ocorrencias.html', context=context)