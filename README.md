Projeto PI 1 da turma 002 Cravinhos 2024

Aplicativo simples para Orçamento feito com Python 3.10.14

**Necessário ter o Python:
https://www.python.org/downloads/
E o Git instalados:
https://git-scm.com/downloads**

Opcionalmente para editar o codigo pode-se utilizar o Vscode:
https://code.visualstudio.com/

Requerimentos que serão instalados pelo requeriments.txt:
``asgiref==3.8.1``
``crispy-bootstrap4==2024.1``
``Django==4.2.4``
``django-crispy-forms==2.1``
``djangorestframework==3.14.0``
``gunicorn==22.0.0``
``packaging==24.0``
``pytz==2023.3``
``sqlparse==0.4.4``
``typing_extensions==4.11.0``
``tzdata==2023.3``


Para adaptar o aplicativo a suas necessidades:

1 - Abra o terminal(Linux) ou se estiver usando Windows o prompt de comando ou powershell

2 - Clone o repositório:
```
git clone https://github.com/phaleixo/orcamento
```
3 - Navegue até a pasta:
```
cd orcamento
```
4 - Crie o ambiente virtual:
```
python -m venv .venv
```
Ou se estiver usando linux pode ser necessario informar que é o python 3:
```
python3 -m venv .venv
```
Voce pode colocar o nome que preferir, neste caso eu coloquei  ".venv"

5 - Ative o ambiente virtual:
Linux
```
source .venv/bin/activate
```
Windows:
```
.venv\Scripts\activate
```

6 - Instale os requerimentos:
```
pip install -r requirements.txt
```

7 - Crie um Superuser (necessario para acesso ao painel administrativo)

```
python manage.py createsuperuser
```

8 - Inicie o servidor
```
python manage.py runserver
```
8 - Abra o seu navegador e coloque o Endereço:
```
http://127.0.0.1:8000/
```
9 - Para adaptar ou melhorar o aplicativo, abra o vscode na pasta:
```
code .
```
10 - Divirta-se!!!

