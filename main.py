from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario import Usuario, get_all_users, get_user_by_id, create_user, update_user, delete_user
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

# CRUD de Usuarios

@app.get("/usuarios/create", response_class=HTMLResponse)
def usuario_create_form(request: Request):
    return templates.TemplateResponse("usuario_form.html", {"request": request, "usuario": None, "error": ""})

@app.post("/usuarios/create", response_class=HTMLResponse)
def usuario_create(
    request: Request,
    nombre: str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(...),
    rol: str = Form(...),
    db: Session = Depends(get_db)
):
    _, error = create_user(db, nombre, correo, contraseña, rol)
    if error:
        return templates.TemplateResponse("usuario_form.html", {"request": request, "usuario": None, "error": error})
    return RedirectResponse(url="/dashboard_admin", status_code=303)

@app.get("/usuarios/edit/{id_usuario}", response_class=HTMLResponse)
def usuario_edit_form(id_usuario: int, request: Request, db: Session = Depends(get_db)):
    usuario = get_user_by_id(db, id_usuario)
    if not usuario:
        return RedirectResponse(url="/dashboard_admin", status_code=303)
    return templates.TemplateResponse("usuario_form.html", {"request": request, "usuario": usuario, "error": ""})

@app.post("/usuarios/edit/{id_usuario}", response_class=HTMLResponse)
def usuario_edit(
    id_usuario: int,
    request: Request,
    nombre: str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(None),
    rol: str = Form(...),
    db: Session = Depends(get_db)
):
    error = update_user(db, id_usuario, nombre, correo, contraseña, rol)
    if error:
        usuario = get_user_by_id(db, id_usuario)
        return templates.TemplateResponse("usuario_form.html", {"request": request, "usuario": usuario, "error": error})
    return RedirectResponse(url="/dashboard_admin", status_code=303)

@app.post("/usuarios/delete/{id_usuario}", response_class=HTMLResponse)
def usuario_delete(id_usuario: int, db: Session = Depends(get_db)):
    delete_user(db, id_usuario)
    return RedirectResponse(url="/dashboard_admin", status_code=303)