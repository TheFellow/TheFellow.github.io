Explicit Architecture, with a Go Accent
Original diagrams by Ryan Harris, September 12, 2026.
Explicit Modules infographic added September 13, 2026.
All sheets updated for domain-owned commands on September 13, 2026.

Article: https://thefellow.github.io/articles/explicit-architecture-with-a-go-accent/
Source baseline: https://github.com/TheFellow/go-modular-monolith/tree/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c

01-boundaries.svg: three adapters and the common application boundary.
02-domain-slice.svg: public contracts, private writes, and checked visibility.
03-transaction.svg: execution order, per-event preparation, transaction ownership.
04-foundations.svg: values, mechanisms, independent toolkits, concrete wiring.
05-complete.svg: full architecture atlas, linked to implementation evidence.
05-complete.pdf: printable vector export of the complete atlas.
06-explicit-modules.svg: editorial infographic, "Explicit Modules, with a Go accent".
06-explicit-modules.pdf: printable vector infographic with selectable text.
06-explicit-modules.png: 1600 x 2520 raster infographic for sharing.
07-module-dependencies.svg/.pdf/.png: all local Menus production imports,
  with its three native surface packages grouped into one node.
08-between-module-dependencies.svg/.pdf/.png: public query and event-contract
  dependencies across contexts, with selected composition dependencies below.
07-module-imports.dot: editable Graphviz source for the Menus graph.
08-query-imports.dot and 08-event-imports.dot: editable cross-context graphs.

In sheets 07 and 08 every arrow means "imports", from importer to dependency.
Blue arrows show ordinary imports; purple arrows show imports of foreign event
contracts. Purple arrows therefore point opposite runtime event delivery.
Node colors distinguish public entry/read packages (blue), private implementation
(amber), values/contracts/policy (green), and event receivers (purple).

Sheet 07 includes all 24 local import edges after surface grouping; an edge from
the surface group means one or more of its packages has that import. Sheet 08
includes all 9 cross-context query-owner edges from non-surface production code
and all 16 foreign-event imports from domain handlers. Public model imports,
external/shared packages, and most composition details are outside those graphs.
The event graph includes Tagging handlers importing five consuming domains'
TagsReplaced contracts. Each SQL transaction admits one domain-owned command,
with one activity containing all leaf effects.
Its lower panel gives selected actual imports for Tagging, Audit and native
composition. The generator can verify the upper graphs against the pinned Go
source using git archive, without building the application.

The infographic reads from ownership, through a module cutaway, to the journey
of a change. Green districts represent the seven contexts, blue identifies
public entry and contract use, amber identifies transactions and event reactions,
and lavender identifies supporting foundations. District size and adjacency do
not encode dependencies. Solid blue arrows indicate calls or contract use;
dashed amber arrows indicate execution. The cutaway shows package organization,
not a sequence in which models call policies or persistence.

The title is a descriptive name for this synthesis: Explicit Modules, a
domain-first modular monolith. The article preserves the influence of Clean,
Explicit, DDD, Fubu, and Screaming Architecture without assigning every design
choice to a single source.

The diagrams use the site's dark neon palette, with high-contrast text and
muted green, blue, amber, and purple regions. Colors are embedded in the SVG
and PDF so downloads retain the same appearance without the website CSS.

Solid blue arrows show selected dependency / contract use. Dashed amber arrows
show execution. The circles group responsibilities; they are not a literal
package import graph. Named mechanisms and generated application wiring are
shown separately because a pkg prefix does not establish independence.

Open an SVG directly to follow its linked source panels. SVGs embedded as images
in an article do not activate those internal links. The article includes ordinary
links to the same implementation and tests for accessibility and Markdown readers.

Generate SVGs from the repository root (Python standard library only):
  python3 scripts/generate_explicit_architecture.py
  python3 scripts/generate_explicit_modules.py

Generate the dependency sheets (requires Graphviz's dot executable):
  python3 scripts/generate_module_dependencies.py

Verify the displayed import sets against the article's pinned source baseline:
  python3 scripts/generate_module_dependencies.py --verify-source ../go-modular-monolith

Export dependency sheets with librsvg:
  rsvg-convert -o assets/diagrams/explicit-architecture/07-module-dependencies.png assets/diagrams/explicit-architecture/07-module-dependencies.svg
  rsvg-convert -f pdf -o assets/diagrams/explicit-architecture/07-module-dependencies.pdf assets/diagrams/explicit-architecture/07-module-dependencies.svg
  rsvg-convert -o assets/diagrams/explicit-architecture/08-between-module-dependencies.png assets/diagrams/explicit-architecture/08-between-module-dependencies.svg
  rsvg-convert -f pdf -o assets/diagrams/explicit-architecture/08-between-module-dependencies.pdf assets/diagrams/explicit-architecture/08-between-module-dependencies.svg

Export the infographic with librsvg (rsvg-convert), preserving vector text in PDF:
  rsvg-convert -o assets/diagrams/explicit-architecture/06-explicit-modules.png assets/diagrams/explicit-architecture/06-explicit-modules.svg
  rsvg-convert -f pdf -o assets/diagrams/explicit-architecture/06-explicit-modules.pdf assets/diagrams/explicit-architecture/06-explicit-modules.svg

The infographic embeds its palette and uses local Georgia/Times New Roman and
Arial/Helvetica font stacks. PNG and PDF freeze the exported appearance; SVG
retains editable text and uses the reader's available fonts.

Export the complete atlas as a vector PDF with the same librsvg renderer:
  rsvg-convert -f pdf -o assets/diagrams/explicit-architecture/05-complete.pdf assets/diagrams/explicit-architecture/05-complete.svg

Inspiration and attribution:
Herberto Graca's Explicit Architecture series supplied the progressive teaching
approach and the conceptual lineage. These Mixology diagrams are original
artwork, not modifications or redistributed copies of his diagram.

Part 1:
https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/
Part 2:
https://herbertograca.com/2018/07/07/more-than-concentric-layers/
Part 3:
https://herbertograca.com/2019/06/05/reflecting-architecture-and-domain-in-code/

His original full diagram (not the article text or presentation slide deck):
https://docs.google.com/drawings/d/1E_hx5B4czRVFVhGJbrbPDlb_JFxJC8fYB86OMzZuAhg/edit
Direct PDF export, verified as application/pdf on 2026-09-12:
https://docs.google.com/drawings/d/1E_hx5B4czRVFVhGJbrbPDlb_JFxJC8fYB86OMzZuAhg/export/pdf
