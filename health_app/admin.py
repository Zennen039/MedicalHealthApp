from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask import redirect
from health_app import app, db
from health_app.models import *
from flask_login import current_user, logout_user


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='TDA System', template_mode='bootstrap4', index_view=MyAdminView())


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class SpecialtyView(AdminView):
    column_list = ('id', 'name', 'description')
    column_filters = ('id' ,'name')
    column_searchable_list = ('id', 'name')
    column_editable_list = ('name', 'description')
    can_export = True


admin.add_view(SpecialtyView(Specialty, db.session, name='Chuyên khoa'))
admin.add_view(AdminView(User, db.session, name='Người dùng'))
admin.add_view(LogoutView(name='Đăng xuất'))
