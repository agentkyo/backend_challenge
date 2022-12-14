# backend_challenge

Nota: Utilizaremos os seguintes critérios para a avaliação: Desempenho, Testes, Manutenabilidade, Separação de responsabilidades e boas práticas de engenharia de software.

## QUESTION

1. _Tomando como base a estrutura do banco de dados fornecida (conforme diagrama ER_diagram.png e/ou script DDL 1_create_database_ddl.sql, disponibilizados no repositório do github): Construa uma consulta SQL que retorne o nome, e-mail, a descrição do papel e as descrições das permissões/claims que um usuário possui._

```sql
SELECT

    u.name as user_name,
    u.email as user_email,
    r.description as role_description,
    c.description as claim_description

    FROM users u

        INNER JOIN roles r ON u.role_id = r.id
        INNER JOIN user_claims uc ON u.id = uc.user_id
        INNER JOIN claims c ON c.id = uc.claim_id

    WHERE 1=1

        AND u.name = '{}'

```

## QUESTION

2. _Utilizando a mesma estrutura do banco de dados da questão anterior, rescreva a consulta anterior utilizando um ORM (Object Relational Mapping) de sua preferência utilizando a query language padrão do ORM adotado (ex.: Spring JOOQ, EEF LINQ, SQL Alchemy Expression Language, etc)._

```python

    def question_query(self, user_name):

        query = (
            self.session.query(Users, Roles, Claims)
            .filter(Users.name == user_name)
            .filter(Users.role_id == Roles.id)
            .filter(UserClaims.user_id == Users.id)
            .filter(UserClaims.claim_id == Claims.id)
            .all()
        )

        return query

```

## QUESTION

3. _Utilizando a mesma estrutura do banco de dados fornecida anteriormente, e a linguagem que desejar, construa uma API REST que irá listar o papel de um usuário pelo Id (role_id)._

```python

@app.route("/user/<id>/role", methods=["GET"])
def get_user_role(id):
    REQUEST_TRACEBACK_CODE = uuid.uuid4()

    try:
        db = Database()

        role_id = db.get_user_role(user_id=id)

        if role_id["status_code"] == 200:

            Log("get_user_role").add_info("User role retrieved", REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_200(
                message=f"User role retrieved successfully - Role_ID:{role_id['data']}"
            )
        else:
            Log("get_user_role").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_404(
                message=f"Not found =["
            )

    except Exception as e:
        Log("get_user_role").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
        Log("get_user_role").add_error(e, REQUEST_TRACEBACK_CODE)
        msg = Messages(REQUEST_TRACEBACK_CODE).message_return_400(
            message=f"Bad Request - {e} - Traceback_code = {REQUEST_TRACEBACK_CODE}"
        )

    finally:

        return msg


```

## QUESTION

4. _Utilizando a mesma estrutura do banco de dados fornecida anteriormente, e a linguagem que desejar, construa uma API REST que irá criar um usuário. Os campos obrigatórios serão nome, e-mail e papel do usuário. A senha será um campo opcional, caso o usuário não informe uma senha o serviço da API deverá gerar essa senha automaticamente._

```python

@app.route("/adduser", methods=["POST"])
def add_user():
    REQUEST_TRACEBACK_CODE = uuid.uuid4()

    recived_data = request.get_json()
    if recived_data is None or recived_data == {}:
        Log("add_user").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
        return Messages(REQUEST_TRACEBACK_CODE).message_return_400()

    else:
        try:

            PAYLOAD = UserSchema().load(recived_data)

            db = Database()

            if PAYLOAD["password"] is None or PAYLOAD["password"] == "":
                password = Utilities().generate_random_password()

            else:
                password = PAYLOAD["password"]

            print("USER PASSWORD = ", password)

            db.add_user(
                name=PAYLOAD["name"],
                email=PAYLOAD["email"],
                role_id=PAYLOAD["role_id"],
                password=password,
            )

            Log("add_user").add_info("User added", REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_201()

        except Exception as e:
            Log("add_user").add_info("Bad Request", REQUEST_TRACEBACK_CODE)
            Log("add_user").add_error(e, REQUEST_TRACEBACK_CODE)
            msg = Messages(REQUEST_TRACEBACK_CODE).message_return_400(
                message=f"Bad Request - {e} - Traceback_code = {REQUEST_TRACEBACK_CODE}"
            )

        finally:

            return msg

```

## QUESTION

5. _Crie uma documentação que explique como executar seu projeto em ambiente local e também como deverá ser realizado o ‘deploy’ em ambiente produtivo._

```shell

bin/virtualenv testing

source bin/activate

pip install -r /path/to/requirements.txt

python /app.py

```

_Para a próxima questão (a de número 6) apesar da 'stack trace' apresentada ser em Python, o erro é genérico e pode ocorrer com qualquer outra linguagem._

## QUESTION

6. _Nossos analistas de qualidade reportaram uma falha que só acontece em ambientes diferentes do local/desenvolvimento, os engenheiros responsáveis pelo ambiente de Homologação já descartaram problemas de infra-estrutura, temos que levantar o que está acontecendo._

_Ao executar o comando para listar os logs (no stdio) do Pod de Jobs, capturei o seguinte registro de log:_

> [2020-07-06 20:24:49,781: INFO/ForkPoolWorker-2] [expire_orders] - Finishing job…
> [2020-07-06 20:34:49,721: INFO/ForkPoolWorker-1] [renew_wallet_x_access_tokens] Starting task that renew Access Tokens from Wallet X about to expire
> [2020-07-06 20:34:49,723: ERROR/ForkPoolWorker-1] Task tasks.wallet_oauth.renew_wallet_x_access_tokens[ee561a2e-e837-4d98-b771-07f4e2b5ec70] raised u>nexpected: AttributeError("module 'core.settings' has no attribute ‘WALLET_X_TOKEN_MAX_AGE'") Traceback (most recent call last): File "/usr/local/lib/python3.7/site-packages/celery/app/trace.py", line 385, in trace_task R = retval = fun(args, kwargs) File "/usr/local/lib/python3.7/site-packages/celery/app/trace.py", line 650, in protected_call return self.run(args, kwargs) File "/opt/worker/src/tasks/wallet_oauth.py", line 15, in renew_wallet_x_access_tokens expire_at = now - settings.WALLET_X_TOKEN_MAX_AGE AttributeError: module 'core.settings' has no attribute ‘WALLET_X_TOKEN_MAX_AGE'
> [2020-07-06 20:34:49,799: INFO/ForkPoolWorker-2] [expire_orders] - Starting job…
> [2020-07-66 20:34:49,801: INFO/ForkPoolWorker-2] [expire_orders] - Filtering pending operations older than 10 minutes ago.

_De acordo com o log capturado, o que pode estar originando a falha?_
<br>
<br>

> Resposta: A Falha é causada pois não existe o atributo 'WALLET_X_TOKEN_MAX_AGE' no modulo core.settings.
> <br> > <img src="example.png" alt="Example" style="height: 300px; width:700px;"/>

## QUESTION

7. _Ajude-nos fazendo o Code Review do código de um robô/rotina que exporta os dados da tabela users de tempos em tempos. O código foi disponibilizado no mesmo repositório do git hub dentro da pasta bot. ATENÇÃO: Não é necessário implementar as revisões, basta apenas anota-las em um arquivo texto ou em forma de comentários no código._

> As sugestões estão expressas em comentários no código:


``` python

# -*- coding: utf-8 -*-
import os, sys, traceback, logging, configparser
import xlsxwriter
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

def main(argv):
    greetings()

    print('Press Crtl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    '''
Não entendi o motivo do Flask estar sendo utilizado, se não for necessário;
seria interessante remover essa dependência, fazer a conexão do banco direto no SQLALchemy.
    '''
    app = Flask(__name__)
    handler = RotatingFileHandler('bot.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123mudar@127.0.0.1:5432/bot_db'
    db = SQLAlchemy(app)
    config = configparser.ConfigParser()

    '''
Para evitar um novo commit sempre que for necessário alterar o tempo de execução;
seria interessante ter esse valor salvo como uma variavel de ambiente.
    '''
    config.read('/tmp/bot/settings/config.ini')

    var1 = int(config.get('scheduler','IntervalInMinutes'))
    app.logger.warning('Intervalo entre as execucoes do processo: {}'.format(var1))
    scheduler = BlockingScheduler()

    task1_instance = scheduler.add_job(task1(db), 'interval', id='task1_job', minutes=var1)

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        pass

def greetings():
    print('             ##########################')
    print('             # - ACME - Tasks Robot - #')
    print('             # - v 1.0 - 2020-07-28 - #')
    print('             ##########################')

def task1(db):


    '''
Exportar dados de uma tabela para um arquivo Excel, consome recurso e espaço em disco.
O Google Sheets pode receber via API estes dados e armazenar em uma planilha online;
minha primeira sugestão seria salvar os dados necessários em uma planilha realtime do Sheets.
    '''
    file_name = 'data_export_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    file_path = os.path.join(os.path.curdir, file_name)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    '''
Já que foi importada a lib do SQL Alchemy, esta query poderia ser realizada com o ORM.
Select * dependendo do tamanho da tabela, pode consumir muito recurso do banco de dados.
    '''
    orders = db.session.execute('SELECT * FROM users;')
    
    index = 1
    
    worksheet.write('A{0}'.format(index),'Id')
    worksheet.write('B{0}'.format(index),'Name')
    worksheet.write('C{0}'.format(index),'Email')
    worksheet.write('D{0}'.format(index),'Password')
    worksheet.write('E{0}'.format(index),'Role Id')
    worksheet.write('F{0}'.format(index),'Created At')
    worksheet.write('G{0}'.format(index),'Updated At')
    
'''
Escrever linha por linha, pode levar o código a demorar mais do que o necessário e consumir muito recurso.
Aqui é possivel utilizar o pandas, escrever um dataframe e postar no Google Sheets.
Forma mais rápida do que simplesmente appendar linhas em um arquivo Excel.
'''

    for order in orders:
        index = index + 1

        print('Id: {0}'.format(order[0]))
        worksheet.write('A{0}'.format(index),order[0])
        print('Name: {0}'.format(order[1]))
        worksheet.write('B{0}'.format(index),order[1])
        print('Email: {0}'.format(order[2]))
        worksheet.write('C{0}'.format(index),order[2])
        print('Password: {0}'.format(order[3]))
        worksheet.write('D{0}'.format(index),order[3])
        print('Role Id: {0}'.format(order[4]))
        worksheet.write('E{0}'.format(index),order[4])
        print('Created At: {0}'.format(order[5]))
        worksheet.write('F{0}'.format(index),order[5])
        print('Updated At: {0}'.format(order[6]))
        worksheet.write('G{0}'.format(index),order[6])
        
    workbook.close()
    print('job executed!')

if __name__ == '__main__':
    main(sys.argv)
    
   ```




## QUESTION

8. _Qual ou quais Padrões de Projeto/Design Patterns você utilizaria para normalizar serviços de terceiros (tornar múltiplas interfaces de diferentes fornecedores uniforme), por exemplo serviços de disparos de e-mails, ou então disparos de SMS. ATENÇÃO: Não é necessário implementar o Design Pattern, basta descrever qual você utilizaria e por quais motivos optou pelo mesmo._
