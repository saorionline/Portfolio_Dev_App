# Simplificación de Portfolio_Dev_App

Casi termino, pero falta un paso que tienes que hacer tú. Una actualización de Windows del 8 de septiembre me impide ejecutar comandos en tu computadora, así que no puedo crear la rama, borrar archivos ni correr Django. Lo que sí pude hacer fue escribir los archivos nuevos, así que dejé todo en un script.

## Ejecuta esto en la terminal de VS Code, dentro de `Portfolio_Dev_App`

```powershell
powershell -ExecutionPolicy Bypass -File .\simplificar.ps1
```

El script hace lo siguiente:

1. Crea la rama `simplificacion`.
2. Borra `atlas_app/`, `core/`, `curriculum/`, las migraciones, `db.sqlite3`, los JSON viejos y `main.html` / `main.js` / `style.css`.
3. Comprueba que Django arranca, corre una prueba y carga la página y el CSS.
4. Si todo sale bien, abre el sitio en `http://127.0.0.1:8000`.

Todo lo que se borra está guardado en tu último commit (`5196ff8`), así que puedes recuperarlo cuando quieras.

## Encontré tres cosas que cambiaron el plan

- **El proyecto no era un portafolio tipo CV.** Es tu monitor de proyectos ("PAI Project Monitor"): los 4 proyectos (Nebula, Phoenix, Quantum, Silverlining), el curso de FastAPI con sus 22 lecciones y las 4 cápsulas de Java. Hasta ahora eso solo se veía en el admin, porque ninguna página estaba conectada y `atlas_app/views.py` tenía un import roto. Ahora hay una página que muestra las tres secciones.
- **La base de datos tenía cambios más recientes que los JSON.** En febrero editaste Nebula, Quantum y Silverlining desde el admin. Saqué los datos de la base, no de los JSON viejos, para no perder esos cambios.
- **`main.html`, `main.js` y `style.css` eran otro proyecto.** Eran un ejercicio de "Social Media App" que no se usaba en ninguna parte, así que el script también los borra.

## Así queda el proyecto

```
config/        settings.py (reducido) · urls.py
portfolio/     views.py · tests.py
  data/        projects.json · curriculum.json · portfolio.json  ← aquí editas
  templates/portfolio/dashboard.html
  static/portfolio/style.css
manage.py · requirements.txt · .gitignore
```

## Siguiente paso

Cuando termine el script, avísame. El script guarda sus resultados en `simplificar.log` y yo lo reviso para confirmar que todo pasó. Si dice que Django no está instalado, primero corre:

```powershell
python -m pip install -r requirements.txt
```
