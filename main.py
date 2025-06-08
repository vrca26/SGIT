from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario import Usuario, get_all_users
from models.ticket import get_recent_tickets, get_ticket_stats
from models.asignacion import get_recent_assignments

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})

@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    correo: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter_by(correo=correo, contraseña=contraseña).first()
    if user:
        if user.rol == "admin":
            return RedirectResponse(url="/dashboard_admin", status_code=303)
        else:
            return RedirectResponse(url="/dashboard_empleado", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuario o contraseña incorrectos"})

@app.get("/dashboard_admin", response_class=HTMLResponse)
def dashboard_admin(request: Request, db: Session = Depends(get_db)):
    usuarios = get_all_users(db)
    tickets = get_recent_tickets(db)
    asignaciones = get_recent_assignments(db)
    stats_tickets = get_ticket_stats(db)
    return templates.TemplateResponse("dashboard_admin.html", {
        "request": request,
        "usuarios": usuarios,
        "tickets": tickets,
        "asignaciones": asignaciones,
        "stats_tickets": stats_tickets
    })

@app.get("/dashboard_empleado", response_class=HTMLResponse)
def dashboard_empleado(request: Request):
    return templates.TemplateResponse("dashboard_empleado.html", {"request": request})