#!/usr/bin/env python3
"""Draw the Explicit Modules infographic using only the Python standard library.

The SVG is self-contained, has selectable text, and links to the article's pinned
source baseline. Export commands for PNG and PDF live in the diagram README.
"""

from html import escape
from generate_explicit_architecture import CODE, OUT, SHA


INK = '#fff6ed'
MUTED = '#c1c6c4'
FAINT = '#8c9996'
BG = '#141817'
LINE = '#39433f'
GREEN = '#84e5b9'
BLUE = '#8bcafb'
GOLD = '#f4c879'
PURPLE = '#c8b1f1'


class Poster:
    def __init__(self, height=2520, title='Explicit Modules, with a Go accent', description=None):
        description = description or (
            'A map of Mixology, a domain-first modular monolith. Three native surfaces '
            'call public Go operations. Seven bounded contexts own their capabilities. Public queries '
            'and owner-local events connect contexts; writes remain private. A command, prepared leaf '
            'reactions, and success audit share one SQLite transaction. Shared values, mechanisms, '
            'and explicit wiring support the modules; types and architecture tests enforce boundaries. '
            f'Original infographic by Ryan Harris. Source baseline {SHA}.')
        self.parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="1600" height="{height}" viewBox="0 0 1600 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="desc">{escape(description)}</desc>',
            '<defs>',
            '<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">'
            '<circle cx="1" cy="1" r="0.8" fill="#64766c" opacity="0.20"/></pattern>',
            '<linearGradient id="domain" x2="1" y2="1"><stop stop-color="#203b31"/>'
            '<stop offset="1" stop-color="#1b2b25"/></linearGradient>',
            '<linearGradient id="transaction"><stop stop-color="#30291f"/>'
            '<stop offset="1" stop-color="#211f1a"/></linearGradient>',
            *[f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
              f'markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1 L9 5 L1 9" '
              f'fill="none" stroke="{color}" stroke-width="1.5"/></marker>'
              for name, color in [('blue', BLUE), ('gold', GOLD)]],
            '</defs>',
            '<style>text{font-family:Arial,Helvetica,sans-serif} '
            '.serif{font-family:Georgia,"Times New Roman",serif} '
            '.mono{font-family:Menlo,Consolas,monospace} '
            'a:hover .district{stroke:#fff6ed;stroke-width:2} '
            'a:focus .district{stroke:#fff6ed;stroke-width:3}</style>',
        ]
        self.rect(0, 0, 1600, height, BG, radius=0, stroke='none')
        self.rect(0, 0, 1600, height, 'url(#grid)', radius=0, stroke='none')

    def rect(self, x, y, w, h, fill='none', stroke=LINE, radius=16, extra=''):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                          f'fill="{fill}" stroke="{stroke}" {extra}/>')

    def text(self, x, y, value, size=22, color=INK, weight=400, cls='', anchor='start', extra=''):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
                          f'font-weight="{weight}" class="{cls}" text-anchor="{anchor}" '
                          f'{extra}>{escape(value)}</text>')

    def lines(self, x, y, lines, size=22, color=MUTED, leading=30):
        for i, line in enumerate(lines):
            self.text(x, y + i * leading, line, size, color)

    def path(self, d, color=LINE, width=2, extra=''):
        self.parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" '
                          f'fill="none" stroke-linecap="round" stroke-linejoin="round" {extra}/>')

    def circle(self, x, y, r, fill, stroke='none'):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')

    def arrow(self, d, kind='blue'):
        self.path(d, BLUE if kind == 'blue' else GOLD, 2,
                  f'marker-end="url(#arrow-{kind})"' + (' stroke-dasharray="6 6"' if kind == 'gold' else ''))

    def link(self, path):
        url = escape(CODE + path, quote=True)
        self.parts.append(f'<a href="{url}" xlink:href="{url}" target="_blank">')

    def endlink(self):
        self.parts.append('</a>')

    def section(self, y, number, label, title, color):
        self.circle(91, y - 7, 19, color)
        self.text(91, y - 1, number, 17, BG, 700, anchor='middle')
        self.text(125, y, label, 17, color, 700, extra='letter-spacing="2.5"')
        self.text(72, y + 47, title, 35, INK, 500, cls='serif')

    def icon(self, x, y, name, color=GREEN, scale=1):
        # Original line illustrations, in a shared 48-unit coordinate space.
        shapes = {
            'leaf': ['M12 38 C9 10 24 6 40 7 C43 24 31 37 12 38 Z', 'M10 42 L32 16', 'M20 30 L19 20', 'M26 23 L34 23'],
            'drink': ['M6 9 H42 L24 28 Z', 'M24 28 V42 M14 42 H34', 'M12 15 H36', 'M31 12 L38 3'],
            'stock': ['M6 17 L24 7 L42 17 V37 L24 47 L6 37 Z', 'M6 17 L24 27 L42 17 M24 27 V47', 'M15 12 L33 22 V30'],
            'menu': ['M8 6 H31 L40 15 V44 H8 Z', 'M30 6 V16 H40', 'M15 24 H32 M15 31 H32 M15 38 H26'],
            'order': ['M10 5 H38 V45 L31 41 L24 45 L17 41 L10 45 Z', 'M17 15 H31 M17 23 H31', 'M17 32 L22 36 L31 28'],
            'audit': ['M7 10 H34 V44 H7 Z', 'M15 19 H27 M15 27 H27 M15 35 H22', 'M30 6 L36 2 L42 6 V22 L36 27 L30 22 Z'],
            'tag': ['M6 6 H25 L45 26 L26 45 L6 25 Z', 'M14 15 A2 2 0 1 0 18 15 A2 2 0 1 0 14 15'],
            'cli': ['M4 8 H44 V40 H4 Z', 'M11 17 L18 23 L11 29 M24 30 H34'],
            'tui': ['M4 8 H44 V40 H4 Z', 'M4 17 H44 M18 17 V40 M9 23 H13 M9 29 H13 M24 24 H37 M24 30 H33'],
            'gui': ['M4 8 H44 V36 H4 Z', 'M18 43 H30 M24 36 V43 M4 16 H44', 'M11 23 H23 V30 H11 M29 23 H37 M29 29 H35'],
            'shield': ['M24 3 L41 10 V24 C41 35 31 43 24 47 C17 43 7 35 7 24 V10 Z', 'M16 24 L22 30 L33 18'],
        }
        self.parts.append(f'<g transform="translate({x} {y}) scale({scale})">')
        for d in shapes[name]:
            self.path(d, color, 2)
        self.parts.append('</g>')

    def district(self, x, y, w, h, name, detail, icon, path, compact=False):
        self.link(path)
        self.rect(x, y, w, h, 'url(#domain)', '#466658', 10, 'class="district"')
        self.path(f'M{x + w - 50} {y} L{x + w - 50} {y + 15} L{x + w} {y + 15}', '#466658', 1)
        self.icon(x + 22, y + (16 if compact else 22), icon, scale=.75 if compact else 1)
        self.text(x + (72 if compact else 88), y + (38 if compact else 49), name, 27 if compact else 32, GREEN, 600)
        if compact:
            self.text(x + 220, y + 38, detail[0], 21, MUTED)
        else:
            self.lines(x + 24, y + 93, detail, 21, leading=29)
        self.endlink()

    def draw(self):
        # A restrained editorial cover, with a small cartographic ownership motif.
        self.text(72, 67, 'MIXOLOGY  /  AN ARCHITECTURE FIELD GUIDE', 18, GREEN, 700, extra='letter-spacing="3"')
        self.text(72, 163, 'Explicit Modules', 91, INK, 400, cls='serif')
        self.text(76, 237, 'with a Go accent.', 53, GREEN, cls='serif', extra='font-style="italic"')
        self.text(76, 281, 'A domain-first modular monolith. Clear ownership. Little ceremony.', 25, MUTED)
        for x, y in [(1360, 122), (1420, 122), (1360, 182), (1420, 182)]:
            self.rect(x, y, 48, 48, '#203b31', GREEN, 6)
            self.circle(x + 24, y + 24, 4, GREEN)
        self.rect(1344, 106, 140, 140, 'none', '#466658', 15)
        self.text(1414, 275, 'ONE APPLICATION', 13, GREEN, 700, anchor='middle', extra='letter-spacing="1.5"')
        self.path('M72 316 H1528', LINE, 1)

        self.section(354, '01', 'THE TERRITORY', 'Three entrances. Seven owners.', GREEN)
        for x, title, detail, icon, path in [
            (72, 'CLI', 'urfave/cli · arguments & output', 'cli', 'main/cli/README.md'),
            (568, 'TUI', 'Bubble Tea · messages & state', 'tui', 'main/tui/README.md'),
            (1064, 'GUI', 'Fyne · controls & callbacks', 'gui', 'main/gui/README.md'),
        ]:
            self.link(path)
            self.rect(x, 424, 464, 99, '#202625', LINE, 12)
            self.icon(x + 22, 446, icon, BLUE)
            self.text(x + 87, 459, title, 26, BLUE, 700)
            self.text(x + 87, 494, detail, 20, MUTED)
            self.endlink()

        self.rect(72, 552, 1456, 544, '#181f1c', '#60796d', 22)
        self.path('M304 523 V539 H1296 V523 M800 523 V539', BLUE, 2)
        self.arrow('M800 539 V575')
        self.rect(868, 542, 627, 23, BG, 'none', 0)
        self.text(880, 558, 'EACH ENTRYPOINT BUILDS THE APPLICATION THROUGH app.New', 16, MUTED, 500)
        self.link('app/app.go')
        self.rect(96, 578, 1408, 61, '#21333e', '#466879', 10)
        self.text(124, 618, 'PUBLIC GO OPERATIONS', 22, BLUE, 700)
        self.text(518, 618, 'Typed facade calls  ·  shared behavior  ·  fresh operation context', 23, INK)
        self.endlink()

        self.district(96, 657, 450, 150, 'Ingredients', ['Catalog, substitutions & retirement'], 'leaf', 'app/domains/ingredients/module.go')
        self.district(562, 657, 450, 150, 'Drinks', ['Recipes, preparation & review'], 'drink', 'app/domains/drinks/module.go')
        self.district(1028, 657, 476, 150, 'Menus', ['Curation, readiness & publication'], 'menu', 'app/domains/menus/module.go')
        self.district(96, 823, 696, 150, 'Inventory', ['Physical stock, reservations & disposition'], 'stock', 'app/domains/inventory/module.go')
        self.district(808, 823, 696, 150, 'Orders', ['Acceptance, fulfillment plans & amendments'], 'order', 'app/domains/orders/module.go')
        self.district(96, 989, 696, 66, 'Audit', ['Activities, participants & effects'], 'audit', 'app/domains/audit/module.go', True)
        self.district(808, 989, 696, 66, 'Tagging', ['Associations & domain-owned targets'], 'tag', 'app/domains/tagging/module.go', True)
        self.text(96, 1081, 'Districts show ownership. Their size and adjacency carry no dependency meaning.', 17, FAINT)
        self.text(72, 1132, 'Every capability keeps its vocabulary, rules, policy, persistence and native adapters close together.', 24, MUTED)

        self.section(1201, '02', 'THE MODULE BOUNDARY', 'Public contracts connect. Private writes stay owned.', BLUE)
        # Cutaway of a representative operational context, paired with collaboration rules.
        self.rect(72, 1274, 886, 365, '#1b2220', LINE, 18)
        self.text(96, 1311, 'ONE OPERATIONAL CONTEXT', 16, GREEN, 700, extra='letter-spacing="2"')
        self.text(927, 1311, 'app/domains/ingredients/', 17, MUTED, cls='mono', anchor='end')
        layers = [
            (1334, '#21333e', BLUE, 'surfaces/', 'Native adapters translate intent'),
            (1404, '#21333e', BLUE, 'facade + pipeline', 'Typed operations select the behavior'),
            (1474, '#25372e', GREEN, 'models + authz', 'Values, domain rules and Cedar policy'),
            (1544, '#302b21', GOLD, 'internal/', 'Commands and DAO own mutations'),
        ]
        for y, fill, color, label, explanation in layers:
            self.rect(96, y, 838, 56, fill, 'none', 8)
            self.text(116, y + 36, label, 21, color, 600, cls='mono')
            self.text(424, y + 36, explanation, 21, INK)
        self.text(96, 1624, 'Package organization; models and policy support both reads and writes.', 17, FAINT)

        self.link('docs/architecture.md')
        self.text(1002, 1305, 'BETWEEN OWNERS', 16, BLUE, 700, extra='letter-spacing="2"')
        self.arrow('M1004 1344 H1050')
        self.text(1072, 1351, 'Read through public queries', 23, INK, 600)
        self.text(1072, 1383, 'models / queries belong to their context', 18, MUTED)
        self.arrow('M1004 1433 H1050', 'gold')
        self.text(1072, 1440, 'React to owner-local events', 23, INK, 600)
        self.text(1072, 1472, 'Each receiver writes its own state', 20, MUTED)
        self.endlink()
        self.link('pkg/middleware/context.go')
        self.path('M1004 1511 H1504', LINE, 1)
        self.text(1004, 1548, 'Handlers are leaves.', 27, GOLD, 500, cls='serif')
        self.lines(1004, 1580, ['HandlerContext has no AddEvent.', 'Queries and handlers cannot call commands.'], 20, MUTED, 29)
        self.endlink()
        self.arrow('M1004 1640 H1040')
        self.text(1051, 1646, 'Contract use', 16, MUTED)
        self.arrow('M1250 1640 H1286', 'gold')
        self.text(1297, 1646, 'Execution', 16, MUTED)
        self.text(72, 1674, 'Public coupling is deliberate. Go internal + arch-lint protect the implementation boundary.', 23, MUTED)

        self.section(1743, '03', 'THE JOURNEY OF A CHANGE', 'One operation. One local commit.', GOLD)
        self.rect(72, 1815, 1456, 382, 'url(#transaction)', '#76603e', 18)
        self.text(96, 1851, 'COMMAND + REACTIONS + SUCCESS AUDIT SHARE A SQLITE TRANSACTION', 17, GOLD, 700, extra='letter-spacing="1"')
        steps = [('Load', 'Authorize input'), ('Decide', 'Authorize result'), ('React', 'Prepare, then apply'), ('Record', 'Success audit'), ('Commit', 'All writes together')]
        for i, (title, subtitle) in enumerate(steps):
            x = 135 + i * 283
            if i < 4:
                self.arrow(f'M{x + 24} 1904 H{x + 257}', 'gold')
            self.circle(x, 1904, 21, GOLD)
            self.text(x, 1911, str(i + 1), 19, BG, 700, anchor='middle')
            self.text(x - 25, 1956, title, 29, INK, 600)
            self.text(x - 25, 1987, subtitle, 20, MUTED)

        self.path('M96 2010 H1504', '#514635', 1)
        self.text(96, 2044, 'FOLLOW ONE FACT', 15, GOLD, 700, extra='letter-spacing="2"')
        self.text(96, 2082, 'Ingredient retired', 27, INK, 600)
        self.text(96, 2113, 'IngredientDeleted event', 18, MUTED, cls='mono')
        self.path('M345 2074 H396 V2023 H1366', GOLD, 2, 'stroke-dasharray="6 6"')
        for x, title, detail in [(421, 'Drinks', 'Revise or flag recipes'), (694, 'Inventory', 'Retain stock'), (967, 'Menus', 'Recheck availability'), (1240, 'Orders', 'Preserve acceptance')]:
            self.arrow(f'M{x + 126} 2023 V2036', 'gold')
            self.rect(x, 2037, 252, 93, '#29271f', '#65563b', 10)
            self.text(x + 16, 2075, title, 24, GOLD, 600)
            self.text(x + 16, 2107, detail, 19, MUTED)
        self.text(421, 2164, 'For each event: prepare every receiver before applying any reaction. No cascading events.', 19, GOLD)
        self.text(72, 2234, 'On managed failure: roll back the changes, then audit the failed attempt separately.', 23, MUTED)

        # Foundations and enforcement are different jobs, not another universal layer.
        self.path('M72 2270 H1528', LINE, 1)
        for x, label, first, second in [
            (72, 'SHARED VOCABULARY', 'Typed IDs · money · units', 'Small kernel + narrow ports'),
            (568, 'NAMED MECHANISMS', 'Store · policy · middleware', 'app.New + generated dispatch'),
            (1064, 'EXECUTABLE BOUNDARIES', 'Types · internal · arch-lint', 'Topology + behavioral tests'),
        ]:
            self.text(x, 2310, label, 16, PURPLE, 700, extra='letter-spacing="1.5"')
            self.text(x, 2347, first, 24, INK)
            self.text(x, 2379, second, 21, MUTED)
        self.path('M72 2410 H1528', LINE, 1)
        self.text(72, 2446, 'Clean · Explicit · DDD · Fubu · Screaming Architecture → expressed through Go', 19, MUTED)
        self.text(72, 2481, 'Ryan Harris  /  thefellow.github.io  /  2026-09-13', 16, FAINT)
        self.text(1528, 2481, 'MIXOLOGY  ·  a7c2efd  ·  MAP 01', 16, FAINT, anchor='end', extra='letter-spacing="1"')

    def save(self, name='06-explicit-modules'):
        self.parts.append('</svg>')
        OUT.mkdir(parents=True, exist_ok=True)
        target = OUT / f'{name}.svg'
        target.write_text('\n'.join(self.parts) + '\n')
        print(f'Generated {target.relative_to(OUT.parent.parent.parent)}')


if __name__ == '__main__':
    poster = Poster()
    poster.draw()
    poster.save()
