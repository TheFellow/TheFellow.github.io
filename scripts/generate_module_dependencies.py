#!/usr/bin/env python3
"""Draw two dependency sheets. Requires Graphviz; Python uses the standard library.

Pass --verify-source ../go-modular-monolith to compare diagram edges with Go
imports at the article's pinned commit. Tests are excluded; surfaces are grouped.
"""

import argparse
from collections import defaultdict
from html import escape
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import xml.etree.ElementTree as ET

from generate_explicit_modules import Poster, INK, MUTED, FAINT, LINE, GREEN, BLUE, GOLD, PURPLE
from generate_explicit_architecture import CODE, OUT, SHA


# Every edge below is an observed source import at SHA, rather than a proposed rule.
LOCAL = {
    'surfaces': ['facade', 'models', 'queries'],
    'facade': ['authz', 'commands', 'dao', 'models', 'queries'],
    'queries': ['availability', 'dao', 'models'],
    'commands': ['availability', 'dao', 'events', 'models'],
    'handlers': ['availability', 'dao', 'events', 'models'],
    'availability': ['models'],
    'dao': ['models'],
    'events': ['models'],
    'models': ['authz'],
}
READS = {
    'drinks': ['ingredients'],
    'inventory': ['ingredients'],
    'menus': ['drinks', 'ingredients', 'inventory'],
    'orders': ['drinks', 'ingredients', 'inventory', 'menus'],
}
EVENTS = {
    'drinks': ['ingredients'],
    'inventory': ['ingredients', 'orders'],
    'menus': ['drinks', 'ingredients', 'inventory', 'orders'],
    'orders': ['drinks', 'ingredients', 'inventory', 'menus'],
}


def verify_source(repo):
    archive = subprocess.check_output(['git', '-C', str(repo), 'archive', SHA, 'app/domains'])
    actual_local, actual_reads, actual_events = (defaultdict(set) for _ in range(3))
    rename = {'menus': 'facade', 'internal/commands': 'commands', 'internal/dao': 'dao',
              'internal/availability': 'availability'}

    def local_name(package):
        name = package.removeprefix('menus/')
        return 'surfaces' if name.startswith('surfaces/') else rename.get(name, name)

    with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
        for member in tree.getmembers():
            if not member.name.endswith('.go') or member.name.endswith('_test.go'):
                continue
            source = str(Path(member.name).parent).removeprefix('app/domains/')
            owner = source.split('/')[0]
            body = tree.extractfile(member).read().decode()
            blocks = re.findall(r'(?m)^import\s*\((.*?)\)', body, re.S)
            blocks += re.findall(r'(?m)^import\s+([^\n(]+)', body)
            for block in blocks:
                for target in re.findall(r'"github.com/TheFellow/go-modular-monolith/app/domains/([^"\n]+)"', block):
                    peer, _, kind = target.partition('/')
                    if owner == peer == 'menus':
                        actual_local[local_name(source)].add(local_name(target))
                    if owner != peer and '/surfaces/' not in source:
                        if kind == 'queries':
                            actual_reads[owner].add(peer)
                        if source.endswith('/handlers') and kind == 'events':
                            actual_events[owner].add(peer)
    for title, expected, actual in [('Menus imports', LOCAL, actual_local),
                                    ('peer queries', READS, actual_reads),
                                    ('peer events', EVENTS, actual_events)]:
        assert {k: set(v) for k, v in expected.items()} == dict(actual), (title, expected, dict(actual))
        print(f'Verified {sum(map(len, expected.values()))} {title} edges at {SHA[:7]}.')


def quote(value):
    return json.dumps(value)


def graph(nodes, edges, color=BLUE, direction='TB', extra=''):
    lines = ['digraph G {',
             f'graph [bgcolor="transparent", rankdir={direction}, pad=0.15, nodesep=0.45, ranksep=0.7, splines=spline, outputorder=edgesfirst];',
             f'node [shape=box, style="rounded,filled", color="#466879", fillcolor="#21333e", fontcolor="{INK}", fontname="Arial", fontsize=21, margin="0.20,0.14", penwidth=1.2];',
             f'edge [color="{color}", arrowsize=0.8, penwidth=1.6];']
    for key, (title, subtitle, path, fill, stroke) in nodes.items():
        label = (f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
                 f'<TR><TD><B>{escape(title)}</B></TD></TR>'
                 f'<TR><TD><FONT POINT-SIZE="15" COLOR="{MUTED}">{escape(subtitle)}</FONT></TD></TR></TABLE>>')
        lines.append(f'{quote(key)} [label={label}, fillcolor="{fill}", color="{stroke}", URL={quote(CODE + path)}, target="_blank"];')
    for source, target in edges:
        lines.append(f'{quote(source)} -> {quote(target)};')
    lines += [extra, '}']
    return '\n'.join(lines) + '\n'


def embed(poster, source, name, x, y, w, h):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f'{name}.dot').write_text(source)
    svg = ET.fromstring(subprocess.check_output(['dot', '-Tsvg'], input=source.encode()))
    for node in svg.iter():
        if 'id' in node.attrib:
            node.attrib['id'] = name + '-' + node.attrib['id']
    svg.attrib.update(x=str(x), y=str(y), width=str(w), height=str(h))
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    poster.parts.append(ET.tostring(svg, encoding='unicode'))


def header(p, title, subtitle, sheet):
    p.text(72, 65, f'EXPLICIT MODULES  /  DEPENDENCY FIELD GUIDE  /  {sheet}', 18, GREEN, 700, extra='letter-spacing="2"')
    p.text(72, 146, title, 65, INK, cls='serif')
    p.text(72, 195, subtitle, 24, MUTED)
    p.path('M72 227 H1528', LINE, 1)
    p.arrow('M74 260 H130')
    p.text(150, 267, 'A → B means A imports B. Every arrow is a source dependency.', 23, BLUE, 600)


def footer(p, y):
    p.path(f'M72 {y} H1528', LINE, 1)
    p.text(72, y + 36, 'Ryan Harris  /  thefellow.github.io  /  source baseline a7c2efd', 17, FAINT)
    p.text(1528, y + 36, 'Open the SVG to follow package links.', 17, FAINT, anchor='end')


def within():
    p = Poster(1720, 'Inside a module: Menus dependency diagram',
               'All 23 local production import edges in Menus at baseline a7c2efd, with its three surface packages grouped. Arrows point from importer to dependency. External imports are summarized separately.')
    header(p, 'Inside a module', 'Menus makes the public entry, private implementation and shared values visible.', '02')
    p.rect(72, 299, 1456, 1010, '#181f1c', '#60796d', 20)
    p.text(98, 339, 'app/domains/menus/', 24, GREEN, 600, cls='mono')
    p.text(1500, 339, 'ALL LOCAL IMPORTS · SURFACES GROUPED', 16, MUTED, anchor='end')
    labels = {
        'surfaces': ('surfaces/{cli,tui,gui}', 'Native adapters', 'surfaces', '#21333e', BLUE),
        'facade': ('menus', 'Public facade + construction', '', '#21333e', BLUE),
        'queries': ('queries', 'Public read contracts', 'queries', '#21333e', BLUE),
        'commands': ('internal/commands', 'Write decisions', 'internal/commands', '#302b21', GOLD),
        'dao': ('internal/dao', 'Private persistence', 'internal/dao', '#302b21', GOLD),
        'availability': ('internal/availability', 'Readiness calculations', 'internal/availability', '#302b21', GOLD),
        'handlers': ('handlers', 'Owned event reactions', 'handlers', '#2e293b', PURPLE),
        'models': ('models', 'Domain values + public types', 'models', '#25372e', GREEN),
        'events': ('events', 'Facts owned by Menus', 'events', '#25372e', GREEN),
        'authz': ('authz', 'Domain-owned Cedar vocabulary', 'authz', '#25372e', GREEN),
    }
    nodes = {k: (a, b, 'app/domains/menus/' + path, fill, stroke) for k, (a, b, path, fill, stroke) in labels.items()}
    source = graph(nodes, [(a, b) for a, bs in LOCAL.items() for b in bs], extra='{rank=same; surfaces; handlers;}')
    embed(p, source, '07-module-imports', 90, 360, 1420, 900)
    p.text(98, 1282, 'The facade → DAO edge includes schema registration. Model imports converge on values and policy vocabulary.', 20, MUTED)
    p.text(72, 1361, 'THE BOUNDARIES THE BUILD CHECKS', 18, GOLD, 700, extra='letter-spacing="2"')
    p.lines(72, 1403, ['Surfaces cannot import their own internal packages.',
                       'Queries and handlers cannot import commands.',
                       'Handlers cannot import domain facades.'], 23, INK, 37)
    p.text(842, 1361, 'DEPENDENCIES BEYOND THIS BOX', 18, PURPLE, 700, extra='letter-spacing="2"')
    p.lines(842, 1403, ['Peer models, queries and events keep their owner.',
                        'Surfaces use matching toolkits and public facades.',
                        'Shared kernel, middleware and store support the module.'], 21, MUTED, 37)
    p.link('.arch-lint.yaml')
    p.rect(72, 1542, 1456, 75, '#202625', LINE, 12, 'class="district"')
    p.text(98, 1573, 'Go internal blocks peer access. arch-lint narrows access inside the owner’s tree.', 23, GREEN, 600)
    p.text(98, 1601, 'Observed imports are shown above; the rules also reject forbidden imports that have not been written.', 19, MUTED)
    p.endlink()
    footer(p, 1652)
    p.save('07-module-dependencies')


def between():
    p = Poster(1950, 'Between modules: public query and event dependencies',
               'Nine cross-context query dependencies and eleven event-contract dependencies at baseline a7c2efd. Arrows point from importer to contract owner. Tagging registry, Audit composition and native facade imports are explained separately.')
    header(p, 'Between modules', 'Public contracts expose the coupling. Each context retains its own write implementation.', '03')
    for x in (72, 816):
        p.rect(x, 306, 712, 886, '#181f1c', LINE, 18)
    p.text(98, 350, '01  SUPPORTED READS', 20, BLUE, 700)
    p.lines(98, 388, ['A package in the source context imports', 'the target context’s public queries package.'], 21, MUTED, 28)
    nodes = {name: (name.capitalize(), 'bounded context', f'app/domains/{name}', '#21333e', BLUE)
             for name in ('orders', 'menus', 'drinks', 'inventory', 'ingredients')}
    source = graph(nodes, [(a, b) for a, bs in READS.items() for b in bs])
    embed(p, source, '08-query-imports', 92, 446, 672, 655)
    p.lines(98, 1131, ['9 edges · non-surface production packages', 'Models may also cross these public seams.'], 19, MUTED, 28)

    p.text(842, 350, '02  EVENT CONTRACTS', 20, PURPLE, 700)
    p.lines(842, 388, ['A receiving handler imports the event type', 'from the context that owns the fact.'], 21, MUTED, 28)
    nodes = {}
    for name in EVENTS:
        nodes[name + '_h'] = (name + '/handlers', 'receiver', f'app/domains/{name}/handlers', '#2e293b', PURPLE)
    for name in ('ingredients', 'drinks', 'inventory', 'menus', 'orders'):
        nodes[name + '_e'] = (name + '/events', 'contract owner', f'app/domains/{name}/events', '#25372e', GREEN)
    source = graph(nodes, [(a + '_h', b + '_e') for a, bs in EVENTS.items() for b in bs], PURPLE, 'LR')
    embed(p, source, '08-event-imports', 834, 446, 676, 655)
    p.lines(842, 1131, ['11 edges · arrow points toward the event owner', 'Runtime delivery runs the other way.'], 19, MUTED, 28)

    p.text(72, 1252, 'OTHER DEPENDENCIES HAVE DISTINCT JOBS', 19, GREEN, 700, extra='letter-spacing="2"')
    # These are deliberately selected exact imports; the upper graphs are exhaustive for their stated categories.
    p.rect(72, 1283, 1456, 398, '#202625', LINE, 16)
    for y, title, left, right, note, path in [
        (1323, 'TAGGING', 'Operational facades', 'tagging', 'Registry and target registration; persistence uses the kernel’s tag.Repository port.', 'app/domains/menus/tagging.go'),
        (1440, 'AUDIT + WIRING', 'app', 'audit + dispatcher + middleware', 'app.New injects the audit writer and dispatcher into the pipeline.', 'app/app.go'),
        (1557, 'NATIVE COMPOSITION', 'menus/surfaces/{gui,tui}', 'drinks', 'Public facade imports compose screens; peer surfaces and private writes stay inaccessible.', 'app/domains/menus/surfaces/gui'),
    ]:
        p.link(path)
        p.text(98, y, title, 17, GREEN, 700)
        p.text(379, y, left, 22, INK, 600)
        p.arrow(f'M735 {y - 7} H813')
        p.text(842, y, right, 22, BLUE, 600)
        p.text(379, y + 39, note, 19, MUTED)
        p.endlink()
    p.text(72, 1733, 'RECIPROCAL BUSINESS RELATIONSHIPS CAN STILL FORM AN ACYCLIC PACKAGE GRAPH.', 18, GOLD, 700)
    p.lines(72, 1774, ['Orders reads inventory/queries; Inventory reacts through inventory/handlers → orders/events.',
                       'The generated dispatcher imports event types and receivers. Commands publish their own events.',
                       'These views omit standard library, third-party and other shared-package imports.'], 22, MUTED, 34)
    footer(p, 1882)
    p.save('08-between-module-dependencies')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-source', type=Path)
    args = parser.parse_args()
    if args.verify_source:
        verify_source(args.verify_source)
    within()
    between()
