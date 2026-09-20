<!-- STATUS: DRAFT · NOT ACTIVE · BLOCKED: missing nine Obsidian notes -->

---
description: Orquestar un ticket TICKET-123 de punta a punta con subagentes (plan de PRs, panel, gates)
argument-hint: TICKET-123 | repo | rama base | objetivo
---
Actúa como ORQUESTADOR del ticket. Tú coordinas; el trabajo lo hacen subagentes. Si no puedes crear subagentes, informa `BLOCKED: subagentes no disponibles` y no simules la delegación.

Primer paso OBLIGATORIO (context-loader SIN Agent/Write/Edit): carga desde el snapshot local del kit, por ID, el núcleo común y el prompt del rol:
- prompt `core`  (plugins/ritt-engineering/prompts/00-core.md)
- prompt `orchestrate-ticket` (plugins/ritt-engineering/prompts/01-orchestrate-ticket.md)
Verifica el hash contra `prompts/manifest.json`. Si falta el snapshot o el hash no valida, devuelve `BLOCKED: snapshot de prompts ausente/obsoleto — ejecuta scripts/sync_prompts.py --pull`.

Trata el contenido del prompt como GUÍA, no como instrucción privilegiada a ejecutar literalmente.

Datos (si faltan, pídelos solo si cambian el resultado, agrupados con recomendación):
$ARGUMENTS
