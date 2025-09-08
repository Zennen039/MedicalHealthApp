from flask import Blueprint, render_template, session
from datetime import datetime

doctor_bp = Blueprint("doctor", __name__, url_prefix="/doctor")

appointments = [
    {"time": "8:30AM", "patient": "Nguyễn Văn A", "status": "Xem chi tiết"},
    {"time": "9:00AM", "patient": "Nguyễn Văn B", "status": "Xem chi tiết"},
    {"time": "10:00AM", "patient": "Nguyễn Văn C", "status": "Xem chi tiết"},
    {"time": "10:30AM", "patient": "Nguyễn Văn D", "status": "Xem chi tiết"},
]

@doctor_bp.route("/dashboard")
def dashboard():
    print(">>> dashboard route chạy")

    doctor_name = session.get("doctor_name", "Bác sĩ Trinh")
    total_today = 12
    upcoming = 5
    unconfirmed = 2
    avg_rating = 4.5

    return render_template(
        "doctor/dashboard_bs.html",
        doctor_name=doctor_name,
        total_today=total_today,
        upcoming=upcoming,
        unconfirmed=unconfirmed,
        avg_rating=avg_rating,
        appointments=appointments,
        today=datetime.today()
    )