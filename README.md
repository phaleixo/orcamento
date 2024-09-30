Projeto PI da turma 002 Cravinhos 2024

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
``pillow``


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
( se tiver um arquivo chamado 'sqlite',que é o banco de dados, apague ele. Logo vamos criar outro :)
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

8 - Faça as migrações e crie banco de dados sqlite ( se o comando python não funcionar use python3)
```
python manage.py makemigrations
```

```
python manage.py migrate
```

9 - Inicie o servidor
```
python manage.py runserver 0.0.0.0:8080
```
10 - Abra o seu navegador e coloque o Endereço:
```
http:0.0.0.0:8080/admin
```

11 - na tela de login coloque o usuário e a senha que vc criou.

12 - crie um grupo ' gestores ' e nas atribuições permita que ele possa criar usuários, modificar usuários e excluir usuários.

13 - crie um usuário e atribua a este grupo ( esse vai ser o usuário que vai gerir todo o sistema).
14 - crie um grupo chamado ' vendedores ' e salve.

15 - pronto agora saia e abra o link: 

```
http:0.0.0.0:8080
```
16 - faça o login e na tela de gerenciamento vc pode cadastrar sua empresa, vendedores, produtos e clientes ( depois se vc logar como vendedor vai poder realizar orçamentos e cadastrar clientes


17 - Para adaptar ou melhorar o aplicativo, abra o vscode na pasta:
```
code .
```
18 - Divirta-se!!!

