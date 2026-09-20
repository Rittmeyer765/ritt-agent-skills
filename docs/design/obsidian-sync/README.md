<!-- STATUS: DRAFT · NOT ACTIVE · BLOCKED: missing nine Obsidian notes -->

# Obsidian prompt-sync — design (INACTIVE)

Diseño **no activo**. NADA aquí está conectado a comandos reales ni accede al vault.

- `SPEC.md` — diseño de snapshot local versionado + sync con hash.
- `wrapper-inicio-tarea.DRAFT.md` — ejemplo de wrapper sin ruta absoluta (no instalado).
- `sync_prompts.py.DRAFT.md` — esqueleto de sync (`--check`/`--pull`), NO ejecutable como script aún.

## Bloqueo
Requiere las 9 notas del vault (`Prompts/00 Core` + `1..8`), hoy inaccesibles por TCC
(external sync provider). Hasta auditarlas: duplicación/recursión/seguridad = UNVERIFIED.

## No hacer hasta desbloquear
- No conectar los wrappers a `~/.claude/commands/`.
- No acceder ni escribir en el vault.
- No ejecutar `sync_prompts.py`.
