import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.controllers.application import Application
from bottle import Bottle, run, request, response, redirect, static_file, TEMPLATE_PATH

views_path = os.path.join(BASE_DIR, 'app', 'views', 'html')
if views_path not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, views_path)
if BASE_DIR not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, BASE_DIR)

app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas Estáticas e Helper:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    static_root = os.path.join(BASE_DIR, 'app', 'static')
    return static_file(filepath, root=static_root)

@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Rotas de Controle de Acesso e Sessão (Nível 3 e 4):

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = (request.forms.getunicode('username') or '').strip()
    password = (request.forms.getunicode('password') or '').strip()
    session_id, authenticated_username = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, max_age=3600, path='/')
        return redirect(f'/despesas/{authenticated_username}')
    return redirect('/portal?err=Credenciais+inválidas')

@app.route('/register', method='POST')
def action_register():
    username = (request.forms.getunicode('username') or '').strip()
    password = (request.forms.getunicode('password') or '').strip()
    created = ctl.register_user(username, password)
    if not created:
        return redirect('/portal?err=Usuário+já+existe+ou+dados+inválidos')
    session_id, authenticated_username = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, max_age=3600, path='/')
        return redirect(f'/despesas/{authenticated_username}?msg=Conta+criada+e+autenticada+com+sucesso')
    return redirect('/portal?msg=Conta+criada+com+sucesso')

@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id', path='/')
    return redirect('/portal?msg=Logout+realizado+com+sucesso')


#-----------------------------------------------------------------------------
# Rotas da Aplicação (Páginas e Ações MVC - Níveis 1, 2 e 4):

@app.route('/', method='GET')
@app.route('/despesas', method='GET')
@app.route('/despesas/<parameter>', method='GET')
def despesas(parameter=None):
    return ctl.render('despesas', parameter=parameter)

@app.route('/add', method='POST')
def add_expense():
    return ctl.add_expense()

@app.route('/edit/<expense_id:int>', method='GET')
def edit_expense(expense_id):
    return ctl.render('editar_despesa', expense_id=expense_id)

@app.route('/edit/<expense_id:int>', method='POST')
def update_expense(expense_id):
    return ctl.update_expense(expense_id)

@app.route('/delete/<expense_id:int>', method='POST')
def delete_expense(expense_id):
    return ctl.delete_expense(expense_id)

@app.route('/export', method='GET')
def export_csv():
    return ctl.export_csv()


#-----------------------------------------------------------------------------
# Rotas de API REST/JSON (Sincronização com o Frontend Interativo - Nível 4):

@app.route('/api/transactions', method='GET')
def api_list():
    return ctl.api_list()

@app.route('/api/transactions', method='POST')
def api_create():
    return ctl.api_create()

@app.route('/api/transactions/<expense_id:int>', method='PUT')
def api_update(expense_id):
    return ctl.api_update(expense_id)

@app.route('/api/transactions/<expense_id:int>', method='DELETE')
def api_delete(expense_id):
    return ctl.api_delete(expense_id)

@app.route('/api/reset', method='POST')
def api_reset():
    return ctl.api_reset()


#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
