#!/usr/bin/env python3
"""
validate_plugin.py — my-marketplace 插件结构校验脚本

实现 V1-V6 自动化检查（V7 为判断型检查，由 Claude 执行）。

用法:
    python validate_plugin.py                    # 校验所有 plugin
    python validate_plugin.py --scope mp-dev     # 仅校验 mp-dev
    python validate_plugin.py --scope marketplace # 仅校验仓库级
    python validate_plugin.py --root /path/to/my-marketplace  # 指定项目根
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


class ValidationResult:
    """单条校验结果"""

    def __init__(self, rule_id: str, name: str, status: str, message: str = ""):
        self.rule_id = rule_id
        self.name = name
        self.status = status  # PASS, FAIL, WARN, SKIP
        self.message = message

    def __str__(self):
        line = f"[{self.rule_id}][{self.status}] {self.name}"
        if self.message:
            line += f" — {self.message}"
        return line


class PluginValidator:
    """my-marketplace 插件结构校验器"""

    REQUIRED_PLUGIN_JSON_FIELDS = ["name", "description", "version", "author", "license", "skills"]
    REQUIRED_MARKETPLACE_FIELDS = ["name", "owner", "metadata", "plugins"]
    REQUIRED_PLUGIN_FILES = [
        ".claude-plugin/plugin.json",
        "CLAUDE.md",
        "README.md",
        "CHANGELOG.md",
    ]
    REQUIRED_PLUGIN_DIRS = ["skills"]

    def __init__(self, project_root: Path, scope: Optional[str] = None):
        self.root = project_root
        self.scope = scope
        self.results: list[ValidationResult] = []

    def find_project_root(self) -> Path:
        """Auto-detect project root by looking for .claude-plugin/marketplace.json"""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".claude-plugin" / "marketplace.json").exists():
                return current
            current = current.parent
        return Path.cwd()

    def add_result(self, rule_id: str, name: str, status: str, message: str = ""):
        self.results.append(ValidationResult(rule_id, name, status, message))

    def get_plugin_dirs(self) -> list[Path]:
        """Get list of plugin directories to validate"""
        plugins_dir = self.root / "plugins"
        if not plugins_dir.exists():
            return []

        if self.scope and self.scope != "marketplace":
            target = plugins_dir / self.scope
            if target.exists():
                return [target]
            return []

        return sorted([d for d in plugins_dir.iterdir() if d.is_dir()])

    def validate_v1_plugin_json(self):
        """V1: Validate plugin.json schema"""
        for plugin_dir in self.get_plugin_dirs():
            plugin_name = plugin_dir.name
            pj_path = plugin_dir / ".claude-plugin" / "plugin.json"

            if not pj_path.exists():
                self.add_result("V1", "plugin.json schema", "FAIL",
                                f"plugins/{plugin_name}/.claude-plugin/plugin.json not found")
                continue

            try:
                with open(pj_path, encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                self.add_result("V1", "plugin.json schema", "FAIL",
                                f"plugins/{plugin_name}/.claude-plugin/plugin.json invalid JSON: {e}")
                continue

            missing = [field for field in self.REQUIRED_PLUGIN_JSON_FIELDS if field not in data]
            if missing:
                for field in missing:
                    self.add_result("V1", "plugin.json schema", "FAIL",
                                    f"plugins/{plugin_name}/.claude-plugin/plugin.json missing required field: {field}")
            else:
                self.add_result("V1", "plugin.json schema", "PASS",
                                f"{plugin_name} — all 6 required fields present")

    def validate_v2_directory_structure(self):
        """V2: Validate directory structure"""
        for plugin_dir in self.get_plugin_dirs():
            plugin_name = plugin_dir.name
            errors = []

            for req_file in self.REQUIRED_PLUGIN_FILES:
                if not (plugin_dir / req_file).exists():
                    errors.append(f"missing required file: {req_file}")

            for req_dir in self.REQUIRED_PLUGIN_DIRS:
                if not (plugin_dir / req_dir).is_dir():
                    errors.append(f"missing required directory: {req_dir}")

            if errors:
                for err in errors:
                    self.add_result("V2", "Directory structure", "FAIL",
                                    f"plugins/{plugin_name} {err}")
            else:
                self.add_result("V2", "Directory structure", "PASS",
                                f"{plugin_name} — all required files and directories present")

    def validate_v3_skill_frontmatter(self):
        """V3: Validate SKILL.md frontmatter"""
        for plugin_dir in self.get_plugin_dirs():
            plugin_name = plugin_dir.name
            skills_dir = plugin_dir / "skills"

            if not skills_dir.exists():
                continue

            skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir()])

            if not skill_dirs:
                self.add_result("V3", "SKILL.md frontmatter", "WARN",
                                f"{plugin_name} — no skill directories found")
                continue

            all_pass = True
            for skill_dir in skill_dirs:
                dir_name = skill_dir.name

                # Skip *-shared directories
                if dir_name.endswith("-shared"):
                    self.add_result("V3", "SKILL.md frontmatter", "SKIP",
                                    f"{dir_name} (shared resource, not a skill)")
                    continue

                skill_file = skill_dir / "SKILL.md"
                if not skill_file.exists():
                    self.add_result("V3", "SKILL.md frontmatter", "FAIL",
                                    f"plugins/{plugin_name}/skills/{dir_name}/ missing SKILL.md")
                    all_pass = False
                    continue

                # Read first 20 lines to check frontmatter
                with open(skill_file, encoding="utf-8") as f:
                    head_lines = []
                    for i, line in enumerate(f):
                        if i >= 20:
                            break
                        head_lines.append(line)

                head_text = "".join(head_lines)
                missing_fields = []

                if not re.search(r"^name:", head_text, re.MULTILINE):
                    missing_fields.append("name")
                if not re.search(r"^description:", head_text, re.MULTILINE):
                    missing_fields.append("description")

                if missing_fields:
                    for field in missing_fields:
                        self.add_result("V3", "SKILL.md frontmatter", "FAIL",
                                        f"plugins/{plugin_name}/skills/{dir_name}/SKILL.md missing frontmatter field: {field}")
                    all_pass = False

            if all_pass:
                self.add_result("V3", "SKILL.md frontmatter", "PASS",
                                f"{plugin_name} — all SKILL.md files have required frontmatter")

    def validate_v4_marketplace_json(self):
        """V4: Validate marketplace.json consistency"""
        if self.scope and self.scope != "marketplace":
            # Skip marketplace-level checks for plugin-scoped validation
            return

        mj_path = self.root / ".claude-plugin" / "marketplace.json"

        if not mj_path.exists():
            self.add_result("V4", "marketplace.json", "FAIL",
                            ".claude-plugin/marketplace.json not found")
            return

        try:
            with open(mj_path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.add_result("V4", "marketplace.json", "FAIL",
                            f".claude-plugin/marketplace.json invalid JSON: {e}")
            return

        # Check required fields
        missing = [f for f in self.REQUIRED_MARKETPLACE_FIELDS if f not in data]
        if missing:
            for field in missing:
                self.add_result("V4", "marketplace.json", "FAIL",
                                f"marketplace.json missing required field: {field}")
            return

        # Check plugin directory existence
        errors = []
        for plugin_entry in data.get("plugins", []):
            name = plugin_entry.get("name", "")
            if not (self.root / "plugins" / name).is_dir():
                errors.append(
                    f"marketplace.json references plugin '{name}' but directory plugins/{name}/ not found")

        if errors:
            for err in errors:
                self.add_result("V4", "marketplace.json", "FAIL", err)
        else:
            self.add_result("V4", "marketplace.json", "PASS",
                            "all referenced plugins have corresponding directories")

    def validate_v5_version_sync(self):
        """V5: Validate version consistency"""
        mj_path = self.root / ".claude-plugin" / "marketplace.json"
        if not mj_path.exists():
            self.add_result("V5", "Version sync", "FAIL",
                            "marketplace.json not found, cannot verify versions")
            return

        with open(mj_path, encoding="utf-8") as f:
            mj_data = json.load(f)

        # Check marketplace-level version sync (VERSION <-> marketplace.json metadata.version)
        if not self.scope or self.scope == "marketplace":
            version_file = self.root / "VERSION"
            if version_file.exists():
                file_version = version_file.read_text(encoding="utf-8").strip()
                mj_version = mj_data.get("metadata", {}).get("version", "")

                if file_version != mj_version:
                    self.add_result("V5", "Version sync", "FAIL",
                                    f"VERSION ({file_version}) != marketplace.json metadata.version ({mj_version})")
                else:
                    self.add_result("V5", "Version sync", "PASS",
                                    f"marketplace version {file_version} consistent")

        # Check plugin-level version sync
        for plugin_dir in self.get_plugin_dirs():
            plugin_name = plugin_dir.name
            pj_path = plugin_dir / ".claude-plugin" / "plugin.json"

            if not pj_path.exists():
                continue

            with open(pj_path, encoding="utf-8") as f:
                pj_data = json.load(f)

            pj_version = pj_data.get("version", "")

            # Find matching entry in marketplace.json
            mj_plugin_version = None
            for entry in mj_data.get("plugins", []):
                if entry.get("name") == plugin_name:
                    mj_plugin_version = entry.get("version", "")
                    break

            if mj_plugin_version is None:
                self.add_result("V5", "Version sync", "WARN",
                                f"{plugin_name} not found in marketplace.json plugins array")
            elif pj_version != mj_plugin_version:
                self.add_result("V5", "Version sync", "FAIL",
                                f"{plugin_name} plugin.json ({pj_version}) != marketplace.json ({mj_plugin_version})")
            else:
                self.add_result("V5", "Version sync", "PASS",
                                f"{plugin_name} version {pj_version} consistent")

    def validate_v6_changelog(self):
        """V6: Validate CHANGELOG existence"""
        # Root CHANGELOG
        if not self.scope or self.scope == "marketplace":
            root_changelog = self.root / "CHANGELOG.md"
            if root_changelog.exists():
                self.add_result("V6", "CHANGELOG existence", "PASS",
                                "Root CHANGELOG.md present")
            else:
                self.add_result("V6", "CHANGELOG existence", "FAIL",
                                "Root CHANGELOG.md not found")

        # Plugin CHANGELOGs
        for plugin_dir in self.get_plugin_dirs():
            plugin_name = plugin_dir.name
            changelog = plugin_dir / "CHANGELOG.md"

            if changelog.exists():
                self.add_result("V6", "CHANGELOG existence", "PASS",
                                f"plugins/{plugin_name}/CHANGELOG.md present")
            else:
                self.add_result("V6", "CHANGELOG existence", "FAIL",
                                f"plugins/{plugin_name}/CHANGELOG.md not found")

    def run_all(self):
        """Run all validation checks"""
        self.validate_v1_plugin_json()
        self.validate_v2_directory_structure()
        self.validate_v3_skill_frontmatter()
        self.validate_v4_marketplace_json()
        self.validate_v5_version_sync()
        self.validate_v6_changelog()

    def print_report(self):
        """Print structured validation report"""
        scope_label = self.scope or "all"

        # Count results
        pass_count = sum(1 for r in self.results if r.status == "PASS")
        fail_count = sum(1 for r in self.results if r.status == "FAIL")
        warn_count = sum(1 for r in self.results if r.status == "WARN")
        skip_count = sum(1 for r in self.results if r.status == "SKIP")

        print()
        print("=" * 60)
        print("  mp-dev:validate — Structure Validation Report")
        print("=" * 60)
        print(f"  Scope: {scope_label}")
        print(f"  Project: {self.root}")
        print("-" * 60)

        # Group by rule_id
        current_rule = ""
        for result in self.results:
            if result.rule_id != current_rule:
                current_rule = result.rule_id
                print()

            status_marker = {
                "PASS": "  PASS",
                "FAIL": "  FAIL",
                "WARN": "  WARN",
                "SKIP": "  SKIP",
            }.get(result.status, "  ????")

            print(f"  [{result.rule_id}]{status_marker}  {result.message}")

        print()
        print("-" * 60)
        print(f"  Total: {pass_count} PASS / {fail_count} FAIL / {warn_count} WARN / {skip_count} SKIP")
        print("=" * 60)
        print()

        return fail_count == 0


def main():
    parser = argparse.ArgumentParser(
        description="my-marketplace plugin structure validator (V1-V6)"
    )
    parser.add_argument(
        "--scope",
        type=str,
        default=None,
        help='Validation scope: plugin name (e.g. "mp-dev") or "marketplace" for repo-level only',
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Project root path (auto-detected if not specified)",
    )
    args = parser.parse_args()

    # Determine project root
    if args.root:
        project_root = Path(args.root)
    else:
        # Auto-detect: walk up from cwd looking for .claude-plugin/marketplace.json
        current = Path.cwd()
        project_root = None
        while current != current.parent:
            if (current / ".claude-plugin" / "marketplace.json").exists():
                project_root = current
                break
            current = current.parent

        if project_root is None:
            print("ERROR: Could not auto-detect project root.")
            print("       Looking for .claude-plugin/marketplace.json in parent directories.")
            print("       Use --root to specify the project root explicitly.")
            sys.exit(2)

    if not project_root.exists():
        print(f"ERROR: Project root does not exist: {project_root}")
        sys.exit(2)

    validator = PluginValidator(project_root, scope=args.scope)
    validator.run_all()
    success = validator.print_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
