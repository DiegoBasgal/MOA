from datetime import datetime


rawlog = []
with open('/usr/local/operacao-autonoma/logs/MOA.log') as fp:
    rawlog = fp.readlines()

log = []
for line in rawlog:
    try:
        log.append({'datahora': datetime.strptime(' '.join(line.split()[0:2]), '%Y-%m-%d %H:%M:%S,%f'),
                    'severidade': line.split(' ] [')[1],
                    'conteudo': '[' + ''.join(line.split(' ] [')[2:]),
        })
    except:
        log.append({
            'conteudo': ''.join(line),
        })
context = {'log': log,}
print(context)