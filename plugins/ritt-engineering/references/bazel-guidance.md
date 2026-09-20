# Bazel Guidance

When the project builds with Bazel, work with the graph, not around it.

## Understand before editing

- Find what a change affects: `bazel query 'rdeps(//..., //path/to:target)'` (scope the universe on big repos).
- Inspect a target: `bazel query --output=build //path/to:target`; dependencies: `bazel query 'deps(//path/to:target, 1)'`.
- Respect existing macros and shared rule wrappers — if the repo wraps `go_library`/`py_library`, use the wrapper.

## Change discipline

- Keep `BUILD` files minimal and let Gazelle manage them where the repo uses it (`bazel run //:gazelle`) instead of hand-editing.
- New deps go through the repo's dependency mechanism (`MODULE.bazel` / `go.mod` + gazelle update-repos / requirements lock), never ad-hoc.
- Format/lint `BUILD` files with `buildifier` when available.

## Validation

- Test the affected scope first: `bazel test //affected/package/...`; build the artifact: `bazel build //path/to:target`.
- Never "fix" a failure by disabling sandboxing, adding `--nocache_test_results` tricks, tags like `no-remote`, or blanket `--strategy=local` without stating why — cache correctness is a feature.
- A target that only passes with `--test_env` hacks or looser visibility is a finding, not a fix.
- Respect `.bazelrc` configs; use the repo's named configs (`--config=ci`, etc.) rather than inventing flag sets.
