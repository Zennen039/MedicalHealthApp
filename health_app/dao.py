from health_app.models import *
from flask_login import current_user
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    us = User.query.filter(User.username.__eq__(username),
                           User.password.__eq__(password))

    if role:
        us = us.filter(User.user_role.__eq__(role))

    return us.first()


def add_user(full_name, username, address, gender, date_of_birth, phone, email, password, user_role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(full_name=full_name, phone=phone, email=email, username=username, address=address, gender=gender,
             date_of_birth=date_of_birth, password=password, user_role=user_role)

    db.session.add(u)

    db.session.commit()

    return u


def add_specialty(name, description):
    if not current_user.is_authenticated or current_user.user_role != UserRole.ADMIN:
        raise PermissionError('Chỉ admin mới có quyền thêm chuyên khoa!')

    sp = Specialty(name=name, description=description)

    db.session.add(sp)

    db.session.commit()

    return sp


def edit_specialty(specialty_id, name, description):
    if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
        raise PermissionError('Chỉ admin mới có quyền sửa chuyên khoa!')

    sp = Specialty.query.get(specialty_id)

    if not sp:
        raise ValueError('Chuyên khoa không tồn tại')

    sp.name = name

    sp.description = description

    db.session.commit()

    return sp


def delete_specialty(specialty_id):
    if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
        raise PermissionError('Chỉ admin mới có quyền xóa chuyên khoa!')

    sp = Specialty.query.get(specialty_id)

    if not sp:
        raise ValueError('Chuyên khoa không tồn tại')

    db.session.delete(sp)

    db.session.commit()

    return True
