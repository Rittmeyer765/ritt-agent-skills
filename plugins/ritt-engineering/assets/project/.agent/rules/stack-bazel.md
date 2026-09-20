# Stack: Bazel

- Query before editing: `bazel query 'rdeps(//..., //pkg:target)'` to see the blast radius; `bazel query --output=build //pkg:target` to inspect.
- Use the repo's macros and rule wrappers; regenerate BUILD files with Gazelle where the repo uses it instead of hand-editing.
- New dependencies go through `MODULE.bazel` / the repo's lock mechanism, never ad-hoc.
- Validate the affected scope: `bazel test //affected/...`, then `bazel build` the artifact.
- Never bypass the cache or sandbox to make something pass (`no-remote` tags, `--strategy=local`, `--nocache_test_results`) without flagging it as a finding.
- Respect `.bazelrc` and use the repo's named `--config`s; format BUILD files with `buildifier`.
