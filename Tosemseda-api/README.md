# Instalação do projeto do Tosemseda

### Pré-instalação

Caso você já tenha o VirtualEnv instalado, pode pular essa etapa.

Para instalar, antes é preciso criar um ambiente virtual. Considere instalar o virtualenvwrapper:

    $ sudo pip install virtualenvwrapper

Adicione as seguintes linhas no final do seu bash profile:

    $ export WORKON_HOME=$HOME/.virtualenvs
    $ source /usr/local/bin/virtualenvwrapper.sh

Reinicie seu terminal ou execute:

    $ source /usr/local/bin/virtualenvwrapper.sh

### Instalação

Crie o virtualenv:

    $ mkvirtualenv Tosemseda-api

ps.: Ajuste as variáveis de acordo com as suas configurações. 
Caso tenha algum problema: 
#### A culpa SEMPRE é do Guilherme!
       
Instale os pacotes necessários, lembre-se de estar dentro do virtualenv criado, para este caso (workon Tosemseda-api):

    $ pip install -r requirements.txt
    $ pip install -r requirements_dev.txt

### Criando o  banco:

    $ sudo su postgres
    $ psql
    $ CREATE ROLE tosemseda SUPERUSER LOGIN PASSWORD 'tosemseda';
    $ CREATE DATABASE tosemseda;

    $ ALTER DATABASE tosemseda OWNER TO tosemseda;

Reinicie seu terminal ou use:

    $  load-env
q:
quit

\

após isso para atualizar o banco:

    $ python manage.py db upgrade

Migrations:

Primeira vez:

    $ python manage.py db init

Sempre que houver alteração de estrutura:

    $ python manage.py db migrate

O babacao, para usar a area você precisa do postigs, ai você me pergunta como eu uso o postgis Guicharm, assim carai:

    $ sudo su postgres
    $ psql meu_banco -c "CREATE EXTENSION postgis;"

## CDN

Adicionar no nginx: 

```
location /cdn {
                add_header Access-Control-Allow-Origin *;
                alias /seu_path_aqui;
        }
```
ps.: Se colocar no /, é necessário liberar o acesso via chown

