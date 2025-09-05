from sqlalchemy.orm import relationship
from health_app import app, db
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from enum import Enum as RoleEnum
from flask_login import UserMixin


class UserRole(RoleEnum):
    PATIENT = 1
    DOCTOR = 2
    ADMIN = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    address = Column(String(300), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    phone = Column(String(15), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return self.full_name


class DoctorProfile(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    license = Column(String(100), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    users = relationship('User', backref='doctor_profile', lazy=True,
                         uselist=False)


class Specialty(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib

        # u = User(full_name='Nguyễn Vân Anh', address='HCM', date_of_birth='2003-07-18', gender='Nữ', username='zennen',
        #           email='zennen.tda.clinic@gmail.com.vn', phone='0932694738',
        #           password=str(hashlib.md5('admin'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.ADMIN)

        # u1 = User(full_name='Ngô Hoài Kiều Trinh', address='HCM', date_of_birth='2004-09-09', gender='Nữ', username='tina',
        #          email='tina.tda.clinic@gmail.com.vn', phone='',
        #          password=str(hashlib.md5('admin'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)
        #
        # u2 = User(full_name='Nguyễn Thị Thùy Dương', address='HCM', date_of_birth='2003-08-11', gender='Nữ', username='daisy',
        #          email='daisy.tda.clinic@gmail.com.vn', phone='',
        #          password=str(hashlib.md5('admin'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)

        # u3 = User(full_name='Trương Thị Bảo Ngọc', address='HCM', date_of_birth='2009-11-01', gender='Nữ',
        #           username='tt.bngoc',
        #           email='ttbngoc@gmail.com', phone='0779708819',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.PATIENT)

        # u4 = User(full_name='Trương Văn Tài', address='HCM', date_of_birth='1967-10-01', gender='Nam',
        #           username='vantai', email='tvtai@gmail.com', phone='0903622815',
        #           password=str(hashlib.md5('vantai123'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.DOCTOR)
        #
        # db.session.add(u4)
        #
        # db.session.commit()
