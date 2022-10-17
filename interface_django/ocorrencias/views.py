from datetime import datetime
import os.path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from numpy import block

# Create your views here.


@login_required
def ocorrencias_view(request, *args, **kwargs):

    nlinhas = 5
    if int(request.GET.get("nlinhas", 0)) > 5:
        nlinhas = int(request.GET.get("nlinhas", 0))

    rawlog = []
    with open("/usr/local/operacao-autonoma/logs/MOA.log", "rb") as fp:
        rawlog = tail(fp, nlinhas * 5).decode()
        rawlog = rawlog.split("\n")

    log = []
    for line in rawlog:
        try:
            log.append(
                {
                    "datahora": datetime.strptime(
                        " ".join(line.split()[0:2]), "%Y-%m-%d %H:%M:%S,%f"
                    ).strftime("%d/%m/%Y\n%H:%M:%S"),
                    "severidade": line.split("] [")[1],
                    "conteudo": "[" + "] [".join(line.split("] [")[2:]),
                }
            )
        except:
            log.append(
                {
                    "conteudo": "".join(line),
                }
            )
    context = {"log": log[-nlinhas:]}

    return render(request, "ocorrencias.html", context=context)


def tail(f, lines=20):
    """
    https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-similar-to-tail

    """
    total_lines_wanted = lines

    BLOCK_SIZE = 1024 * 16
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if block_end_byte - BLOCK_SIZE > 0:
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0, 0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b"\n")
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b"".join(reversed(blocks))
    return b"\n".join(all_read_text.splitlines()[-total_lines_wanted:])
