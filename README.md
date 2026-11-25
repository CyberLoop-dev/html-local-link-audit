<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:0d9488&height=160&section=header&text=HTML%20Local%20Link%20Audit&fontSize=29&fontColor=ffffff" alt="HTML Local Link Audit header"/></p>
<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&pause=1000&color=5EEAD4&center=true&vCenter=true&width=760&lines=Find+broken+local+HTML+links+and+fragment+targets" alt="Animated tagline"/></p>
<p align="center"><a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0d9488.svg" alt="MIT"/></a> <img src="https://img.shields.io/badge/language-Python-2563eb.svg" alt="Python"/> <img src="https://img.shields.io/github/stars/CyberLoop-dev/html-local-link-audit?style=flat" alt="Stars"/> <img src="https://img.shields.io/github/last-commit/CyberLoop-dev/html-local-link-audit?style=flat" alt="Last commit"/></p>
<p align="center"><img src="assets/mark.svg" width="110" alt="Custom project mark"/></p>

## 🧭 Overview
A read-only Python CLI for checking local HTML links and asset references. It resolves relative and site-root paths, verifies local files, and checks fragment identifiers in HTML targets. External URLs are never fetched.

## ✨ Features
- 🔗 Check local href and src references in one HTML file or a directory tree
- ⚓ Verify fragment IDs for local HTML targets
- 🛡️ Report references that resolve outside the selected site root
- 📄 Print concise text output or machine-readable JSON

## 🎬 Demo
Run the command against a folder containing HTML files. No hosted demo is claimed.

## 🚀 Quick Start
```bash
python html_link_audit.py ./site
```
Use `--json` for structured output. The original files are never modified.

## 🧰 Tech Stack
- 🧩 Python 3.11+ standard library
- 🔒 Read-only local scanning; no network requests
- 📦 No third-party dependencies

## 🗂️ Folder Structure
```text
html-local-link-audit/
├── assets/mark.svg
├── html_link_audit.py
├── test_html_link_audit.py
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

## 🛣️ Roadmap
- [ ] Add srcset candidate checks
- [ ] Add a GitHub Actions-friendly summary format

## 🤝 Contributing
Issues and pull requests are welcome. Include a small fixture site for new parsing behavior.

## 📄 License
Released under the [MIT License](LICENSE).

<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d9488,100:111827&height=105&section=footer" alt="Animated wave footer"/></p>