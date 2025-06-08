from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal

from models.usuario import (
    Usuario, get_all_users, get_user_by_id, create_user, update_user, delete_user
)
from models.ticket import get_recent_tickets, get_ticket_stats
from models.asignacion import (
    get_recent_assignments, get_all_asignaciones, get_asignacion_by_id,
    create_asignacion, update_asignacion, delete_asignacion
)
from models.proveedor import (
    get_all_proveedores, create_proveedor, get_proveedor_by_id, update_proveedor, delete_proveedor
)
from models.equipo import (
    get_all_equipos, create_equipo, get_equipo_by_id, update_equipo, delete_equipo
)

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
    proveedores = get_all_proveedores(db)
    equipos = get_all_equipos(db)
    tickets = get_recent_tickets(db)
    asignaciones = get_recent_assignments(db)
    stats_tickets = get_ticket_stats(db)
    return templates.TemplateResponse("dashboard_admin.html", {
        "request": request,
        "usuarios": usuarios,
        "proveedores": proveedores,
        "equipos": equipos,
        "tickets": tickets,
        "asignaciones": asignaciones,
        "stats_tickets": stats_tickets
    })

# ========== USUARIOS ==========
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

# ========== PROVEEDORES ==========
@app.get("/proveedores/create", response_class=HTMLResponse)
def proveedor_create_form(request: Request):
    return templates.TemplateResponse("proveedor_form.html", {"request": request, "proveedor": None, "error": ""})

@app.post("/proveedores/create", response_class=HTMLResponse)
def proveedor_create(
    request: Request,
    nombre: str = Form(...),
    contacto: str = Form(""),
    telefono: str = Form(""),
    db: Session = Depends(get_db)
):
    create_proveedor(db, nombre, contacto, telefono)
    return RedirectResponse(url="/dashboard_admin", status_code=303)

@app.get("/proveedores/edit/{id_proveedor}", response_class=HTMLResponse)
def proveedor_edit_form(id_proveedor: int, request: Request, db: Session = Depends(get_db)):
    proveedor = get_proveedor_by_id(db, id_proveedor)
    if not proveedor:
        return RedirectResponse(url="/dashboard_admin", status_code=303)
    return templates.TemplateResponse("proveedor_form.html", {"request": request, "proveedor": proveedor, "error": ""})

@app.post("/proveedores/edit/{id_proveedor}", response_class=HTMLResponse)
def proveedor_edit(
    id_proveedor: int,
    request: Request,
    nombre: str = Form(...),
    contacto: str = Form(""),
    telefono: str = Form(""),
    db: Session = Depends(get_db)
):
    update_proveedor(db, id_proveedor, nombre, contacto, telefono)
    return RedirectResponse(url="/dashboard_admin", status_code=303)

@app.post("/proveedores/delete/{id_proveedor}", response_class=HTMLResponse)
def proveedor_delete(id_proveedor: int, db: Session = Depends(get_db)):
    delete_proveedor(db, id_proveedor)
    return RedirectResponse(url="/dashboard_admin", status_code=303)

# ========== EQUIPOS ==========
@app.get("/equipos/create", response_class=HTMLResponse)
def equipo_create_form(request: Request, db: Session = Depends(get_db)):
    proveedores = get_all_proveedores(db)
    usuarios = get_all_users(db)
    return templates.TemplateResponse("equipo_form.html", {
        "request": request,
        "equipo": None,
        "proveedores": proveedores,
        "usuarios": usuarios,
        "error": ""
    })

@app.post("/equipos/create", response_class=HTMLResponse)
def equipo_create(
    request: Request,
    tipo: str = Form(...),
    marca: str = Form(""),
    modelo: str = Form(""),
    serie: str = Form(""),
    estado: str = Form("disponible"),
    proveedor_id: int = Form(None),
    id_usuario: int = Form(None),
    db: Session = Depends(get_db)
):
    create_equipo(db, tipo, marca, modelo, serie, estado, proveedor_id, id_usuario)
    return RedirectResponse(url="/dashboard_admin", status_code=303)

@app.get("/equipos/edit/{id_equipo}", response_class=HTMLResponse)
def equipo_edit_form(id_equipo: int, request: Request, db: Session = Depends(get_db)):
    equipo = get_equipo_by_id(db, id_equipo)
    proveedores = get_all_proveedores(db)
    usuarios = get_all_users(db)
    return templates.TemplateResponse("equipo_form.html", {
        "request": request,
        "equipo": equipo,
        "proveedores": proveedores,
        "usuarios": usuarios,
        "error": ""
    })

@app.post("/equipos/edit/{id_equipo}", response_class=HTMLResponse)
def equipo_edit(
    id_equipo: int,
    request: Request,
    tipo: str = Form(...),
    marca: str = Form(""),
    modelo: str = Form(""),
    serie: str = Form(""),
    estado: str = Form("disponible"),
    proveedor_id: int = Form(None),
    id_usuario: int = Form(None),
    db: Session = Depends(get_db)
):
    update_equipo(db, id_equipo, tipo, marca, modelo, serie, estado, proveedor_id, id_usuario)
    return RedirectResponse(url="/dashboard_admin", status_code=303)

@app.post("/equipos/delete/{id_equipo}", response_class=HTMLResponse)
def equipo_delete(id_equipo: int, db: Session = Depends(get_db)):
    delete_equipo(db, id_equipo)
    return RedirectResponse(url="/dashboard_admin", status_code=303)

# ========== ASIGNACIONES ==========
@app.get("/asignaciones", response_class=HTMLResponse)
def asignaciones_panel(request: Request, db: Session = Depends(get_db)):
    asignaciones = get_all_asignaciones(db)
    usuarios = get_all_users(db)
    equipos = get_all_equipos(db)
    return templates.TemplateResponse("asignaciones_panel.html", {
        "request": request,
        "asignaciones": asignaciones,
        "usuarios": usuarios,
        "equipos": equipos
    })

@app.get("/asignaciones/create", response_class=HTMLResponse)
def asignacion_create_form(request: Request, db: Session = Depends(get_db)):
    usuarios = get_all_users(db)
    equipos = get_all_equipos(db)
    return templates.TemplateResponse("asignacion_form.html", {
        "request": request,
        "asignacion": None,
        "usuarios": usuarios,
        "equipos": equipos,
        "error": ""
    })

@app.post("/asignaciones/create", response_class=HTMLResponse)
def asignacion_create(
    request: Request,
    id_usuario: int = Form(...),
    id_equipo: int = Form(...),
    fecha_inicio: str = Form(...),
    fecha_fin: str = Form(None),
    db: Session = Depends(get_db)
):
    create_asignacion(db, id_usuario, id_equipo, fecha_inicio, fecha_fin)
    return RedirectResponse(url="/asignaciones", status_code=303)

@app.get("/asignaciones/edit/{id_asignacion}", response_class=HTMLResponse)
def asignacion_edit_form(id_asignacion: int, request: Request, db: Session = Depends(get_db)):
    asignacion = get_asignacion_by_id(db, id_asignacion)
    usuarios = get_all_users(db)
    equipos = get_all_equipos(db)
    return templates.TemplateResponse("asignacion_form.html", {
        "request": request,
        "asignacion": asignacion,
        "usuarios": usuarios,
        "equipos": equipos,
        "error": ""
    })

@app.post("/asignaciones/edit/{id_asignacion}", response_class=HTMLResponse)
def asignacion_edit(
    id_asignacion: int,
    request: Request,
    id_usuario: int = Form(...),
    id_equipo: int = Form(...),
    fecha_inicio: str = Form(...),
    fecha_fin: str = Form(None),
    db: Session = Depends(get_db)
):
    update_asignacion(db, id_asignacion, id_usuario, id_equipo, fecha_inicio, fecha_fin)
    return RedirectResponse(url="/asignaciones", status_code=303)

@app.post("/asignaciones/delete/{id_asignacion}", response_class=HTMLResponse)
def asignacion_delete(id_asignacion: int, db: Session = Depends(get_db)):
    delete_asignacion(db, id_asignacion)
    return RedirectResponse(url="/asignaciones", status_code=303)