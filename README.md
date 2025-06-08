# 🖥️ Sistema de Gestión de Inventario y Soporte IT  
### Inspirado en Odoo • Desarrollado con FastAPI + MySQL + Bootstrap 5

---

## 📌 Descripción General

Este sistema web permite la gestión eficiente de equipos tecnológicos (PCs, laptops, celulares, impresoras, etc.) dentro de una empresa, permitiendo su asignación a empleados, el registro de proveedores, y la creación de tickets de soporte por parte de los usuarios.  
El sistema está inspirado en la lógica de vistas de Odoo, adaptado para ser compacto, moderno, y funcional.

---

## 🎯 Objetivos del Sistema

- Gestionar el inventario de equipos tecnológicos.
- Registrar proveedores de equipos.
- Asignar equipos a usuarios con historial.
- Permitir que los empleados creen tickets de soporte por equipos asignados.
- Administrar usuarios con distintos roles (admin / empleado).
- Llevar un historial de asignaciones y tickets.

---

## 🛠️ Tecnologías Usadas

| Componente | Tecnología |
|------------|------------|
| Backend API | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+) |
| Base de datos | MySQL 8 (modelado con Workbench) |
| ORM | SQLAlchemy |
| Validación de datos | Pydantic |
| Estilo | Bootstrap 5 + SCSS |
| Frontend | HTML5 + Jinja2 Templates |
| Servidor local | Uvicorn |
| Edición | VS Code |

---
## 🔐 Roles de Usuario

| Rol       | Descripción |
|-----------|-------------|
| Admin     | Accede a todos los módulos: usuarios, equipos, proveedores, asignaciones, tickets. Puede editar, eliminar, crear y ver historiales. |
| Empleado  | Solo ve sus equipos asignados, crea tickets y revisa su historial de tickets. |

---

## 📊 Modelo Relacional (Conceptual)

- **usuarios**
- **equipos**
- **proveedores**
- **asignaciones**
- **tickets**

Relaciones clave:
- Un proveedor puede tener varios equipos.
- Un equipo puede ser asignado a varios usuarios en el tiempo (historial).
- Un usuario puede tener varios tickets.
- Cada ticket está relacionado con un equipo.

---

## 🧱 Modelo Físico (Estructura SQL)

Incluye creación de las tablas mencionadas, relaciones `FOREIGN KEY` entre ellas, y atributos normalizados.

Archivo de creación: `modelo_fisico.sql`

---

## 📁 Funcionalidades Implementadas

- [x] Login con validación de credenciales
- [x] Dashboard según rol (admin / empleado)
- [x] CRUD completo de equipos, usuarios y proveedores
- [x] Registro y cierre de tickets
- [x] Vista tipo árbol (tree) para navegación de datos
- [x] Vista tipo formulario (form) para crear y editar
- [x] Historial de asignaciones
- [x] Interfaz moderna, redondeada, responsiva
- [ ] Exportación de reportes PDF (opcional)
- [ ] Subida de imágenes para equipos (opcional)

---

## 🚀 Instalación Rápida (Modo Local)

```bash
# Clona el proyecto
git clone https://github.com/tuusuario/inventario_fastapi.git
cd inventario_fastapi

# Crea entorno virtual
python -m venv env
source env/bin/activate  # o .\env\Scripts\activate en Windows

# Instala dependencias
pip install -r requirements.txt

# Levanta el servidor
uvicorn app.main:app --reload