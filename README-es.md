# 🚀 Antigravity Workspace Manager

[![GitHub stars](https://img.shields.io/github/stars/sickn33/antigravity-awesome-skills?style=social&label=Skills%20Repo%20Stars)](https://github.com/sickn33/antigravity-awesome-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Leer en otros idiomas: [Español](README-es.md), [English](README.md)*

> **⚡ The ultimate companion CLI for the viral [`antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills) library.**

Sistema de gestión completo para estructurar tus proyectos (workspaces) e inyectar *skills* dinámicamente usando el famoso repositorio de [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills). Mientras que el repositorio original provee el conocimiento especializado (+250 skills), este gestor aporta la orquestación para que tus asistentes de IA (Antigravity, Claude Code, Cursor) carguen exclusivamente el contexto necesario en cada proyecto.

![Workspace Manager Demo](demo.gif)

---

## ✨ Características Principales

* **Ubicación Dinámica**: Detección inteligente de la ruta base del proyecto, permitiendo que invoques el script desde cualquier sub-directorio de tu entorno.
* **Asistente Inteligente (Wizard)**: Interfaz de terminal de pasos rápidos para crear workspaces y auto-habilitar los *skills* recomendados de acuerdo a tu stack tecnológico.
* **Aislamiento de Entornos**: Cada proyecto (workspace) mantiene su propia lista de configuración `skill-config.json` y un entorno simbólico (symlink) que enruta solamente a los skills designados.
* **Sincronización Transparente**: Sistema integrado para sincronizar (clonar/actualizar) la carpeta global desde el repositorio oficial de GitHub de manera segura con creación de backups.
* **Reparación Automática**: Detección y limpieza de skills huérfanos o rotos si dejasen de existir en las dependencias padre.

---

## 🚀 Inicio Rápido

### 1. Instalación (Recomendado)

Obtén el alias `wsm` e inicializa todo con un solo comando:

```bash
curl -sSL https://raw.githubusercontent.com/amartelr/antigravity-workspace-manager/main/install.sh | bash
```

*Reinicia tu terminal tras la instalación para activar el comando `wsm`.*

### 2. Instalación Manual (Alternativa)

Si prefieres hacerlo paso a paso:

```bash
# 1. Clona el repositorio
git clone https://github.com/amartelr/antigravity-workspace-manager.git
cd antigravity-workspace-manager

# 2. Inicializa
python3 workspace-manager.py init
```

> 💡 **Tip de portabilidad:** Puedes mover la carpeta clonada a donde prefieras (ej. `~/MisProyectos`), el script autodetectará su nueva ubicación.

### 2. Crear tu Primer Workspace (Modo Asistido)

El flujo más recomendado es utilizar el asistente interactivo:

```bash
wsm wizard
```

El wizard ha sido completamente rediseñado y te guiará en 5 pasos para definir tu entorno:

1. El **Nombre y Descripción** del workspace.
2. El **Tipo de Proyecto** (14 opciones detalladas):
    * Desde clásicos como **API Backend**, **Web Frontend**, **Mobile App**, hasta nuevos flujos como **Microservicios**, **AI/ML**, **Data Engineering**, **DevOps/Infra**, **Game Dev**, **SEO/Marketing**, **Security/Pentesting** y **Blockchain/Web3**.
3. El **Lenguaje Principal** (15 opciones):
    * Python, JavaScript/TypeScript, Go, Dart/Flutter, Rust, Java/Kotlin, C#/.NET, C/C++, Swift/SwiftUI, Ruby, PHP, Elixir, Scala, Julia o Haskell.
4. La **Base de Datos** (11 opciones):
    * PostgreSQL, Supabase, MongoDB/NoSQL, MySQL, SQLite, Redis, Firebase, Neon Postgres, Google Sheets, Elasticsearch o DynamoDB.
5. **Recomendación Inteligente de Skills (Selección Múltiple)**:
    * Basado en lo que hayas seleccionado en los pasos anteriores, el wizard te sugerirá categorías altamente relevantes para inyectar a tu proyecto.
    * *Ejemplos de sugerencias dinámicas:*
      * **🏗️ Arquitectura y Calidad:** [`architecture`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/architecture), [`microservices-patterns`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/microservices-patterns), [`clean-code`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/clean-code)...
      * **🧪 Testing y Debugging:** [`tdd-workflow`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/tdd-workflow), [`playwright-skill`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/playwright-skill)...
      * **🚀 DevOps y Deploy:** [`docker-expert`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/docker-expert), [`github-actions-templates`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/github-actions-templates)...
      * **🔒 Seguridad:** [`api-security-best-practices`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/api-security-best-practices)...
      * **🤖 AI/ML:** [`prompt-engineering`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/prompt-engineering), [`rag-implementation`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/rag-implementation)...
      * **📈 SEO y Marketing:** [`seo-fundamentals`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/seo-fundamentals), [`analytics-tracking`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/analytics-tracking)...
      * **⚡ Automatización:** [`workflow-automation`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/workflow-automation), [`n8n-mcp-tools-expert`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/n8n-mcp-tools-expert)...

---

## 🛠️ Comandos Esenciales

| Acción | Comando |
| :--- | :--- |
| **Inicializar Estructura** | `wsm init` |
| **Darse Alta por Asistente** | `wsm wizard` |
| **Crear Manualmente** | `wsm create nombre-proyecto` |
| **Ver Workspaces Activos** | `wsm list` |
| **Ver Todo el Catálogo de Skills** | `wsm list-skills` |
| **Ver Skills de un Proyecto** | `wsm list-skills nombre-proyecto` |
| **Habilitar Skill** | `wsm enable nombre-proyecto nombre-skill` |
| **Deshabilitar Skill** | `wsm disable nombre-proyecto nombre-skill` |
| **Sincronizar y Reparar Skills** | `wsm sync --auto-fix` |

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
wsm create mi-webapp -t frontend-bundle
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
wsm sync --auto-fix
```

### Trabajos en Background (Crontab/Linux-Mac)
Gracias a que el script auto-detecta rutas e independencias de dónde es invocado, puedes automatizar cronjobs pasándole la ruta absoluta directamente (sin necesidad del clásico `cd` previo). Por ejemplo, actualizaciones automáticas cada domingo de madrugada:

```bash
0 2 * * 0 python3 /ruta/real/a/tu/antigravity-workspace-manager/workspace-manager.py sync --auto-fix
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
