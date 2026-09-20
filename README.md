# Ritt Agent Skills

Kit personal de skills de ingeniería para **Codex** y **Claude Code**, con filosofía *review-first*. Adaptado de ideas de [mattpocock/skills](https://github.com/mattpocock/skills) y personalizado a mi forma de trabajar: aclaración adaptativa, reutilizar antes de construir, planes con dos opciones, trabajo basado en evidencia, escalera de validación y memoria por proyecto.

> Los prompts pueden escribirse en español con normalidad: el disparo de skills es semántico y funciona aunque el contenido de las skills esté en inglés.

## Garantías del diseño

- Los cambios del upstream **nunca se aplican automáticamente**: la comprobación es de solo lectura y genera un informe para revisar.
- Una comprobación de actualizaciones jamás sobrescribe una skill personalizada; portar una idea del upstream es siempre una edición manual revisada.
- El instalador de proyectos nunca borra archivos: sin `--force` rechaza si hay conflictos; con `--force` respalda primero los archivos en conflicto.
- El Markdown es guía de comportamiento, no una barrera técnica: la seguridad dura va en permisos, hooks y sandboxing de cada herramienta.

## El método: cómo se comporta el agente

Estas son las conductas que el kit impone, con el fichero donde vive cada regla. Casi todas están **repetidas en tres capas** — instrucciones globales (`~/.claude/CLAUDE.md`), contrato por proyecto (`AGENTS.md` + `.agent/rules/`) y skills — para que no dependan de que una sola capa esté activa.

### Es crítico contigo (y consigo mismo)

- **Contradecirte es obligatorio, no opcional**: si el camino que pides no tiene sentido, es inseguro o ya está resuelto, debe decirlo pronto, con evidencia y una alternativa. Vive en las instrucciones globales ("Contradíceme cuando el camino no tenga sentido"), en la sección *Disagreement* del `AGENTS.md` de proyecto ("cumplir en silencio con un mal plan es un modo de fallo") y como paso explícito de [clarify-task](plugins/ritt-engineering/skills/clarify-task/SKILL.md): cuestionar la premisa forma parte de aclarar la tarea.
- **Autocrítica forzada con etiquetas de evidencia** ([certainty-labels](plugins/ritt-engineering/references/certainty-labels.md)): toda afirmación importante lleva `VERIFIED` (observado directamente), `INFERENCE` (se deduce de evidencia), `HYPOTHESIS` (plausible, falta probarlo) o `UNVERIFIED` (sin comprobar). Nunca puede afirmar éxito sin una comprobación observada — un "debería funcionar" es solo `HYPOTHESIS`. Si nueva evidencia contradice algo que dijo antes, debe rebajarlo en voz alta, no en silencio.
- **Se para si el plan choca con la realidad**: [implement-change](plugins/ritt-engineering/skills/implement-change/SKILL.md) le prohíbe improvisar en silencio — si a mitad de implementación descubre que el plan era erróneo, para, lo dice y se ajusta el plan.
- **Revisa su propio trabajo como un escéptico**: [review-change](plugins/ritt-engineering/skills/review-change/SKILL.md) revisa el diff "como un colega al que van a despertar cuando esto se rompa", con hallazgos por severidad (BLOCKER/MAJOR/MINOR/NOTE) — y también al revés: si el cambio está bien, debe decirlo sin inflar hallazgos para justificar la revisión.

### Analiza lo que ya existe antes de partir de 0

- **Inspecciona el estado real primero**: antes de proponer o cambiar nada, lee el repo en el que estás, su estructura, y la memoria del proyecto (`.agent/CONTEXT.md`, el último `.agent/history/YYYY-MM.md` y la ficha activa `.agent/tasks/<id>.md` si existen). Los `KO` del historial evitan repetir intentos que ya fallaron; las decisiones activas del contexto explican por qué las cosas son como son.
- **No reinventa la rueda**: [research-and-reuse](plugins/ritt-engineering/skills/research-and-reuse/SKILL.md) salta automáticamente cuando pides algo nuevo o un plan mete una dependencia nueva, y recorre la escalera **tu repo → librerías de la organización → internet/ecosistema** (contra fuentes primarias: docs oficiales, código fuente, release notes — no blogs). Emite un veredicto **REUSE / ADAPT / BUILD**; si es BUILD, tiene que justificar por qué falla cada candidato existente. Evalúa mantenimiento, licencia, coste de adopción y superficie de seguridad ([reuse-assessment](plugins/ritt-engineering/references/reuse-assessment.md)).
- **El veredicto se guarda** en `.agent/CONTEXT.md` para no repetir la misma investigación en la siguiente sesión.

### Pregunta lo justo, y todo de una vez

[clarify-task](plugins/ritt-engineering/skills/clarify-task/SKILL.md) + [question-policy](plugins/ritt-engineering/references/question-policy.md): presupuesto de preguntas según riesgo (0–3 triviales / ≤10 estándar / ≤20 alto riesgo), en **una única tanda numerada** con un default propuesto por pregunta (puedes contestar "defaults salvo la 3 y la 7"). Prohibido preguntar lo que el repo ya responde. Cierra siempre en un estado explícito: `READY`, `READY WITH ASSUMPTIONS` (lista las suposiciones) o `BLOCKED` (dice qué falta y de quién).

### Decide con dos opciones, no con una ni con cinco

Cuando existe una decisión real, [plan-change](plugins/ritt-engineering/skills/plan-change/SKILL.md) presenta **exactamente dos opciones viables** con coste, riesgos y qué cierra cada una, y recomienda una razonadamente. Si no hay alternativa real, lo dice en vez de inventar una de paja. Los planes van por fases ordenadas por dependencias, cada fase con criterios de aceptación observables y la validación que la demuestra, más lo que **no** debe cambiar y el plan de rollback.

### No da nada por validado sin subir la escalera

[validate-change](plugins/ritt-engineering/skills/validate-change/SKILL.md) + [validation-ladder](plugins/ritt-engineering/references/validation-ladder.md): estática → tests del ámbito afectado → frontera de integración → build → smoke → suite amplia, subiendo tan alto como exija el riesgo (migraciones, seguridad, infra y contratos públicos tienen suelo mínimo). Cada peldaño reporta `PASSED` / `FAILED` (con su salida) / `PARTIAL` / `NOT RUN` (con motivo) / `NOT APPLICABLE` — un paso saltado se declara, nunca se omite en silencio. Descubre los comandos del propio repo; no asume herramientas instaladas.

### Seguridad por defecto y frontera de confirmación

- Al escribir código ([coding rules](plugins/ritt-engineering/assets/project/.agent/rules/coding.md)): sin secretos en código/config/logs, valida entradas externas, queries parametrizadas, mínimo privilegio, defaults seguros. La revisión de seguridad de `review-change` se aplica **siempre**, no solo en "tareas de seguridad".
- Antes de cualquier acción destructiva o con efectos externos pide confirmación explícita e inmediata ([safety-boundaries](plugins/ritt-engineering/references/safety-boundaries.md)): borrados, push/merge/release, deploys, `terraform apply`, mutaciones de Kubernetes/cloud/IAM, secretos, migraciones de datos, dependencias de producción, mensajes/tickets. La aprobación de una acción no se extiende a la siguiente.
- Prohibido debilitar tests, silenciar checks o saltarse salvaguardas para "llegar a verde".
- En Bazel ([stack-bazel](plugins/ritt-engineering/assets/project/.agent/rules/stack-bazel.md)): consultar el grafo antes de editar, respetar macros y `--config`s del repo, y nunca "arreglar" algo desactivando cache o sandbox sin declararlo como hallazgo.

### Memoria y modos

- Toda sesión deja rastro: `history/YYYY-MM.md` (hitos, mensual) y `CONTEXT.md` sobrescrito, más una ficha por tarea en `tasks/` (detalle en la sección de uso).
- Modos de trabajo ([modes](plugins/ritt-engineering/assets/project/.agent/rules/modes.md)): `QUICK` (parche mínimo), `STANDARD` (por defecto), `DEEP` (investigación amplia con trade-offs) y `AUDIT` (solo lectura, cero efectos). Si una tarea QUICK destapa un problema estructural, propone cambiar de modo en vez de ampliar el alcance en silencio.

> **Límite honesto**: todo esto es guía de comportamiento reforzada en tres capas — funciona de forma muy consistente, pero no es una barrera técnica al 100%. La barrera dura son los permisos, hooks (`PreToolUse`) y sandboxing de cada herramienta; por diseño, este kit te recuerda configurarlos y nunca los sustituye.

## Estructura del repositorio

```
plugins/ritt-engineering/        ← la implementación canónica
├── skills/<nombre>/
│   ├── SKILL.md                 ← frontmatter (name, description) + instrucciones
│   └── agents/openai.yaml       ← metadatos y política de invocación para Codex
├── references/                  ← doctrina humana (question-policy, validation-ladder…); NO se carga en runtime — las skills son autocontenidas
└── assets/project/              ← kit que se instala en cada proyecto (ver abajo)

upstream/mattpocock/             ← estado del upstream, solo lectura
├── LOCK.json                    ← revisión aceptada (baseline)
├── TRACKED.json                 ← rutas del upstream que vigilamos
├── CUSTOMIZATIONS.json          ← qué skill local adapta qué fichero del upstream
└── snapshots/<sha>/             ← importaciones inmutables con manifest de hashes

reports/upstream/                ← informes generados (no versionados)
scripts/                         ← mantenimiento: validar, enlazar, gestionar upstream
docs/                            ← arquitectura, autoría de skills, política de upstream, ADRs
```

## Skills

**Auto-invocables** — el agente las carga solo cuando la tarea encaja con su descripción:

| Skill | Qué hace |
| --- | --- |
| [clarify-task](plugins/ritt-engineering/skills/clarify-task/SKILL.md) | Una única tanda numerada de preguntas con defaults propuestos (0–3 triviales / ≤10 estándar / ≤20 alto riesgo). Cierra en `READY` / `READY WITH ASSUMPTIONS` / `BLOCKED`. |
| [research-and-reuse](plugins/ritt-engineering/skills/research-and-reuse/SKILL.md) | Antes de construir: ¿existe ya en el repo → organización → ecosistema? Veredicto REUSE / ADAPT / BUILD. |
| [plan-change](plugins/ritt-engineering/skills/plan-change/SKILL.md) | Plan por fases con criterios de aceptación y exactamente dos opciones + recomendación. Read-only: devuelve el plan; se persiste en la ficha activa `.agent/tasks/<id>.md` solo explícitamente. |
| [implement-change](plugins/ritt-engineering/skills/implement-change/SKILL.md) | Diff mínimo y coherente, patrones del repo, seguridad por defecto. Único escritor del alcance; no encadena validación/revisión/memoria. |
| [diagnose-systematically](plugins/ritt-engineering/skills/diagnose-systematically/SKILL.md) | Causa raíz con evidencia antes de tocar código; separa causa de síntomas. Read-only. |
| [validate-change](plugins/ritt-engineering/skills/validate-change/SKILL.md) | Escalera de validación adaptativa con resultado explícito por peldaño (`PASSED`/`FAILED`/`NOT RUN`…). Read-only. |
| [review-change](plugins/ritt-engineering/skills/review-change/SKILL.md) | Revisión del diff por severidad: corrección, **seguridad** (siempre) y mantenibilidad. Read-only. |

**Manuales** — solo cuando tú las invocas (`/nombre`):

| Skill | Qué hace |
| --- | --- |
| [research-plan-implement](plugins/ritt-engineering/skills/research-plan-implement/SKILL.md) | Orquesta un cambio grande/brownfield en tres fases con contexto aislado (Research → Plan → Implement); la ficha activa `.agent/tasks/<id>.md` es la fuente de verdad y se revisa visualmente con plannotator. Compactación intencional (~40–60%) y subagentes de research read-only. |
| [project-memory](plugins/ritt-engineering/skills/project-memory/SKILL.md) | Único escritor de la memoria `.agent/` (esquema canónico): `history/YYYY-MM.md`, `tasks/<id>.md`, `CONTEXT.md` y `HANDOFF.md`. Manual: solo la invoca el orquestador o tú, nunca una pasada de análisis. |
| [handoff](plugins/ritt-engineering/skills/handoff/SKILL.md) | Compacta la sesión en `.agent/HANDOFF.md` con un prompt listo para el siguiente agente. |
| [setup-project](plugins/ritt-engineering/skills/setup-project/SKILL.md) | Instala y adapta el kit de instrucciones en el proyecto actual. |
| [check-upstream](plugins/ritt-engineering/skills/check-upstream/SKILL.md) | Comprueba si mattpocock/skills tiene novedades y genera un informe. Nunca modifica nada. |

## Instalación

**Enlaces locales (recomendado, vale para ambas herramientas):**

```bash
scripts/link_skills.sh
```

Crea symlinks de cada skill en `~/.claude/skills` y `~/.agents/skills`. Como son enlaces, un `git pull` del repo actualiza las skills instaladas. Re-ejecútalo al añadir o renombrar una skill.

**Como plugin de Claude Code:** este repo es su propio marketplace ([.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)); añádelo como marketplace e instala `ritt-engineering`.

## Uso correcto en el día a día

1. **Trabajo normal**: no hay que invocar nada. Las skills auto-invocables saltan solas — pides algo ambiguo y `clarify-task` te hará su tanda de preguntas; pides "algo nuevo" y `research-and-reuse` comprobará si ya existe; tras implementar, `validate-change` sube la escalera.
2. **Al empezar en un repo nuevo**: `/setup-project` (o `python3 scripts/install_project.py /ruta/al/repo`). Instala `AGENTS.md`, `CLAUDE.md` y `.agent/`, y siembra la memoria inicial.
   - **Uso privado (mi caso por defecto, p. ej. en el monorepo del trabajo)**: NO commitear el kit. Añade sus rutas a `.git/info/exclude` del repo — es un ignore local que no se comparte con nadie (a diferencia de `.gitignore`, que sí se commitea):
     ```
     AGENTS.md
     CLAUDE.md
     .agent/
     .agent-kit-backup/
     ```
     Así el kit y la memoria (`CONTEXT.md`, `history/`, `tasks/`) solo existen en tu máquina y nunca aparecen en `git status` ni en un push.
   - **Uso compartido** (solo si algún día quieres que el equipo herede el mismo contrato): commitear el kit es opcional y una decisión explícita, nunca el paso por defecto.
3. **Al terminar una sesión larga**: `/handoff` deja el estado, riesgos y siguiente prompt en `.agent/HANDOFF.md`.
4. **De vez en cuando (mensual sobra)**: `/check-upstream` para saber si el repo de Matt Pocock tiene cambios que merezcan revisión.

### La memoria por proyecto (`.agent/`)

Esquema canónico v0.4 (detalle en `assets/project/.agent/README.md`):

- **`CONTEXT.md`** — *sobrescrito*: solo el estado que funciona ahora y el porqué breve de cada decisión activa (≤60 líneas). Si un enfoque se supera, se reemplaza.
- **`tasks/<TASK-ID>.md`** — una ficha por tarea: objetivo, hechos verificados, decisiones, plan, intentos (con fingerprints anti-bucle), validación y siguiente paso.
- **`history/YYYY-MM.md`** — *append-only*, un hito por línea, rotación mensual: `- 2026-07-16 | intent: arreglar test flaky | cmd: bazel test //auth/... | result: KO — timeout`. Los `KO` son lo más valioso. No se carga por defecto.
- **`HANDOFF.md`** — último relevo; enlaza CONTEXT + la tarea activa, no los duplica.

Solo el orquestador escribe memoria (skill `project-memory`), nunca en AUDIT. `HISTORY.md`/`PLANS.md`/`RESEARCH.md` son legacy (solo migración). Además `rules/` (modos QUICK/STANDARD/DEEP/AUDIT, coding, validación, seguridad, stacks).

## Flujo de actualizaciones del upstream (review-first)

```bash
python3 scripts/check_upstream.py                     # solo lectura; exit 1 = hay novedades
python3 scripts/import_upstream.py --revision <sha>   # snapshot inmutable del candidato
python3 scripts/compare_upstream.py --candidate <sha> # informe de diferencias vs baseline
python3 scripts/accept_upstream.py --revision <sha> --confirm <sha>  # aceptación explícita
```

Al revisar, `CUSTOMIZATIONS.json` te dice qué skill local podría beneficiarse de cada cambio. Portar algo se hace como cualquier cambio normal (plan → implementación → validación) y se anota en ese mismo fichero. Detalle completo: [docs/UPSTREAM_POLICY.md](docs/UPSTREAM_POLICY.md).

## Mantenimiento del repo

```bash
python3 scripts/validate_repo.py       # estructura, manifests, frontmatter, versiones en sync
claude plugin validate . --strict      # validación oficial de Claude Code
```

Reglas al tocar el repo (las mismas que impone [AGENTS.md](AGENTS.md)):

- Cada skill: frontmatter con `name` = directorio y `description` con condiciones de disparo, más su `agents/openai.yaml`.
- Al cambiar una skill: subir la versión en **los dos** `plugin.json` y en el marketplace (validate_repo lo exige), anotar en [CHANGELOG.md](CHANGELOG.md) y re-sincronizar la tabla de este README.
- Nada escribe nunca contenido del upstream dentro de `plugins/`.

Más documentación: [arquitectura](docs/ARCHITECTURE.md) · [cómo escribir skills](docs/SKILL_AUTHORING.md) · [política de upstream](docs/UPSTREAM_POLICY.md) · [ADRs](docs/adr/).

## Licencia y atribución

Distribuido bajo licencia [MIT](LICENSE) — Copyright (c) 2026 Rittmeyer765.

Incluye y adapta material de [mattpocock/skills](https://github.com/mattpocock/skills) (MIT — Copyright (c) 2026 Matt Pocock). Las adaptaciones propias no eliminan los derechos ni el aviso original. Detalles en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) y `upstream/mattpocock/LICENSE`.
