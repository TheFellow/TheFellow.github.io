<!-- Generated from https://thefellow.github.io/articles/indexing-schemas-and-build-declarations-without-executing-the-repository/ by scripts/generate_llm_content.py; do not edit. -->

# Indexing Schemas and Build Declarations Without Executing the Repository

Source: [https://thefellow.github.io/articles/indexing-schemas-and-build-declarations-without-executing-the-repository/](https://thefellow.github.io/articles/indexing-schemas-and-build-declarations-without-executing-the-repository/)

## Pyramid summary

- **~2 words:** Source-only declarations
- **~8 words:** Bounded parsers turn schemas, infrastructure, migrations, and manifests into category-atomic graph evidence.
- **Expanded:** How Weave turns bounded source-only schemas, infrastructure, migrations, and build manifests into category-atomic graph evidence without running their tools.

## Full content

**Part 11 of [Building Weave](/series/weave.md).**

Compiler providers explain what executable source means. The [workspace provider](/articles/making-a-semantic-graph-inspectable.md) explains files, documents, headings, routes, and links. A large repository still carries another layer of knowledge between them: API operations, schema types, migration resources, infrastructure addresses, project identities, dependencies, and explicit generation mappings.

Those declarations are too useful to leave as plain text. They are also not permission to run every tool that understands them. Evaluating a build can execute plugins and targets. Terraform can load providers and state. An OpenAPI loader can follow files or URLs. A migration framework can apply templates or connect to a database. Automatic indexing should not acquire any of those powers merely because a matching file exists.

[Weave](https://github.com/TheFellow/weave) adds one built-in `weave-schema-build` freshness provider for that middle layer. It feeds bounded Git-visible bytes to maintained parsers for Protobuf, OpenAPI 3, GraphQL, PostgreSQL migrations, Terraform HCL, and a deliberately declarative build-manifest subset. The result is ordinary provider-owned graph evidence, so existing context, graph, diff, watch, explorer, export, and CI paths gain the new facts without a second data model or query surface.

The [accepted design record](https://github.com/TheFellow/weave/blob/main/.ai/decisions/0017-source-only-schema-build-provider.md) states the trust and freshness rules, while the [parser research](https://github.com/TheFellow/weave/blob/main/.ai/prior-art/schema-build-providers/README.md) records why each upstream library and exclusion was chosen.

```sh
weave context listPets
weave dependencies example.test/service
weave graph listPets --kind references --kind depends-on
weave symbols aws_instance --json
weave export --json
```

<figure class="article-figure">
  <img src="/assets/images/articles/weave/source-only-schema-build.svg" alt="A bounded inventory supplies Git-visible regular non-symlink bytes without running builds, generators, package managers, Terraform, databases, templates, or network loaders. Six maintained parser lanes cover Protobuf, OpenAPI 3, GraphQL, PostgreSQL migrations, Terraform HCL, and declarative build manifests. One atomic freshness unit per category reuses an unchanged fingerprint or completely relinks a changed category. Malformed cross-file schema categories are omitted with a diagnostic, while one malformed independent build manifest is omitted without hiding valid projects. Normal graph facts then carry declared, generated, inferred, or syntactic evidence through existing context, graph, diff, watch, CI, and explorer consumers; the provider never claims compiler-exact evidence.">
  <figcaption>Maintained parsers recover declared structure. The byte boundary, category units, and evidence classes prevent parser convenience from becoming execution authority.</figcaption>
</figure>

## Establish the byte boundary before choosing a parser

The provider begins with Git's cached and untracked, non-ignored path inventory. It normalizes repository-relative paths, accepts only supported regular files, rejects symlinks, and checks that an opened file still has the identity inspected before the read. The inventory, each source, total corpus, file count, fact count, diagnostics, and parser concurrency all have explicit bounds.

That boundary matters more than whether a parser is written in Go. A library may expose a pure syntax API beside a loader that reads the filesystem, follows a URI, invokes a compiler, or evaluates expressions. Weave supplies already-bounded bytes directly to the syntax or model layer and does not make the loader reachable.

The automatic provider never runs `protoc`, a build, a restore, a package manager, a generator, a template, Terraform, a database, a repository hook, or a network resolver. It does run Git for the same worktree-aware file inventory used by the rest of freshness. The distinction is concrete: Git tells Weave which local source bytes exist; the declared file does not grant its ecosystem permission to do work.

## Reuse ecosystem parsers without adopting their authority

Writing one convenient grammar for six formats would repeat the mistake the adapter boundary avoids for programming languages. Weave instead selects a maintained parser for each declaration family and narrows what enters it.

| Category | Facts retained | Source-only boundary |
| --- | --- | --- |
| Protobuf | packages, messages, fields, enums, services, RPCs, imports, and linked types | Buf protocompile receives an in-memory local corpus plus standard imports, uses at most two workers, and never runs `protoc` or loads a registry |
| OpenAPI 3 | documents, paths, operations, component schemas, properties, and `$ref` relationships | kin-openapi models identifiable version 3 roots while YAML source nodes retain locations; its URI loader is not used |
| GraphQL | SDL types, fields, arguments, enums, operations, fragments, type references, and fragment spreads | gqlparser receives a bounded token stream; queries are validated where a local schema exists but never executed |
| PostgreSQL migrations | migration files, inferred per-directory filename order, schemas, tables, columns, views, indexes, sequences, enums, functions, and supported dependencies | Bytebase Omni parses selected migration files as PostgreSQL; no database or migration engine is contacted |
| Terraform | module directories, resources, data sources, variables, outputs, locals, module calls, providers, and traversals | HashiCorp HCL parses native `.tf` syntax without evaluation, provider schemas, plugins, state, plans, or registry access |
| Build manifests | project identities, explicit dependencies, selected targets, and one proven generation mapping | x/mod, TOML, JSON, and XML parsers read `go.mod`, `Cargo.toml`, `package.json`, Maven POMs, and MSBuild C#/F#/VB project files without invoking their build systems |

The table is also a list of limits. OpenAPI 2 is not silently converted. SQL is not treated as a portable dialect. Terraform JSON and runtime semantics are absent. Imported SDK targets and registry packages remain external. A parser accepting a file is not evidence that Weave understands every construct inside it.

This honesty is visible in diagnostics. A PostgreSQL statement the upstream parser recognizes but the first semantic slice does not model remains in the source and produces a bounded warning. It does not disappear silently, and it does not become a guessed edge.

## Make a complete declaration family the freshness unit

Cross-file schemas are linked systems. A Protobuf import, GraphQL type extension, OpenAPI reference, Terraform module, or local project dependency can change meaning when a different file changes. Reusing facts one file at a time before that dependency surface is proven would make refresh look incremental while retaining stale relationships.

Weave therefore starts with six conservative units, one per category. Each fingerprint covers the provider schema, category name, sorted repository-relative paths, and source content digests. Five categories require a complete cross-file parse. Build manifests are the deliberate exception because each manifest can be parsed independently before exact local project paths are linked across the valid set. The refresh outcomes are still small enough to state precisely:

- An unchanged fingerprint reuses the previous complete unit without invoking its parser and preserves its category diagnostics.
- A changed fingerprint reparses and relinks the complete category, validates the resulting graph batch, and publishes it atomically.
- A malformed or unsupported Protobuf, OpenAPI, GraphQL, PostgreSQL, or Terraform corpus publishes no partial facts, removes only that category's previous unit, and emits a bounded diagnostic.
- A malformed build manifest is diagnosed and excluded while independently valid projects still link and publish together. If every build manifest is invalid, the build category is omitted.
- A fact-over-limit category is omitted. Inventory, file, and corpus limits reject the read before any category parser runs.
- A removed category removes its unit, while every independent category remains available.

This is deliberately broader invalidation than the final system may need. It is also an auditable guarantee: no old GraphQL edge survives a new schema corpus merely because its own file was untouched, while an unrelated broken project fixture cannot erase the valid build graph. Finer parser caches can follow measurement. Complete linked answers come first.

## Resolve a local identity only when source proves it

Stable IDs are separated by provider schema, repository identity, semantic domain, and declared stable name. Repository-relative paths disambiguate file-scoped declarations without embedding an absolute checkout location. That makes a declaration stable across worktrees while preventing an unrelated repository from acquiring the same local identity accidentally.

Resolution is stricter than name matching. A Protobuf type becomes local when linked descriptors prove it. An OpenAPI `$ref` becomes local only when its normalized contained path is already in the Git-visible OpenAPI corpus and its fragment resolves. A build dependency becomes local only when an explicit relative manifest path identifies an indexed project. A static Terraform module source may resolve to an indexed module directory.

Everything else becomes a stable open endpoint. Remote OpenAPI references, standard non-local Protobuf imports, package names, version ranges, provider sources, imported SDK targets, and unproven modules remain traversable identities without pretending their definitions were indexed. A missing non-standard Protobuf import instead makes the linked Protobuf category incomplete. Absolute, backslash, root-escaping, missing, and remote OpenAPI references produce diagnostics and never trigger an opportunistic read.

The rule prevents two opposite errors. Weave does not discard a useful declared dependency merely because its target lives elsewhere, and it does not collapse unrelated declarations because their short names happen to match.

## Keep evidence narrower than parser success

A maintained parser can establish structure without establishing compiler truth. The new provider never emits `exact` evidence.

| Evidence | What it means here |
| --- | --- |
| `declared` | A schema, migration, infrastructure file, or manifest states the entity or relationship |
| `generated` | An MSBuild item explicitly pairs `AutoGen=true` with `DependentUpon`, proving one source/output mapping |
| `inferred` | Sorted filenames establish useful migration topology inside one directory, without claiming the SQL or an unselected migration engine declared that order |
| `syntactic` | Executable GraphQL syntax exposes a relationship that is not promoted to compiler-resolved truth |
| `exact` | Never claimed by this provider |

Even successful GraphQL validation does not turn an executable selection into compiler evidence. Migration filename order remains inferred because no selected engine has established its execution semantics. Likewise, a Protobuf option that conventionally influences a generated filename does not prove that the generator ran or where its output landed. Generation needs an explicit source/output declaration, not an ecosystem convention.

The same restraint excludes Gradle and CMake from the first build set. Their common files are executable DSLs whose accurate graphs depend on evaluation. A future maintained source-only representation or an explicitly permissioned adapter may support them. A regex approximation inside the automatic core would erase the boundary this provider exists to preserve.

## Publish ordinary graph facts

Each parser produces normal documents, symbols, occurrences, source ranges, and edges through the shared relationship builder. The provider owns those facts, but its edges may point at workspace path identities, another local declaration, or an open endpoint. It never writes discovered relationships into `.weave/bridges.json`; authored intent and rebuildable automatic evidence remain separate owners.

That choice makes the feature larger than a schema listing command without making the CLI larger. `weave context listPets` can join an OpenAPI operation to its current source excerpt and adjacent schema. `weave graph` can render the same reference edge as DOT. A project dependency can participate in impact, architecture policy, semantic diff, catalog federation, and the local explorer because those consumers already understand the common graph and evidence model.

The end-to-end test follows that public route. It initializes a real Git repository containing an OpenAPI document, runs an ordinary index, asks `context --json` for `listPets`, then asks `graph --kind references` for the neighborhood connecting the operation and `Pet`. The parser implementation is not the integration point. The graph contract is.

This fills an important space without turning Weave into six new runtimes. Compiler facts still own executable semantics. Workspace facts still own repository topology and content. Authored bridges still own reviewed human intent. The schema/build provider adds what inert declarations can prove, stops where evaluation would begin, and lets every existing graph consumer do the rest.
