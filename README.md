# 🚀 Antigravity Workspace Manager

[![GitHub stars](https://img.shields.io/github/stars/sickn33/antigravity-awesome-skills?style=social&label=Skills%20Repo%20Stars)](https://github.com/sickn33/antigravity-awesome-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚡ The ultimate companion CLI for the viral [`antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills) library.**

Sistema de gestión completo para estructurar tus proyectos (workspaces) e inyectar *skills* dinámicamente usando el famoso repositorio de [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills). Mientras que el repositorio original provee el conocimiento especializado (+250 skills), este gestor aporta la orquestación para que tus asistentes de IA (Antigravity, Claude Code, Cursor) carguen exclusivamente el contexto necesario en cada proyecto.

---

## ✨ Características Principales

* **Ubicación Dinámica**: Detección inteligente de la ruta base del proyecto, permitiendo que invoques el script desde cualquier sub-directorio de tu entorno.
* **Asistente Inteligente (Wizard)**: Interfaz de terminal de pasos rápidos para crear workspaces y auto-habilitar los *skills* recomendados de acuerdo a tu stack tecnológico.
* **Aislamiento de Entornos**: Cada proyecto (workspace) mantiene su propia lista de configuración `skill-config.json` y un entorno simbólico (symlink) que enruta solamente a los skills designados.
* **Sincronización Transparente**: Sistema integrado para sincronizar (clonar/actualizar) la carpeta global desde el repositorio oficial de GitHub de manera segura con creación de backups.
* **Reparación Automática**: Detección y limpieza de skills huérfanos o rotos si dejasen de existir en las dependencias padre.

---

## 🚀 Inicio Rápido

### 1. Instalación (Primera vez)

Asegúrate de contar con Python 3 y Git en tu entorno de trabajo.

```bash
# 1. Clona el repositorio en tu máquina local
git clone https://github.com/amartelr/antigravity-workspace-manager.git
cd antigravity-workspace-manager

# 2. (Opcional) Haz el script ejecutable en macOS/Linux
chmod +x workspace-manager.py

# 3. Inicializa la estructura de directorios y descarga los skills
python3 workspace-manager.py init
```

> 💡 **Tip de portabilidad:** Puedes mover la carpeta clonada a donde prefieras (por ejemplo, `~/MisProyectos`), el script autodetectará su nueva ubicación sin romper tus rutas.

### 2. Crear tu Primer Workspace (Modo Asistido)

El flujo más recomendado es utilizar el asistente interactivo:

```bash
python3 workspace-manager.py wizard
```

El wizard te guiará para definir:
1. El **nombre** y una **descripción** de contexto breve.
2. El **tipo de proyecto** (API Backend, Web Frontend, Full-Stack, Mobile App).
3. El **lenguaje principal** (Python, Go, JS/TS, Dart/Flutter).
4. La **base de datos** (PostgreSQL, MongoDB, Supabase, Google Sheets).

---

## 🛠️ Comandos Esenciales

| Acción | Comando |
| :--- | :--- |
| **Inicializar Estructura** | `python3 workspace-manager.py init` |
| **Darse Alta por Asistente** | `python3 workspace-manager.py wizard` |
| **Crear Manualmente** | `python3 workspace-manager.py create nombre-proyecto` |
| **Ver Workspaces Activos** | `python3 workspace-manager.py list` |
| **Ver Todo el Catálogo de Skills** | `python3 workspace-manager.py list-skills` |
| **Ver Skills de un Proyecto** | `python3 workspace-manager.py list-skills nombre-proyecto` |
| **Habilitar Skill** | `python3 workspace-manager.py enable nombre-proyecto nombre-skill` |
| **Deshabilitar Skill** | `python3 workspace-manager.py disable nombre-proyecto nombre-skill` |
| **Sincronizar y Reparar Skills** | `python3 workspace-manager.py sync --auto-fix` |

---

## 📂 Organización de la Estructura Generada

Tras llamar al comando `init`, el script autodesplegará una jerarquía robusta para tu orquestación:

```text
/ruta-base-de-tu-manager/
├── workspace-manager.py          ← Entorno de la CLI
├── .agent/
│   ├── skills/                   ← Todo el repositorio de skills 
│   │   ├── public/               ← Skills oficiales clonados del remote public
│   │   ├── private/              ← Tus skills o directrices empresariales
│   │   └── user/                 ← Skills desarrollados de forma local
│   └── skills_backup/            ← Copias de seguridad periódicas del gestor
├── workspaces/                   ← Directorio contenedor de tus carpetas de trabajo
│   ├── mi-proyecto/
│   │   ├── .agent/
│   │   │   └── skills            ← Enlace estático (symlink) a la biblioteca principal
│   │   ├── skill-config.json     ← Declaración explícita de tus dependencias necesarias
│   │   └── README.md             ← Documento basal propio auto-generado
├── skill-config-templates/       ← Plantillas y colecciones default pre-empaquetadas
```

---

## 💡 Alternativa a la Interfaz: Plantillas (Templates)

Si prefieres obviar la interfaz guiada (Wizard), puedes valerte de los *bundles* para acelerar el *scaffolding*:

```bash
# Inyectará en conjunto todos los skills relativos al área frontend
python3 workspace-manager.py create mi-webapp -t frontend-bundle
```

Ejemplos de plantillas disponibles por defecto:
* **frontend-bundle**: UI/UX design components, react/tailwind patterns, frontend testing.
* **backend-bundle**: clean code, api guidelines y patrones transaccionales.
* **mobile-bundle**: flutter best practices, mobile security.

---

## 🤖 Uso Directo con tu Agente (Prompting Inteligente)

Una vez tu *workspace* es creado, se auto-suministrará un fichero `README.md` base dentro de la carpeta local. Ese fichero incluye un extracto pensado para dárselo en contexto al Asistente IA respectivo:

```text
Workspace: [nombre-del-proyecto]
Recoge la lógica de skills descrita leyendo de la ruta de contexto local ./skill-config.json
Confirma qué librerías exactas tienes ahora bajo contexto.
```

---

## 🔧 Actualización / Mantenimiento Programado

Considera como un hábito refrescar los paquetes que forman tu catálogo de *skills* ejecutando sincrónicos periódicos.

```bash
# Clona, verifica diff de versiones, borra anticuados y actualiza referencias de un golpe
python3 workspace-manager.py sync --auto-fix
```

### Trabajos en Background (Crontab/Linux-Mac)
Puedes desentenderte y decirle a un orquestador cron que evalúe y ejecute actualizaciones cada domingo de madugada:
```bash
0 2 * * 0 cd /ruta/generica/a/la/carpeta/del/manager && python3 workspace-manager.py sync --auto-fix
```

---

## ⚠️ Resolución Frecuente (Troubleshooting)

* **Problemas con Symlinks (Especialmente en Windows):**
  A menudo la consola requiere privilegios amplios para manejar mapeos de directorio profundos.
  > Resuélvelo activando el modo de compatibilidad **Modo Desarrollador**, y abre tu terminal o de comandos con **Permisos de Administrador**. WSL (Windows Subsystem for Linux) también evita el problema al 100%.
* **Rechazos Ejecutando Comando Listados o Command not found:**
  La envoltura del path python debe ser local. Ejecuta `python3 workspace-manager.py ...` (y recuerda el `chmod +x` si prefieres invocarlo crudo).

---

*Desarrolla más rápido, y dota a tu IA del contexto universal exacto.* 🚀
