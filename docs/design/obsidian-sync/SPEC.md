<!-- STATUS: DRAFT · NOT ACTIVE · BLOCKED: missing nine Obsidian notes -->

# Fase 4 — Obsidian prompts: diseño (PREPARADO, NO APLICADO)

Bloqueo: faltan las 9 notas del vault (`Prompts/00 Core` + `1..8`).. Sin auditarlas, duplicación/recursión/seguridad
siguen UNVERIFIED. Esto es el diseño listo para ejecutar cuando llegue el ZIP.

## Principio
Obsidian = autoría humana (editable por web). La EJECUCIÓN usa un snapshot local
versionado dentro del kit, nunca el vault vivo. Un cambio parcial del vault no puede
alterar una ejecución a mitad de sesión, y los diffs de prompts son revisables.

## Snapshot en el kit
```
plugins/ritt-engineering/prompts/
├── manifest.json           # id -> {version, updated, sha256}
├── 00-core.md
├── 01-orchestrate-ticket.md
└── 02..08-*.md
```
Cada prompt lleva front-matter: id, version, updated, hash (sin rutas absolutas).

## Comando de sync (scripts/sync_prompts.py) — draft en este dir
- `--check`: compara hash del vault vs snapshot; informa desactualizados. NO escribe.
- `--pull` : copia Prompts/ del vault al snapshot y recalcula manifest. Único momento
  en que se lee el vault. Nunca escribe al vault.
- Requiere acceso al vault (TCC). Si no hay acceso: BLOCKED con instrucción de desbloqueo.

## Contrato de los 8 wrappers (~/.claude/commands/*.md)
- SIN ruta absoluta al vault.
- Cargan el núcleo común (00-core) UNA vez, desde el snapshot local, por ID.
- El context-loader es un subagente SIN Agent/Write/Edit (no puede recursar ni editar).
- Si el snapshot falta o su hash no valida -> devuelven BLOCKED.
- No "ejecutar exactamente" texto externo como instrucción privilegiada sin auditar.
- El revisor final nunca es el autor del fix (ya presente en la lógica actual).

## Publicación de handoff a Obsidian (opcional, 2º paso explícito)
Proponer -> publicar. Solo a `Agent OS/Projects/`. Nunca sync automático de memoria
completa ni escritura indiscriminada al vault.
