# .agent — memoria técnica operativa (esquema canónico v0.4)

```
.agent/
├── CONTEXT.md            # estado actual (sobrescrito, ≤60 líneas)
├── tasks/<TASK-ID>.md    # una ficha por tarea (research+plan+intentos+validación)
├── history/YYYY-MM.md    # un hito por línea, rotación mensual
├── HANDOFF.md            # snapshot de relevo, enlaza (no duplica)
└── README.md             # este esquema
```

Reglas:
- **Solo el orquestador escribe** memoria compartida (skill `project-memory`); en hitos o handoff, nunca en AUDIT.
- Sin secretos, sin PII, sin salidas largas. Lenguaje claro legible por humanos.
- `CONTEXT.md` se sobrescribe (≤60 líneas/8 KiB). `tasks/<id>.md` ≤100 líneas/16 KiB.
- `history/` no se carga por defecto; se consulta por task_id/error/fingerprint.
- Decisiones de peso arquitectónico → `docs/adr/`.

## Regla anti-bucle (fingerprints), en cada `tasks/<id>.md`
`attempt | hypothesis | action_fingerprint | input_changed | result | evidence | next`
- No repetir un `action_fingerprint` sin cambiar hipótesis, entrada o entorno.
- Máx. 2 intentos por hipótesis; máx. 3 sin progreso observable.
- Al límite: hipótesis discriminante, preguntar, o cerrar `BLOCKED`.
- Un OK sin evidencia observada se registra como `UNVERIFIED`.

## Legacy (solo migración)
`HISTORY.md`, `PLANS.md`, `RESEARCH.md` son formato antiguo. Se reconocen para migrar, pero
**ninguna escritura nueva** debe crearlos: usa `history/YYYY-MM.md` y `tasks/<id>.md`.
