from flask import render_template, request, redirect, flash, url_for
from health_app import app, login, dao
from health_app.models import *
from functools import wraps
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html')


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated or current_user.user_role != UserRole.ADMIN:
            return redirect('/login')
        return f(*args, **kwargs)

    return wrapper


@app.route('/admin', methods=['POST'])
def admin_login():
    return render_template('admin/index.html')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/profile')
@login_required
@admin_required
def profile():
    doctors = DoctorProfile.query.all()

    return render_template('admin/index.html', doctors=doctors)


@app.route('/verify/<int:doctor_id>')
@login_required
@admin_required
def verify_doctor(doctor_id):
    doc = DoctorProfile.query.get_or_404(doctor_id)

    if not doc.is_verified:
        doc.is_verified = True

        db.session.commit()

        flash(f'✅ Bác sĩ {doc.full_name} đã được xác nhận thành công!', 'success')
    else:
        flash(f'ℹ️ Bác sĩ {doc.full_name} đã được xác nhận trước đó.', 'info')

    return redirect(url_for('profile'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')

        password = request.form.get('password')

        u = dao.auth_user(username=username, password=password)

        if u:
            login_user(u)

            next = request.args.get('next')

            return redirect(next if next else '/')
        else:
            flash('Sai username hoặc mật khẩu!!! Thử lại đi!', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        email = request.form.get('email')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_role = request.form.get('user_role')

        if User.query.filter_by(username=username).first():
            flash('Username đã tồn tại!', 'danger')

            return redirect('/register')

        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'danger')

            return redirect('/register')

        u = dao.add_user(full_name=full_name, username=username, address=address, gender=gender,
                         date_of_birth=date_of_birth, phone=phone, email=email, password=password, user_role=user_role)

        if user_role == UserRole.DOCTOR:
            license_profile = request.form.get('license_profile')

            doctor = DoctorProfile(user_id=u.id, license_profile=license_profile)

            db.session.add(doctor)

            db.session.commit()

        flash('Đăng ký thành công! Vui lòng đăng nhập', 'success')

        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/')


if __name__ == '__main__':
    from health_app import admin

    app.run(debug=True)
