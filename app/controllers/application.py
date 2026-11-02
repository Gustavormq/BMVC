import csv
import json
import os
from datetime import date, datetime
from io import StringIO
from bottle import template, request, response, redirect, TEMPLATE_PATH
from app.controllers.datarecord import DataRecord
from app.models.expense import Expense

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
views_path = os.path.join(BASE_DIR, 'app', 'views', 'html')
if views_path not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, views_path)
if BASE_DIR not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, BASE_DIR)


class Application():

    def __init__(self):
        self.__model = DataRecord()
        self.__current_username = None
        self.pages = {
            'despesas': self.despesas,
            'editar_despesa': self.editar_despesa,
            'portal': self.portal,
            'helper': self.helper
        }

    def render(self, page, parameter=None, **kwargs):
        content = self.pages.get(page, self.helper)
        if parameter is not None:
            return content(parameter, **kwargs)
        return content(**kwargs)

    # -------------------------------------------------------------------------
    # Autenticação e Controle de Sessão (Nível 3)
    # -------------------------------------------------------------------------
    def get_session_id(self):
        return request.get_cookie('session_id')

    def is_authenticated(self, username=None):
        session_id = self.get_session_id()
        current_username = self.__model.getUserName(session_id)
        if not current_username:
            return False
        if username:
            return username == current_username
        return True

    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self.__current_username = self.__model.getUserName(session_id)
            return session_id, username
        return None, None

    def register_user(self, username, password):
        if not username or not password:
            return None
        return self.__model.book_user(username, password)

    def logout_user(self):
        self.__current_username = None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)

    def portal(self, **kwargs):
        session_id = self.get_session_id()
        current_user = self.__model.getCurrentUser(session_id)
        msg = (request.query.get('msg') or '').strip()
        err = (request.query.get('err') or '').strip()
        return template('portal', current_user=current_user, msg=msg, err=err)

    # -------------------------------------------------------------------------
    # Métricas e Painel de Despesas (Níveis 1, 2 e 4)
    # -------------------------------------------------------------------------
    def _compute_metrics(self, expenses_list):
        total_income = 0.0
        total_expense = 0.0
        category_totals = {}
        day_totals = {}

        for exp in expenses_list:
            if exp.type == 'receita':
                total_income += exp.amount
            else:
                total_expense += exp.amount
                category_totals[exp.category] = round(
                    category_totals.get(exp.category, 0.0) + exp.amount, 2
                )
                day_totals[exp.date] = round(
                    day_totals.get(exp.date, 0.0) + exp.amount, 2
                )

        day_totals_sorted = dict(sorted(day_totals.items()))
        balance = round(total_income - total_expense, 2)

        return {
            'total_income': round(total_income, 2),
            'total_expense': round(total_expense, 2),
            'balance': balance,
            'category_totals': category_totals,
            'day_totals': day_totals_sorted
        }

    def despesas(self, parameter=None, **kwargs):
        session_id = self.get_session_id()
        current_user = self.__model.getCurrentUser(session_id)

        # Caso um parâmetro de rota (/despesas/<username>) seja informado:
        if parameter and not self.is_authenticated(parameter):
            return redirect('/portal?err=Faça+login+para+acessar+a+área+do+usuário')

        start = (request.query.get('start') or '').strip()
        end = (request.query.get('end') or '').strip()
        category = (request.query.get('category') or '').strip()
        expense_type = (request.query.get('type') or 'all').strip()
        search = (request.query.get('search') or '').strip()
        msg = (request.query.get('msg') or '').strip()
        err = (request.query.get('err') or '').strip()

        expenses = self.__model.filter_expenses(
            start=start,
            end=end,
            category=category,
            expense_type=expense_type,
            search=search
        )
        metrics = self._compute_metrics(expenses)

        return template(
            'despesas',
            current_user=current_user,
            expenses=expenses,
            expenses_json=json.dumps([e.to_dict() for e in expenses], ensure_ascii=False),
            categories=Expense.CATEGORIES,
            selected_category=category,
            selected_type=expense_type,
            start=start,
            end=end,
            search=search,
            today=date.today().strftime('%Y-%m-%d'),
            msg=msg,
            err=err,
            **metrics
        )

    def editar_despesa(self, expense_id=None, **kwargs):
        exp = self.__model.get_by_id(expense_id)
        if not exp:
            return redirect('/despesas?err=Lançamento+não+encontrado')
        err = (request.query.get('err') or '').strip()
        return template(
            'editar_despesa',
            expense=exp,
            categories=Expense.CATEGORIES,
            err=err
        )

    def add_expense(self):
        expense_type = (request.forms.getunicode('type') or 'despesa').strip()
        description = (request.forms.getunicode('description') or '').strip()
        amount_str = (request.forms.getunicode('amount') or '').strip()
        category = (request.forms.getunicode('category') or '').strip()
        date_str = (request.forms.getunicode('date') or '').strip()

        if not description or not amount_str or not category or not date_str:
            return redirect('/despesas?err=Todos+os+campos+são+obrigatórios')

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return redirect('/despesas?err=O+valor+deve+ser+um+número+positivo')

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return redirect('/despesas?err=Data+inválida')

        self.__model.book(
            description=description,
            amount=amount,
            category=category,
            expense_date=date_str,
            expense_type=expense_type
        )
        return redirect('/despesas?msg=Lançamento+registrado+com+sucesso')

    def update_expense(self, expense_id):
        exp = self.__model.get_by_id(expense_id)
        if not exp:
            return redirect('/despesas?err=Lançamento+não+encontrado')

        expense_type = (request.forms.getunicode('type') or exp.type).strip()
        description = (request.forms.getunicode('description') or '').strip()
        amount_str = (request.forms.getunicode('amount') or '').strip()
        category = (request.forms.getunicode('category') or '').strip()
        date_str = (request.forms.getunicode('date') or '').strip()

        if not description or not amount_str or not category or not date_str:
            return redirect(f'/edit/{expense_id}?err=Todos+os+campos+são+obrigatórios')

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return redirect(f'/edit/{expense_id}?err=O+valor+deve+ser+um+número+positivo')

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return redirect(f'/edit/{expense_id}?err=Data+inválida')

        self.__model.update(
            expense_id=expense_id,
            description=description,
            amount=amount,
            category=category,
            expense_date=date_str,
            expense_type=expense_type
        )
        return redirect('/despesas?msg=Lançamento+atualizado+com+sucesso')

    def delete_expense(self, expense_id):
        self.__model.remove(expense_id)
        return redirect('/despesas?msg=Lançamento+excluído+com+sucesso')

    def export_csv(self):
        expenses = self.__model.get_all()
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Tipo', 'Data', 'Descrição', 'Categoria', 'Valor'])

        for exp in expenses:
            writer.writerow([
                exp.id,
                exp.type.capitalize(),
                exp.date,
                exp.description,
                exp.category,
                f'{exp.amount:.2f}'
            ])

        response.content_type = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = 'attachment; filename=despesas.csv'
        return output.getvalue()

    # Endpoints JSON para interatividade assíncrona do Frontend
    def api_list(self):
        response.content_type = 'application/json; charset=utf-8'
        expenses = self.__model.get_all()
        return json.dumps([e.to_dict() for e in expenses], ensure_ascii=False)

    def api_create(self):
        response.content_type = 'application/json; charset=utf-8'
        data = request.json or {}
        description = (data.get('description') or '').strip()
        category = (data.get('category') or 'Outros').strip()
        date_str = (data.get('date') or date.today().strftime('%Y-%m-%d')).strip()
        expense_type = (data.get('type') or 'despesa').strip()

        try:
            amount = float(data.get('amount', 0))
            if not description or amount <= 0:
                raise ValueError
        except ValueError:
            response.status = 400
            return json.dumps({'error': 'Dados inválidos para o lançamento.'})

        new_exp = self.__model.book(
            description=description,
            amount=amount,
            category=category,
            expense_date=date_str,
            expense_type=expense_type
        )
        return json.dumps(new_exp.to_dict(), ensure_ascii=False)

    def api_update(self, expense_id):
        response.content_type = 'application/json; charset=utf-8'
        data = request.json or {}
        updated = self.__model.update(
            expense_id=expense_id,
            description=data.get('description', ''),
            amount=data.get('amount', 0),
            category=data.get('category', 'Outros'),
            expense_date=data.get('date', date.today().strftime('%Y-%m-%d')),
            expense_type=data.get('type', 'despesa')
        )
        if not updated:
            response.status = 404
            return json.dumps({'error': 'Não encontrado'})
        return json.dumps(updated.to_dict(), ensure_ascii=False)

    def api_delete(self, expense_id):
        response.content_type = 'application/json; charset=utf-8'
        ok = self.__model.remove(expense_id)
        if not ok:
            response.status = 404
            return json.dumps({'error': 'Não encontrado'})
        return json.dumps({'deleted': expense_id})

    def api_reset(self):
        response.content_type = 'application/json; charset=utf-8'
        expenses = self.__model.reset()
        return json.dumps([e.to_dict() for e in expenses], ensure_ascii=False)

    def helper(self, **kwargs):
        return template('helper')
