Explicit Architecture, with a Go Accent
Original diagrams by Ryan Harris, September 12, 2026.

Article: https://thefellow.github.io/articles/explicit-architecture-with-a-go-accent/
Source baseline: https://github.com/TheFellow/go-modular-monolith/tree/a7c2efda8c0cd905089a27060242ff841bb0ad41

01-boundaries.svg: three adapters and the common application boundary.
02-domain-slice.svg: public contracts, private writes, and checked visibility.
03-transaction.svg: execution order, per-event preparation, transaction ownership.
04-foundations.svg: values, mechanisms, independent toolkits, concrete wiring.
05-complete.svg: full architecture atlas, linked to implementation evidence.
05-complete.pdf: printable vector export of the complete atlas.

Solid blue arrows show selected dependency / contract use. Dashed amber arrows
show execution. The circles group responsibilities; they are not a literal
package import graph. Named mechanisms and generated application wiring are
shown separately because a pkg prefix does not establish independence.

Open an SVG directly to follow its linked source panels. SVGs embedded as images
in an article do not activate those internal links. The article includes ordinary
links to the same implementation and tests for accessibility and Markdown readers.

Generate SVGs from the repository root (Python standard library only):
  python3 scripts/generate_explicit_architecture.py

Export the poster as a vector PDF, keeping CairoSVG's dependency environment
outside the repository:
  uv run --with cairosvg==2.8.2 python -c "import cairosvg; cairosvg.svg2pdf(url='assets/diagrams/explicit-architecture/05-complete.svg', write_to='assets/diagrams/explicit-architecture/05-complete.pdf')"

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
