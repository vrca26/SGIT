from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime


from models.usuario import (
    Usuario, get_all_users, get_user_by_id, create_user, update_user, delete_user
)
from models.ticket import get_recent_tickets, Ticket, get_ticket_stats, create_ticket, update_ticket, delete_ticket

from models.asignacion import (
    get_recent_assignments, get_all_asignaciones, get_asignacion_by_id,
    create_asignacion, update_asignacion, delete_asignacion, puede_asignar_equipo
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

from fastapi.responses import RedirectResponse

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
            response = RedirectResponse(url="/dashboard_empleado", status_code=303)
            response.set_cookie(key="correo", value=correo)  
            return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuario o contraseña incorrectos"})

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("correo")
    return response

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

@app.get("/dashboard_empleado", response_class=HTMLResponse)
def dashboard_empleado(request: Request, db: Session = Depends(get_db), correo: str = Cookie(None)):
    from models.ticket import Ticket
    from models.asignacion import Asignacion
    from models.equipo import Equipo
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    if not usuario or usuario.rol != "empleado":
        return RedirectResponse(url="/", status_code=303)
    tickets = db.query(Ticket).filter_by(id_usuario=usuario.id_usuario).order_by(Ticket.id_ticket.desc()).all()
    asignaciones = db.query(Asignacion).filter_by(id_usuario=usuario.id_usuario).all()
    equipos = []
    for a in asignaciones:
        equipo = db.query(Equipo).filter_by(id_equipo=a.id_equipo).first()
        if equipo:
            equipos.append(equipo)
    return templates.TemplateResponse("dashboard_empleado.html", {
        "request": request,
        "usuario": usuario,
        "tickets": tickets,
        "equipos": equipos,
        "error": ""
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
    error = delete_proveedor(db, id_proveedor)
    if error:
        return templates.TemplateResponse("dashboard_admin.html", {
            "request": {},
            "usuarios": get_all_users(db),
            "proveedores": get_all_proveedores(db),
            "equipos": get_all_equipos(db),
            "tickets": get_recent_tickets(db),
            "asignaciones": get_recent_assignments(db),
            "stats_tickets": get_ticket_stats(db),
            "error": error
        })
    return RedirectResponse(url="/dashboard_admin", status_code=303)

# ========== EQUIPOS ==========
ESTADOS_EQUIPO = ["disponible", "asignado", "reparación"]

@app.get("/equipos/create", response_class=HTMLResponse)
def equipo_create_form(request: Request, db: Session = Depends(get_db)):
    proveedores = get_all_proveedores(db)
    usuarios = get_all_users(db)
    return templates.TemplateResponse("equipo_form.html", {
        "request": request,
        "equipo": None,
        "proveedores": proveedores,
        "usuarios": usuarios,
        "error": "",
        "estados_equipo": ESTADOS_EQUIPO
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
        "error": "",
        "estados_equipo": ESTADOS_EQUIPO
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
    error = delete_equipo(db, id_equipo)
    if error:
        # Renderiza el dashboard con el error
        return templates.TemplateResponse("dashboard_admin.html", {
            "request": {},
            "usuarios": get_all_users(db),
            "proveedores": get_all_proveedores(db),
            "equipos": get_all_equipos(db),
            "tickets": get_recent_tickets(db),
            "asignaciones": get_recent_assignments(db),
            "stats_tickets": get_ticket_stats(db),
            "error": error
        })
    return RedirectResponse(url="/dashboard_admin", status_code=303)


# ========== ASIGNACIONES ==========
@app.get("/asignaciones", response_class=HTMLResponse)
def asignaciones_panel(request: Request, db: Session = Depends(get_db)):
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
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date() if fecha_fin else None
    if not puede_asignar_equipo(db, id_equipo, fecha_inicio_dt, fecha_fin_dt):
        usuarios = get_all_users(db)
        equipos = get_all_equipos(db)
        return templates.TemplateResponse("asignacion_form.html", {
            "request": request,
            "asignacion": None,
            "usuarios": usuarios,
            "equipos": equipos,
            "error": "Este equipo ya está asignado en ese periodo. Debe elegir otro periodo o equipo."
        })
    create_asignacion(db, id_usuario, id_equipo, fecha_inicio_dt, fecha_fin_dt)
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
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date() if fecha_fin else None
    if not puede_asignar_equipo(db, id_equipo, fecha_inicio_dt, fecha_fin_dt, id_asignacion_ignorar=id_asignacion):
        usuarios = get_all_users(db)
        equipos = get_all_equipos(db)
        asignacion = get_asignacion_by_id(db, id_asignacion)
        return templates.TemplateResponse("asignacion_form.html", {
            "request": request,
            "asignacion": asignacion,
            "usuarios": usuarios,
            "equipos": equipos,
            "error": "Este equipo ya está asignado en ese periodo. Debe elegir otro periodo o equipo."
        })
    update_asignacion(db, id_asignacion, id_usuario, id_equipo, fecha_inicio_dt, fecha_fin_dt)
    return RedirectResponse(url="/asignaciones", status_code=303)

@app.post("/asignaciones/delete/{id_asignacion}", response_class=HTMLResponse)
def asignacion_delete(id_asignacion: int, db: Session = Depends(get_db)):
    delete_asignacion(db, id_asignacion)
    return RedirectResponse(url="/asignaciones", status_code=303)


# Crear ticket
@app.get("/tickets/create", response_class=HTMLResponse)
def ticket_create_form(request: Request, db: Session = Depends(get_db), correo: str = Cookie(None)):
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    from models.asignacion import Asignacion
    from models.equipo import Equipo  # <-- Agrega esta línea
    asignaciones = db.query(Asignacion).filter_by(id_usuario=usuario.id_usuario).all()
    equipos = [db.query(Equipo).filter_by(id_equipo=a.id_equipo).first() for a in asignaciones]
    return templates.TemplateResponse("ticket_form.html", {
        "request": request,
        "equipos": equipos,
        "ticket": None,
        "error": ""
    })

@app.post("/tickets/create", response_class=HTMLResponse)
def ticket_create(
    request: Request,
    asunto: str = Form(...),
    descripcion: str = Form(...),
    id_equipo: int = Form(...),
    db: Session = Depends(get_db),
    correo: str = Cookie(None)
):
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    from models.ticket import Ticket
    ticket = Ticket(
        id_usuario=usuario.id_usuario,
        id_equipo=id_equipo,
        asunto=asunto,
        descripcion=descripcion,
        estado="abierto"
    )
    db.add(ticket)
    db.commit()
    return RedirectResponse(url="/dashboard_empleado", status_code=303)

# Editar ticket
@app.get("/tickets/edit/{id_ticket}", response_class=HTMLResponse)
def ticket_edit_form(id_ticket: int, request: Request, db: Session = Depends(get_db), correo: str = Cookie(None)):
    from models.ticket import Ticket
    ticket = db.query(Ticket).filter_by(id_ticket=id_ticket).first()
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    from models.asignacion import Asignacion
    asignaciones = db.query(Asignacion).filter_by(id_usuario=usuario.id_usuario, fecha_fin=None).all()
    equipos = [db.query(models.equipo.Equipo).filter_by(id_equipo=a.id_equipo).first() for a in asignaciones]
    return templates.TemplateResponse("ticket_form.html", {
        "request": request,
        "equipos": equipos,
        "ticket": ticket,
        "error": ""
    })

@app.post("/tickets/edit/{id_ticket}", response_class=HTMLResponse)
def ticket_edit(
    id_ticket: int,
    request: Request,
    asunto: str = Form(...),
    descripcion: str = Form(...),
    id_equipo: int = Form(...),
    db: Session = Depends(get_db)
):
    from models.ticket import Ticket
    ticket = db.query(Ticket).filter_by(id_ticket=id_ticket).first()
    ticket.asunto = asunto
    ticket.descripcion = descripcion
    ticket.id_equipo = id_equipo
    db.commit()
    return RedirectResponse(url="/dashboard_empleado", status_code=303)

# Eliminar ticket
@app.post("/tickets/delete/{id_ticket}", response_class=HTMLResponse)
def ticket_delete(id_ticket: int, db: Session = Depends(get_db)):
    from models.ticket import Ticket
    ticket = db.query(Ticket).filter_by(id_ticket=id_ticket).first()
    if ticket:
        db.delete(ticket)
        db.commit()
    return RedirectResponse(url="/dashboard_empleado", status_code=303)