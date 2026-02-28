# 🚀 Antigravity Workspace Manager

[![GitHub stars](https://img.shields.io/github/stars/sickn33/antigravity-awesome-skills?style=social&label=Skills%20Repo%20Stars)](https://github.com/sickn33/antigravity-awesome-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Read this in other languages: [English](README.md), [Español](README-es.md)*

> **⚡ The ultimate companion CLI for the viral [`antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills) library.**

A complete management system to structure your projects (workspaces) and dynamically inject *skills* using the famous [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) repository. While the original repository provides specialized knowledge (+250 skills), this manager brings the orchestration needed for your AI assistants (Antigravity, Claude Code, Cursor) to load exclusively the necessary context into each project.

![Workspace Manager Demo](demo-en.gif)

---

## ✨ Key Features

* **Dynamic Location**: Intelligent detection of the base project path, allowing you to invoke the script from any subdirectory within your environment.
* **Smart Wizard**: A step-by-step terminal interface to easily create workspaces and auto-enable recommended *skills* tailored to your tech stack.
* **Environment Isolation**: Each project (workspace) maintains its own `skill-config.json` configuration file and a symbolic link (symlink) environment routing only to the designated skills.
* **Transparent Synchronization**: Integrated system to safely sync (clone/update) the global folder from the official GitHub repository, including automatic backups.
* **Auto-Repair**: Detection and cleanup of orphaned or broken skills in case they are removed from the parent repository.

---

## 🚀 Quick Start

### 1. Installation (Recommended)

Get the `wsm` alias and initialize everything in one command:

```bash
curl -sSL https://raw.githubusercontent.com/amartelr/antigravity-workspace-manager/main/install.sh | bash
```

*Restart your terminal after installation to enable the `wsm` command.*

### 2. Manual Installation (Alternative)

If you prefer to do it manually:

```bash
# 1. Clone the repository
git clone https://github.com/amartelr/antigravity-workspace-manager.git
cd antigravity-workspace-manager

# 2. Initialize
python3 workspace-manager.py init
```

> 💡 **Portability Tip:** You can move the folder wherever you prefer (e.g., `~/MyProjects`). The script will auto-detect its new location.

### 2. Create Your First Workspace (Assisted Mode)

The highly recommended workflow is to use the interactive wizard:

```bash
wsm wizard
```

The completely redesigned wizard will guide you through 5 steps to define your environment:

1. The **Name and Description** of the workspace.
2. The **Project Type** (14 detailed options):
   * From classics like **API Backend**, **Web Frontend**, **Mobile App**, to new flows like **Microservices**, **AI/ML**, **Data Engineering**, **DevOps/Infra**, **Game Dev**, **SEO/Marketing**, **Security/Pentesting** and **Blockchain/Web3**.
3. The **Primary Language** (15 options):
   * Python, JavaScript/TypeScript, Go, Dart/Flutter, Rust, Java/Kotlin, C#/.NET, C/C++, Swift/SwiftUI, Ruby, PHP, Elixir, Scala, Julia or Haskell.
4. The **Database** (11 options):
   * PostgreSQL, Supabase, MongoDB/NoSQL, MySQL, SQLite, Redis, Firebase, Neon Postgres, Google Sheets, Elasticsearch or DynamoDB.
5. **Intelligent Skill Recommendation (Multi-select)**:
   * Based on your previous selections, the wizard will suggest highly relevant categories to inject into your project.
   * *Examples of dynamic suggestions:*
     * **🏗️ Architecture & Quality:** [`architecture`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/architecture), [`microservices-patterns`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/microservices-patterns), [`clean-code`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/clean-code)...
     * **🧪 Testing & Debugging:** [`tdd-workflow`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/tdd-workflow), [`playwright-skill`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/playwright-skill)...
     * **🚀 DevOps & Deploy:** [`docker-expert`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/docker-expert), [`github-actions-templates`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/github-actions-templates)...
     * **🔒 Security:** [`api-security-best-practices`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/api-security-best-practices)...
     * **🤖 AI/ML:** [`prompt-engineering`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/prompt-engineering), [`rag-implementation`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/rag-implementation)...
     * **📈 SEO & Marketing:** [`seo-fundamentals`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/seo-fundamentals), [`analytics-tracking`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/analytics-tracking)...
     * **⚡ Automation:** [`workflow-automation`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/workflow-automation), [`n8n-mcp-tools-expert`](https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/n8n-mcp-tools-expert)...

---

## 🛠️ Essential Commands

| Action | Command |
| :--- | :--- |
| **Initialize Structure** | `wsm init` |
| **Assisted Setup** | `wsm wizard` |
| **Manual Creation** | `wsm create project-name` |
| **View Active Workspaces** | `wsm list` |
| **View Full Skills Catalog**| `wsm list-skills` |
| **View Project Skills** | `wsm list-skills project-name` |
| **Enable Skill** | `wsm enable project-name skill-name` |
| **Disable Skill** | `wsm disable project-name skill-name` |
| **Recommend Skills**       | `wsm reco-skills project-name` |
| **Sync and Repair Skills** | `wsm sync --auto-fix` |

---

## 📂 Generated Structure Organization

After executing the `init` command, the script will automatically deploy a robust hierarchy for your orchestration:

```text
/your-manager-base-path/
├── workspace-manager.py          ← CLI Environment
├── .agent/
│   ├── skills/                   ← The entire skills repository
│   │   ├── public/               ← Official skills cloned from the public remote
│   │   ├── private/              ← Your private skills or enterprise guidelines
│   │   └── user/                 ← Locally developed skills
│   └── skills_backup/            ← Periodic manager backups
├── workspaces/                   ← Container directory for your working folders
│   ├── my-project/
│   │   ├── .agent/
│   │   │   └── skills            ← Static link (symlink) to the main library
│   │   ├── skill-config.json     ← Explicit declaration of your necessary dependencies
│   │   └── README.md             ← Auto-generated foundational document
├── skill-config-templates/       ← Pre-packaged default templates and collections
```

---

## 💡 Interface Alternative: Templates

If you prefer to bypass the guided interface (Wizard), you can speed up scaffolding by relying on *bundles*:

```bash
# Will collectively inject all skills related to the frontend area
wsm create my-webapp -t frontend-bundle
```

Examples of default available templates:
* **frontend-bundle**: UI/UX design components, react/tailwind patterns, frontend testing.
* **backend-bundle**: clean code, api guidelines, and transactional patterns.
* **mobile-bundle**: flutter best practices, mobile security.

---

## 🤖 Direct Usage with your Agent (Smart Prompting)

Once your *workspace* is created, a base `README.md` file will automatically populate within the local folder. This file includes an excerpt specifically designed to pass context to your respective AI Assistant:

```text
Workspace: [project-name]
Collect the described skills logic reading from the local context path ./skill-config.json
Confirm the exact libraries you now have under context.
```

---

## 🔧 Scheduled Update / Maintenance

Consider making it a habit to refresh the packages comprising your *skills* catalog by running periodic syncs.

```bash
# Clone, verify version diffs, delete outdated ones, and update references in one go
wsm sync --auto-fix
```

### Background Jobs (Crontab/Linux-Mac)
Thanks to the script auto-detecting paths independently of where it's invoked, you can automate cronjobs by passing the absolute path directly (no need for the classic preceding `cd`). For instance, automatic updates every Sunday at dawn:

```bash
0 2 * * 0 python3 /real/path/to/your/antigravity-workspace-manager/workspace-manager.py sync --auto-fix
```

---

## ⚠️ Troubleshooting

* **Symlink Issues (Especially on Windows):**
  Console often requires extended privileges to handle deep directory mappings.
  > Resolve it by enabling the compatibility **Developer Mode**, and opening your command terminal with **Administrator Privileges**. WSL (Windows Subsystem for Linux) also prevents this issue 100%.
* **Rejections Executing Listed Commands or Command not found:**
  The python path wrapping must be local. Execute `python3 workspace-manager.py ...` (and remember the `chmod +x` if you prefer invoking it raw).

---

*Develop faster, and endow your AI with the exact universal context.* 🚀
