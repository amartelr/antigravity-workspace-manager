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
        """Wizard interactivo"""
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"{Colors.CYAN}{Colors.BOLD}{'═'*70}")
        print("  🧙‍♂️ WORKSPACE WIZARD")
        print(f"{'═'*70}{Colors.ENDC}\n")
        
        ans = {}
        skills = set()
        
        ans['name'] = input(f"{Colors.YELLOW}Nombre: {Colors.ENDC}").strip()
        if not ans['name']:
            print(f"{Colors.RED}Requerido{Colors.ENDC}")
            return
        
        ans['desc'] = input(f"{Colors.YELLOW}Descripción: {Colors.ENDC}").strip()
        
        print(f"\n{Colors.BOLD}Tipo:{Colors.ENDC}")
        types = list(self.skill_database['project_types'].keys())
        for i, t in enumerate(types, 1):
            print(f"  {i}. {t}")
        try:
            choice = int(input(f"{Colors.YELLOW}→ {Colors.ENDC}"))
            if 1 <= choice <= len(types):
                skills.update(self.skill_database['project_types'][types[choice-1]])
        except:
            pass
        
        print(f"\n{Colors.BOLD}Lenguaje:{Colors.ENDC}")
        langs = list(self.skill_database['languages'].keys())
        for i, l in enumerate(langs, 1):
            print(f"  {i}. {l}")
        try:
            choice = int(input(f"{Colors.YELLOW}→ {Colors.ENDC}"))
            if 1 <= choice <= len(langs):
                skills.update(self.skill_database['languages'][langs[choice-1]])
        except:
            pass
        
        print(f"\n{Colors.BOLD}Database:{Colors.ENDC}")
        dbs = list(self.skill_database['databases'].keys())
        for i, d in enumerate(dbs, 1):
            print(f"  {i}. {d}")
        print("  0. Ninguna")
        try:
            choice = int(input(f"{Colors.YELLOW}→ {Colors.ENDC}"))
            if 1 <= choice <= len(dbs):
                skills.update(self.skill_database['databases'][dbs[choice-1]])
        except:
            pass
        
        skills.update(self.skill_database['essential'])
        
        print(f"\n{Colors.BOLD}Skills ({len(skills)}):{Colors.ENDC}\n")
        for s in sorted(skills):
            print(f"  {Colors.GREEN}✓{Colors.ENDC} {s}")
        
        if input(f"\n{Colors.YELLOW}¿Crear? (s/n): {Colors.ENDC}").lower() == 's':
            self.create_workspace(ans['name'], description=ans.get('desc', ''))
            print(f"\n{Colors.YELLOW}Habilitando...{Colors.ENDC}\n")
            for s in skills:
                self.enable_skill(ans['name'], s)
            print(f"\n{Colors.GREEN}{'═'*70}")
            print(f"✅ '{ans['name']}' creado!")
            print(f"{'═'*70}{Colors.ENDC}\n")
            print(f"cd {self.workspaces_dir / ans['name']}")
    
    def _load_skill_database(self):
        return {
            "languages": {
                "Go": ["api-patterns", "backend-patterns", "clean-code", "testing-patterns"],
                "Python": ["python-patterns", "api-patterns", "testing-patterns"],
                "JavaScript/TypeScript": ["nodejs-best-practices", "typescript-expert", "clean-code"],
                "Dart/Flutter": ["flutter-supabase-architect", "mobile-design", "testing-patterns"],
            },
            "project_types": {
                "API Backend": ["api-patterns", "backend-patterns", "api-security-best-practices", "testing-patterns"],
                "Web Frontend": ["frontend-design", "react-patterns", "tailwind-patterns", "testing-patterns"],
                "Full-Stack": ["frontend-design", "backend-patterns", "api-patterns", "testing-patterns"],
                "Mobile App": ["mobile-design", "flutter-supabase-architect", "testing-patterns"],
            },
            "databases": {
                "PostgreSQL": ["database-design", "postgresql-patterns"],
                "MongoDB": ["mongodb-patterns"],
                "Google Sheets": ["api-patterns", "clean-code"],
                "Supabase": ["flutter-supabase-architect", "database-design"],
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
