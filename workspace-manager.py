#!/usr/bin/env python3
"""
===============================================================================
WORKSPACE MANAGER - Sistema Completo de Gestión de Workspaces y Skills
===============================================================================

✨ FUNCIONA DESDE CUALQUIER UBICACIÓN ✨

Soporta:
  /Users/alfredomartel/dev/antigravity/workspace-manager.py
  /Users/alfredomartel/dev/antigravity/workspaces/workspace-manager.py

Detecta automáticamente la raíz del proyecto y ajusta todas las rutas.

Uso: python3 workspace-manager.py wizard

Autor: Sistema de Gestión de Skills para Agentes IA
Versión: 2.1 - Auto-detección de rutas
===============================================================================
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Set, Optional
import argparse

# ============================================================================
# COLORES
# ============================================================================

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ============================================================================
# DETECCIÓN AUTOMÁTICA DE RUTAS
# ============================================================================

def detect_project_root() -> Path:
    """Detecta la raíz del proyecto automáticamente"""
    current = Path(__file__).resolve().parent
    
    # Caso 1: Ya estamos en la raíz
    if (current / ".agent").exists() or (current / "workspaces").exists():
        return current
    
    # Caso 2: Buscar hacia arriba
    for _ in range(5):
        if current.name == "workspaces":
            return current.parent
        parent = current.parent
        if (parent / ".agent").exists() or (parent / "workspaces").exists():
            return parent
        current = parent
    
    return Path(__file__).resolve().parent

# ============================================================================
# WORKSPACE MANAGER
# ============================================================================

class WorkspaceManager:
    def __init__(self):
        self.root_dir = detect_project_root()
        self.skills_dir = self.root_dir / ".agent" / "skills"
        self.workspaces_dir = self.root_dir / "workspaces"
        self.templates_dir = self.root_dir / "skill-config-templates"
        self.backup_dir = self.root_dir / ".agent" / "skills_backup"
        self.skill_database = self._load_skill_database()
    
    def initialize_project(self, force: bool = False):
        """Inicializa estructura"""
        print(f"{Colors.BLUE}🚀 Inicializando...{Colors.ENDC}")
        print(f"{Colors.CYAN}📁 Raíz: {self.root_dir}{Colors.ENDC}\n")
        
        for dir_path in [
            self.skills_dir / "public",
            self.skills_dir / "private", 
            self.skills_dir / "user",
            self.workspaces_dir,
            self.templates_dir
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ {dir_path.relative_to(self.root_dir)}")
        
        if not (self.skills_dir / "public" / "docx").exists() or force:
            print(f"\n{Colors.YELLOW}📦 Clonando skills...{Colors.ENDC}")
            try:
                temp = self.skills_dir / "temp_clone"
                subprocess.run([
                    "git", "clone",
                    "https://github.com/sickn33/antigravity-awesome-skills.git",
                    str(temp)
                ], check=True, capture_output=True)
                
                if (temp / "skills").exists():
                    for item in (temp / "skills").iterdir():
                        if item.is_dir():
                            dest = self.skills_dir / "public" / item.name
                            shutil.copytree(item, dest, dirs_exist_ok=True)
                shutil.rmtree(temp)
                print(f"{Colors.GREEN}✅ Skills clonados{Colors.ENDC}")
            except:
                print(f"{Colors.RED}⚠️  Error al clonar{Colors.ENDC}")
        
        self._create_templates()
        print(f"\n{Colors.GREEN}✨ Inicializado!{Colors.ENDC}")
    
    def _create_templates(self):
        templates = {
            "frontend-bundle.json": {
                "name": "Frontend Bundle",
                "enabled_skills": ["frontend-design", "react-patterns", "tailwind-patterns", "testing-patterns"]
            },
            "backend-bundle.json": {
                "name": "Backend Bundle",
                "enabled_skills": ["api-patterns", "backend-patterns", "testing-patterns", "clean-code"]
            },
            "mobile-bundle.json": {
                "name": "Mobile Bundle",
                "enabled_skills": ["flutter-supabase-architect", "mobile-design", "testing-patterns"]
            }
        }
        for name, config in templates.items():
            path = self.templates_dir / name
            if not path.exists():
                with open(path, 'w') as f:
                    json.dump(config, f, indent=2)
    
    def create_workspace(self, name: str, template: Optional[str] = None, description: str = ""):
        """Crea workspace"""
        path = self.workspaces_dir / name
        if path.exists():
            print(f"{Colors.RED}❌ Ya existe{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}🏗️  Creando: {name}{Colors.ENDC}")
        
        path.mkdir(parents=True)
        agent = path / ".agent"
        agent.mkdir()
        
        # Symlink
        try:
            link = agent / "skills"
            rel = os.path.relpath(self.skills_dir, agent)
            link.symlink_to(rel)
            print(f"✅ Symlink: {rel}")
        except:
            print(f"{Colors.YELLOW}⚠️  Symlink error (Windows: ejecutar como admin){Colors.ENDC}")
        
        # Config
        config = {
            "name": name,
            "description": description,
            "enabled_skills": [],
            "disabled_skills": [],
            "skill_priority": {}
        }
        
        if template:
            t = self.templates_dir / f"{template}.json"
            if t.exists():
                with open(t) as f:
                    config['enabled_skills'] = json.load(f).get('enabled_skills', [])
        
        with open(path / "skill-config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        # README
        script_rel = os.path.relpath(Path(__file__), path)
        with open(path / "README.md", 'w') as f:
            f.write(f"""# {name}

{description}

## Skills

```bash
# Using the wsm alias (recommended):
wsm list-skills {name}
wsm enable {name} skill-name

# Or using the direct path:
python3 {script_rel} list-skills {name}
```

## Prompt Antigravity

```
Workspace: {name}
Carga skills de ./skill-config.json
Confirma qué tienes activo.
```
""")
        
        print(f"{Colors.GREEN}✅ Creado: {path.relative_to(self.root_dir)}{Colors.ENDC}")
        return True
    
    def list_workspaces(self):
        """Lista workspaces"""
        if not self.workspaces_dir.exists():
            print(f"{Colors.RED}❌ No hay workspaces{Colors.ENDC}")
            return
        
        ws = [d for d in self.workspaces_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        if not ws:
            print(f"{Colors.YELLOW}📭 No hay workspaces{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}📂 Workspaces ({len(ws)}):{Colors.ENDC}\n")
        for w in sorted(ws):
            cfg = w / "skill-config.json"
            if cfg.exists():
                with open(cfg) as f:
                    c = json.load(f)
                    print(f"  {Colors.CYAN}•{Colors.ENDC} {w.name:20}")
                    if c.get('description'):
                        print(f"    {c['description']}")
                    print(f"    Skills: {len(c.get('enabled_skills', []))}\n")
    
    def enable_skill(self, workspace: str, skill: str):
        """Habilita skill"""
        cfg = self.workspaces_dir / workspace / "skill-config.json"
        if not cfg.exists():
            print(f"{Colors.RED}❌ Workspace no encontrado{Colors.ENDC}")
            return False
        
        with open(cfg) as f:
            c = json.load(f)
        
        if skill in c.get('enabled_skills', []):
            print(f"{Colors.YELLOW}⚠️  Ya habilitado{Colors.ENDC}")
            return False
        
        c.setdefault('enabled_skills', []).append(skill)
        if skill in c.get('disabled_skills', []):
            c['disabled_skills'].remove(skill)
        
        with open(cfg, 'w') as f:
            json.dump(c, f, indent=2)
        
        print(f"{Colors.GREEN}✅ Habilitado: {skill} en {workspace}{Colors.ENDC}")
        return True
    
    def disable_skill(self, workspace: str, skill: str):
        """Deshabilita skill"""
        cfg = self.workspaces_dir / workspace / "skill-config.json"
        if not cfg.exists():
            print(f"{Colors.RED}❌ Workspace no encontrado{Colors.ENDC}")
            return False
        
        with open(cfg) as f:
            c = json.load(f)
        
        if skill not in c.get('enabled_skills', []):
            print(f"{Colors.YELLOW}⚠️  No habilitado{Colors.ENDC}")
            return False
        
        c['enabled_skills'].remove(skill)
        with open(cfg, 'w') as f:
            json.dump(c, f, indent=2)
        
        print(f"{Colors.GREEN}✅ Deshabilitado: {skill} de {workspace}{Colors.ENDC}")
        return True
    
    def list_workspace_skills(self, workspace: str):
        """Lista skills de workspace"""
        cfg = self.workspaces_dir / workspace / "skill-config.json"
        if not cfg.exists():
            print(f"{Colors.RED}❌ No encontrado{Colors.ENDC}")
            return
        
        with open(cfg) as f:
            c = json.load(f)
        
        skills = c.get('enabled_skills', [])
        print(f"\n{Colors.BOLD}📊 {workspace} ({len(skills)} skills):{Colors.ENDC}\n")
        for s in sorted(skills):
            print(f"  {Colors.GREEN}✓{Colors.ENDC} {s}")
        print()
    
    def sync_from_github(self, auto_fix: bool = False):
        """Sincroniza desde GitHub"""
        print(f"\n{Colors.BLUE}🔄 Sincronizando...{Colors.ENDC}\n")
        
        if self.skills_dir.exists():
            print(f"{Colors.YELLOW}💾 Backup...{Colors.ENDC}")
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            shutil.copytree(self.skills_dir, self.backup_dir)
            print(f"{Colors.GREEN}✅ Backup creado{Colors.ENDC}\n")
        
        temp = self.root_dir / ".agent" / "temp_sync"
        try:
            if temp.exists():
                shutil.rmtree(temp)
            
            print(f"{Colors.YELLOW}📦 Descargando...{Colors.ENDC}")
            subprocess.run([
                "git", "clone", "--depth", "1",
                "https://github.com/sickn33/antigravity-awesome-skills.git",
                str(temp)
            ], check=True, capture_output=True)
            
            if (temp / "skills").exists():
                pub = self.skills_dir / "public"
                pub.mkdir(parents=True, exist_ok=True)
                
                new = upd = 0
                for item in (temp / "skills").iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dest = pub / item.name
                        if dest.exists():
                            shutil.rmtree(dest)
                            upd += 1
                        else:
                            new += 1
                        shutil.copytree(item, dest)
                
                print(f"{Colors.GREEN}✅ Nuevos: {new}, Actualizados: {upd}{Colors.ENDC}")
            
            shutil.rmtree(temp)
            
            if auto_fix:
                self._fix_broken()
            
            print(f"\n{Colors.GREEN}✨ Sincronizado!{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            return False
    
    def _fix_broken(self):
        """Repara skills rotos"""
        available = self._get_available_skills()
        broken = {}
        
        for w in self._get_workspaces():
            cfg = w / "skill-config.json"
            if not cfg.exists():
                continue
            with open(cfg) as f:
                c = json.load(f)
            bad = [s for s in c.get('enabled_skills', []) if s not in available]
            if bad:
                broken[w.name] = bad
        
        if broken:
            print(f"\n{Colors.YELLOW}⚠️  Skills rotos:{Colors.ENDC}\n")
            for ws, skills in broken.items():
                print(f"  {ws}:")
                for s in skills:
                    print(f"    {Colors.RED}❌{Colors.ENDC} {s}")
                    self.disable_skill(ws, s)
    
    def run_wizard(self):
        """Wizard interactivo mejorado"""
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"{Colors.CYAN}{Colors.BOLD}{'═'*70}")
        print("  🧙‍♂️ WORKSPACE WIZARD")
        print(f"{'═'*70}{Colors.ENDC}\n")
        
        ans = {}
        skills = set()
        selected_type = None
        selected_lang = None
        selected_db = None
        
        # ── Paso 1: Nombre ──
        ans['name'] = input(f"{Colors.YELLOW}📝 Nombre: {Colors.ENDC}").strip()
        if not ans['name']:
            print(f"{Colors.RED}❌ Requerido{Colors.ENDC}")
            return
        
        ans['desc'] = input(f"{Colors.YELLOW}📄 Descripción: {Colors.ENDC}").strip()
        
        # ── Paso 2: Tipo de Proyecto ──
        print(f"\n{Colors.BOLD}{'─'*50}")
        print(f"  📦 Tipo de Proyecto")
        print(f"{'─'*50}{Colors.ENDC}")
        types = list(self.skill_database['project_types'].keys())
        for i, t in enumerate(types, 1):
            print(f"  {Colors.CYAN}{i:2}.{Colors.ENDC} {t}")
        try:
            choice = int(input(f"\n{Colors.YELLOW}  → {Colors.ENDC}"))
            if 1 <= choice <= len(types):
                selected_type = types[choice-1]
                skills.update(self.skill_database['project_types'][selected_type])
                print(f"  {Colors.GREEN}✓ {selected_type}{Colors.ENDC}")
        except:
            pass
        
        # ── Paso 3: Lenguaje ──
        print(f"\n{Colors.BOLD}{'─'*50}")
        print(f"  💻 Lenguaje de Programación")
        print(f"{'─'*50}{Colors.ENDC}")
        langs = list(self.skill_database['languages'].keys())
        for i, l in enumerate(langs, 1):
            print(f"  {Colors.CYAN}{i:2}.{Colors.ENDC} {l}")
        try:
            choice = int(input(f"\n{Colors.YELLOW}  → {Colors.ENDC}"))
            if 1 <= choice <= len(langs):
                selected_lang = langs[choice-1]
                skills.update(self.skill_database['languages'][selected_lang])
                print(f"  {Colors.GREEN}✓ {selected_lang}{Colors.ENDC}")
        except:
            pass
        
        # ── Paso 4: Base de Datos ──
        print(f"\n{Colors.BOLD}{'─'*50}")
        print(f"  🗄️  Base de Datos")
        print(f"{'─'*50}{Colors.ENDC}")
        dbs = list(self.skill_database['databases'].keys())
        for i, d in enumerate(dbs, 1):
            print(f"  {Colors.CYAN}{i:2}.{Colors.ENDC} {d}")
        print(f"  {Colors.CYAN} 0.{Colors.ENDC} Ninguna")
        try:
            choice = int(input(f"\n{Colors.YELLOW}  → {Colors.ENDC}"))
            if 1 <= choice <= len(dbs):
                selected_db = dbs[choice-1]
                skills.update(self.skill_database['databases'][selected_db])
                print(f"  {Colors.GREEN}✓ {selected_db}{Colors.ENDC}")
        except:
            pass
        
        # ── Paso 5: Skills Adicionales (multi-select) ──
        print(f"\n{Colors.BOLD}{'─'*50}")
        print(f"  🧩 Skills Adicionales (selección múltiple)")
        print(f"{'─'*50}{Colors.ENDC}")
        
        # Build suggested skills based on previous selections
        suggested = self._get_suggested_skills(selected_type, selected_lang, selected_db)
        
        # Remove skills already selected
        suggested = {cat: [s for s in slist if s not in skills] 
                     for cat, slist in suggested.items()}
        suggested = {cat: slist for cat, slist in suggested.items() if slist}
        
        if suggested:
            print(f"  {Colors.CYAN}Basado en tu selección, te pueden ser útiles:{Colors.ENDC}\n")
            
            # Flatten all suggested skills into a numbered list
            flat_skills = []
            for cat, slist in suggested.items():
                print(f"  {Colors.BOLD}▸ {cat}:{Colors.ENDC}")
                for s in slist:
                    flat_skills.append(s)
                    print(f"    {Colors.CYAN}{len(flat_skills):2}.{Colors.ENDC} {s}")
                print()
            
            print(f"  {Colors.YELLOW}Introduce los números separados por coma (ej: 1,3,5)")
            print(f"  o 'all' para todos, Enter para ninguno{Colors.ENDC}")
            
            try:
                sel = input(f"\n{Colors.YELLOW}  → {Colors.ENDC}").strip()
                if sel.lower() == 'all':
                    skills.update(flat_skills)
                    print(f"  {Colors.GREEN}✓ Todos los skills añadidos ({len(flat_skills)}){Colors.ENDC}")
                elif sel:
                    indices = [int(x.strip()) for x in sel.split(',') if x.strip()]
                    added = 0
                    for idx in indices:
                        if 1 <= idx <= len(flat_skills):
                            skills.add(flat_skills[idx-1])
                            added += 1
                    print(f"  {Colors.GREEN}✓ {added} skills añadidos{Colors.ENDC}")
            except:
                pass
        else:
            print(f"  {Colors.CYAN}No hay sugerencias adicionales{Colors.ENDC}")
        
        # Add essential skills
        skills.update(self.skill_database['essential'])
        
        # ── Resumen Final ──
        print(f"\n{Colors.BOLD}{'═'*70}")
        print(f"  📋 RESUMEN")
        print(f"{'═'*70}{Colors.ENDC}\n")
        print(f"  {Colors.BOLD}Nombre:{Colors.ENDC}      {ans['name']}")
        if ans.get('desc'):
            print(f"  {Colors.BOLD}Descripción:{Colors.ENDC} {ans['desc']}")
        if selected_type:
            print(f"  {Colors.BOLD}Tipo:{Colors.ENDC}        {selected_type}")
        if selected_lang:
            print(f"  {Colors.BOLD}Lenguaje:{Colors.ENDC}    {selected_lang}")
        if selected_db:
            print(f"  {Colors.BOLD}Database:{Colors.ENDC}    {selected_db}")
        
        print(f"\n  {Colors.BOLD}Skills ({len(skills)}):{Colors.ENDC}\n")
        for s in sorted(skills):
            print(f"    {Colors.GREEN}✓{Colors.ENDC} {s}")
        
        print()
        if input(f"  {Colors.YELLOW}¿Crear workspace? (s/n): {Colors.ENDC}").lower() == 's':
            self.create_workspace(ans['name'], description=ans.get('desc', ''))
            print(f"\n{Colors.YELLOW}  Habilitando skills...{Colors.ENDC}\n")
            for s in skills:
                self.enable_skill(ans['name'], s)
            print(f"\n{Colors.GREEN}{'═'*70}")
            print(f"  ✅ Workspace '{ans['name']}' creado con {len(skills)} skills!")
            print(f"{'═'*70}{Colors.ENDC}\n")
            print(f"  cd {self.workspaces_dir / ans['name']}")
            print()
    
    def _get_suggested_skills(self, project_type, language, database):
        """Genera sugerencias de skills basadas en las selecciones del wizard"""
        suggestions = {}
        
        # ── Skills de Arquitectura y Calidad ──
        arch_quality = []
        if project_type in ["API Backend", "Full-Stack", "Microservicios"]:
            arch_quality.extend(["architecture", "architecture-patterns", "architecture-decision-records",
                                 "software-architecture", "microservices-patterns", "code-review-excellence"])
        elif project_type in ["Web Frontend", "Web App (SPA)"]:
            arch_quality.extend(["frontend-design", "web-design-guidelines", "ui-ux-designer"])
        elif project_type == "Mobile App":
            arch_quality.extend(["app-store-optimization", "mobile-developer"])
        
        if project_type:
            arch_quality.extend(["clean-code", "code-reviewer", "architect-review"])
        arch_quality = list(dict.fromkeys(arch_quality))  # deduplicate preserving order
        if arch_quality:
            suggestions["🏗️  Arquitectura y Calidad"] = arch_quality
        
        # ── Skills de Testing ──
        testing = []
        if language == "Python":
            testing.extend(["python-testing-patterns", "tdd-workflow"])
        elif language == "JavaScript/TypeScript":
            testing.extend(["javascript-testing-patterns", "playwright-skill", "e2e-testing-patterns"])
        elif language == "Go":
            testing.extend(["tdd-workflow", "e2e-testing-patterns"])
        elif language == "Dart/Flutter":
            testing.extend(["tdd-workflow", "test-driven-development"])
        elif language == "Rust":
            testing.extend(["tdd-workflow"])
        elif language == "Java/Kotlin":
            testing.extend(["tdd-workflow", "e2e-testing-patterns"])
        
        if project_type in ["Web Frontend", "Full-Stack", "Web App (SPA)"]:
            if "playwright-skill" not in testing:
                testing.append("playwright-skill")
            if "e2e-testing-patterns" not in testing:
                testing.append("e2e-testing-patterns")
        
        testing.extend(["test-automator", "systematic-debugging"])
        testing = list(dict.fromkeys(testing))
        if testing:
            suggestions["🧪 Testing y Debugging"] = testing
        
        # ── Skills de DevOps/Deploy ──
        devops = []
        if project_type in ["API Backend", "Full-Stack", "Microservicios", "Web App (SPA)"]:
            devops.extend(["docker-expert", "github-actions-templates", "deployment-engineer"])
        if project_type == "Microservicios":
            devops.extend(["kubernetes-architect", "k8s-manifest-generator", "terraform-specialist"])
        if project_type in ["Web Frontend", "Web App (SPA)"]:
            devops.extend(["vercel-deployment"])
        devops.extend(["cicd-automation-workflow-automate"])
        devops = list(dict.fromkeys(devops))
        if devops:
            suggestions["🚀 DevOps y Deploy"] = devops
        
        # ── Skills de Seguridad ──
        security = []
        if project_type in ["API Backend", "Full-Stack", "Microservicios"]:
            security.extend(["api-security-best-practices", "backend-security-coder", 
                             "security-auditor", "auth-implementation-patterns"])
        elif project_type in ["Web Frontend", "Web App (SPA)"]:
            security.extend(["frontend-security-coder", "top-web-vulnerabilities"])
        elif project_type == "Mobile App":
            security.extend(["mobile-security-coder"])
        if security:
            suggestions["🔒 Seguridad"] = security
        
        # ── Skills de AI/ML ──
        if project_type in ["AI/ML", "Data Engineering"]:
            ai_skills = ["prompt-engineering", "llm-app-patterns", "rag-implementation",
                         "langchain-architecture", "langgraph", "ai-engineer",
                         "embedding-strategies", "vector-database-engineer"]
            suggestions["🤖 AI/ML"] = ai_skills
        
        # ── Skills de SEO/Marketing ──
        if project_type in ["SEO/Marketing", "Web Frontend", "Full-Stack", "Web App (SPA)"]:
            seo = ["seo-fundamentals", "seo-content-writer", "seo-meta-optimizer",
                   "analytics-tracking", "seo-structure-architect"]
            if project_type == "SEO/Marketing":
                seo.extend(["seo-keyword-strategist", "seo-audit", "programmatic-seo",
                            "content-marketer", "social-content"])
            suggestions["📈 SEO y Marketing"] = seo
        
        # ── Skills de Automatización ──
        if project_type in ["CLI/Automatización", "Data Engineering"]:
            auto = ["workflow-automation", "n8n-mcp-tools-expert", "zapier-make-patterns"]
            if language == "Python":
                auto.extend(["async-python-patterns", "python-performance-optimization"])
            suggestions["⚡ Automatización"] = auto
        
        # ── Skills de Game Dev ──
        if project_type == "Game Dev":
            game = ["unity-developer", "unity-ecs-patterns", "unreal-engine-cpp-pro",
                    "godot-gdscript-patterns", "threejs-skills", "game-development"]
            suggestions["🎮 Game Dev"] = game
        
        # ── Skills de Blockchain ──
        if project_type == "Blockchain/Web3":
            web3 = ["blockchain-developer", "solidity-security", "nft-standards",
                    "defi-protocol-templates", "web3-testing"]
            suggestions["⛓️  Blockchain/Web3"] = web3
        
        # ── Skills de Database avanzados ──
        if database:
            db_advanced = []
            if database in ["PostgreSQL", "Supabase", "Neon Postgres"]:
                db_advanced.extend(["database-optimizer", "sql-optimization-patterns",
                                    "database-migration", "database-architect"])
            elif database == "MongoDB/NoSQL":
                db_advanced.extend(["nosql-expert", "database-architect"])
            elif database == "Redis":
                db_advanced.extend(["database-architect"])
            if database == "Supabase":
                db_advanced.extend(["supabase-automation", "nextjs-supabase-auth"])
            if db_advanced:
                suggestions["🗃️  Database Avanzado"] = db_advanced
        
        # ── Skills de Documentación ──
        docs = ["api-documentation-generator", "readme"]
        if project_type in ["API Backend", "Full-Stack", "Microservicios"]:
            docs.append("openapi-spec-generation")
        suggestions["📝 Documentación"] = docs
        
        return suggestions

    def _load_skill_database(self):
        return {
            "languages": {
                "Python": ["python-patterns", "python-pro", "api-patterns", "testing-patterns"],
                "JavaScript/TypeScript": ["nodejs-best-practices", "typescript-expert", "typescript-pro", "javascript-pro", "clean-code"],
                "Go": ["golang-pro", "go-concurrency-patterns", "api-patterns", "clean-code", "testing-patterns"],
                "Dart/Flutter": ["flutter-expert", "mobile-design", "testing-patterns"],
                "Rust": ["rust-pro", "rust-async-patterns", "clean-code", "testing-patterns"],
                "Java/Kotlin": ["java-pro", "api-patterns", "clean-code", "testing-patterns"],
                "C#/.NET": ["csharp-pro", "dotnet-backend", "dotnet-backend-patterns", "clean-code", "testing-patterns"],
                "C/C++": ["c-pro", "cpp-pro", "clean-code", "testing-patterns"],
                "Swift/SwiftUI": ["swiftui-expert-skill", "ios-developer", "mobile-design", "testing-patterns"],
                "Ruby": ["ruby-pro", "api-patterns", "clean-code", "testing-patterns"],
                "PHP": ["php-pro", "laravel-expert", "api-patterns", "testing-patterns"],
                "Elixir": ["elixir-pro", "api-patterns", "clean-code", "testing-patterns"],
                "Scala": ["scala-pro", "api-patterns", "clean-code", "testing-patterns"],
                "Julia": ["julia-pro", "clean-code", "testing-patterns"],
                "Haskell": ["haskell-pro", "clean-code", "testing-patterns"],
            },
            "project_types": {
                "API Backend": ["api-patterns", "api-design-principles", "backend-architect", "api-security-best-practices", "testing-patterns"],
                "Web Frontend": ["frontend-design", "frontend-developer", "react-patterns", "tailwind-patterns", "web-design-guidelines", "testing-patterns"],
                "Full-Stack": ["frontend-design", "backend-architect", "api-patterns", "senior-fullstack", "testing-patterns"],
                "Web App (SPA)": ["frontend-design", "react-patterns", "react-best-practices", "react-state-management", "tailwind-patterns", "testing-patterns"],
                "Mobile App": ["mobile-design", "mobile-developer", "flutter-expert", "testing-patterns"],
                "CLI/Automatización": ["workflow-automation", "bash-pro", "clean-code", "testing-patterns"],
                "Microservicios": ["microservices-patterns", "api-patterns", "docker-expert", "kubernetes-architect", "testing-patterns"],
                "AI/ML": ["ai-engineer", "llm-app-patterns", "prompt-engineering", "rag-implementation", "testing-patterns"],
                "Data Engineering": ["data-engineer", "database-design", "database-architect", "sql-pro", "testing-patterns"],
                "DevOps/Infra": ["docker-expert", "kubernetes-architect", "terraform-specialist", "cloud-architect", "github-actions-templates"],
                "Game Dev": ["game-development", "unity-developer", "threejs-skills", "testing-patterns"],
                "SEO/Marketing": ["seo-fundamentals", "seo-content-writer", "analytics-tracking", "programmatic-seo", "content-marketer"],
                "Security/Pentesting": ["security-auditor", "pentest-checklist", "ethical-hacking-methodology", "vulnerability-scanner", "top-web-vulnerabilities"],
                "Blockchain/Web3": ["blockchain-developer", "solidity-security", "web3-testing", "nft-standards"],
            },
            "databases": {
                "PostgreSQL": ["database-design", "postgres-best-practices", "postgresql", "sql-optimization-patterns"],
                "Supabase": ["supabase-automation", "database-design", "nextjs-supabase-auth"],
                "MongoDB/NoSQL": ["nosql-expert", "database-design"],
                "MySQL": ["database-design", "sql-pro", "sql-optimization-patterns"],
                "SQLite": ["database-design", "sql-pro"],
                "Redis": ["database-design"],
                "Firebase": ["firebase", "database-design"],
                "Neon Postgres": ["neon-postgres", "database-design", "postgres-best-practices", "using-neon"],
                "Google Sheets": ["api-patterns", "googlesheets-automation", "clean-code"],
                "Elasticsearch": ["database-design", "database-architect"],
                "DynamoDB": ["aws-skills", "database-design", "nosql-expert"],
            },
            "essential": ["clean-code", "testing-patterns", "git-pushing"]
        }
    
    def _get_workspaces(self):
        if not self.workspaces_dir.exists():
            return []
        return [d for d in self.workspaces_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    def _get_available_skills(self):
        skills = set()
        for cat in ['public', 'private', 'user']:
            p = self.skills_dir / cat
            if p.exists():
                for d in p.iterdir():
                    if d.is_dir() and (d / "SKILL.md").exists():
                        skills.add(d.name)
        return skills

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Workspace Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 workspace-manager.py init
  python3 workspace-manager.py wizard
  python3 workspace-manager.py list
  python3 workspace-manager.py enable ytmusic api-patterns
  python3 workspace-manager.py sync --auto-fix

Funciona desde cualquier ubicación - detecta rutas automáticamente.
        """
    )
    
    sub = parser.add_subparsers(dest='command')
    
    sub.add_parser('init').add_argument('--force', action='store_true')
    sub.add_parser('wizard')
    
    c = sub.add_parser('create')
    c.add_argument('name')
    c.add_argument('-t', '--template')
    c.add_argument('-d', '--description', default='')
    
    sub.add_parser('list')
    
    ls = sub.add_parser('list-skills')
    ls.add_argument('workspace', nargs='?')
    
    en = sub.add_parser('enable')
    en.add_argument('workspace')
    en.add_argument('skill')
    
    dis = sub.add_parser('disable')
    dis.add_argument('workspace')
    dis.add_argument('skill')
    
    sync = sub.add_parser('sync')
    sync.add_argument('--auto-fix', action='store_true')
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    m = WorkspaceManager()
    
    if args.command == 'init':
        m.initialize_project(args.force)
    elif args.command == 'wizard':
        m.run_wizard()
    elif args.command == 'create':
        m.create_workspace(args.name, args.template, args.description)
    elif args.command == 'list':
        m.list_workspaces()
    elif args.command == 'list-skills':
        if args.workspace:
            m.list_workspace_skills(args.workspace)
        else:
            skills = m._get_available_skills()
            print(f"\n{Colors.BOLD}Skills ({len(skills)}):{Colors.ENDC}\n")
            for s in sorted(skills):
                print(f"  • {s}")
            print()
    elif args.command == 'enable':
        m.enable_skill(args.workspace, args.skill)
    elif args.command == 'disable':
        m.disable_skill(args.workspace, args.skill)
    elif args.command == 'sync':
        m.sync_from_github(args.auto_fix)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Cancelado{Colors.ENDC}")
        sys.exit(0)
