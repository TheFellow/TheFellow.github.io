#!/usr/bin/env python3
"""Generate the original, linked SVG figures for Explicit Architecture, with a Go Accent.

Only the Python standard library is required. SVGs are the editable publication
artifacts; PDF export instructions live beside them in README.txt.
"""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/diagrams/explicit-architecture'
SHA = '0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c'
CODE = f'https://github.com/TheFellow/go-modular-monolith/blob/{SHA}/'
SITE = 'https://thefellow.github.io/'
# Match the site's Minimal Mistakes neon skin, retaining semantic color groups.
# Keep colors embedded so downloaded SVG/PDF files also render in the dark theme.
C = {'ink':'#fff6fb', 'muted':'#d0c8d2', 'line':'#797482', 'paper':'#141010',
     'panel':'#242021', 'accent':'#ff4f94',
     'teal':'#63e6be', 'blue':'#74c0fc', 'gold':'#ffc36b', 'purple':'#c084fc',
     'green':'#18372f', 'ice':'#1c2d46', 'sand':'#3b2d1b', 'lav':'#30243e'}

class SVG:
    def __init__(self, width, height, step, title, subtitle):
        self.w, self.h = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
          f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}. Original Mixology diagram by Ryan Harris, inspired by Herberto Graça’s Explicit Architecture. Source baseline {SHA}. Linked panels open implementation evidence.</desc>',
          '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{blue}"/></marker><marker id="flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{gold}"/></marker></defs>'.format_map(C),
          '<style>text {{font-family:Arial,Helvetica,sans-serif;fill:{ink}}} a:hover rect {{stroke:{accent};stroke-width:3}} .muted {{fill:{muted}}} .mono {{font-family:monospace}} .eyebrow {{font-weight:700;letter-spacing:2px;fill:{accent}}}</style>'.format_map(C)]
        self.rect(0,0,width,height,C['paper'],rx=0,stroke='none')
        self.text(40,42,f'MIXOLOGY / EXPLICIT ARCHITECTURE / {step}',15,cls='eyebrow')
        self.text(40,88,title,34,bold=True)
        self.text(40,122,subtitle,18,cls='muted')
    def rect(self,x,y,w,h,fill=C['panel'],stroke=C['line'],rx=14,dash=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def text(self,x,y,s,size=18,bold=False,anchor='start',cls=None):
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}"'+(' font-weight="700"' if bold else '')+(f' class="{cls}"' if cls else '')+f'>{escape(s)}</text>')
    def lines(self,x,y,lines,size=18,leading=27,anchor='start',cls=None):
        for i,line in enumerate(lines): self.text(x,y+i*leading,line,size,anchor=anchor,cls=cls)
    def link(self,url): self.parts.append(f'<a href="{escape(url,quote=True)}" xlink:href="{escape(url,quote=True)}" target="_blank">')
    def endlink(self): self.parts.append('</a>')
    def card(self,x,y,w,h,title,lines,fill=C['panel'],url=None,size=18):
        if url: self.link(url)
        self.rect(x,y,w,h,fill)
        self.text(x+20,y+33,title,21,bold=True)
        self.lines(x+20,y+63,lines,size,27,cls='muted')
        if url: self.endlink()
    def arrow(self,x1,y1,x2,y2,flow=False):
        color=C['gold'] if flow else C['blue']; marker='flow' if flow else 'arrow'
        self.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5"'+(' stroke-dasharray="7 5"' if flow else '')+f' marker-end="url(#{marker})"/>')
    def footer(self):
        self.text(40,self.h-37,'Ryan Harris · thefellow.github.io · 2026-09-13 · Go baseline 0d5e64b',15,cls='muted')
        self.text(40,self.h-14,'Original diagram; progressive approach inspired by Herberto Graça’s Explicit Architecture. Open SVG directly to follow source links.',14,cls='muted')
    def save(self,name):
        self.footer(); self.parts.append('</svg>'); (OUT/name).write_text('\n'.join(self.parts)+'\n')


def boundaries():
    s=SVG(1200,730,'01','One application, three conversations','Driving adapters translate intent; public operations own the behavior that must agree.')
    for y,title,lines,path in [(195,'CLI / urfave/cli',['Arguments → typed request','One invocation, then exit'],'main/cli/README.md'),(355,'TUI / Bubble Tea',['Messages, commands, text','Persistent application session'],'main/tui/README.md'),(515,'GUI / Fyne',['Callbacks, retained widgets','Background work → UI thread'],'main/gui/README.md')]:
        s.card(40,y,300,125,title,lines,C['green'],CODE+path)
        s.arrow(340,y+62,430,y+62)
    s.rect(430,195,350,445,C['ice'])
    s.text(455,231,'PUBLIC APPLICATION OPERATIONS',17,bold=True)
    s.lines(455,277,['Seven domain facades','Typed commands and queries','Fresh operation context'],21,34)
    s.card(453,388,304,224,'One behavioral boundary',['Authorization on current state','Domain decisions and values','Transactions and owned reactions','Audit and typed errors'],url=CODE+'pkg/middleware/README.md',size=16)
    s.card(890,195,270,165,'Local persistence',['Owned Store / Tx / Query','SQLite JSON records','One local database file'],C['sand'],CODE+'pkg/store/README.md',size=16)
    s.card(890,425,270,165,'Policy evaluation',['Domain-owned Cedar policy','Shared evaluation machinery','Models expose Cedar entities'],C['lav'],CODE+'pkg/authz/README.md',size=16)
    s.arrow(780,277,890,277); s.arrow(780,507,890,507)
    s.text(805,256,'uses',16,cls='muted');s.text(805,486,'uses',16,cls='muted')
    s.save('01-boundaries.svg')


def domain_slice():
    s=SVG(1280,890,'02','A domain is a vertical slice','Directory proximity keeps a capability findable; import rules keep its responsibilities separate.')
    s.rect(40,165,950,626,C['panel'])
    s.text(65,205,'app/domains/<context>/',24,bold=True)
    s.card(65,230,900,105,'surfaces/{cli,tui,gui}',['Concrete presentation adapters; matching toolkit only; no access to private writes.'],C['green'],CODE+'app/domains/readme.md',size=17)
    s.arrow(235,335,235,375)
    s.card(65,375,405,126,'Public facade',['Typed operations select pipeline calls','Owns construction and application entry'],C['ice'],CODE+'app/domains/ingredients/delete.go',size=17)
    s.card(500,375,465,126,'Public collaboration contracts',['models / queries / events','Peers depend on the named contract owner'],C['ice'],CODE+'docs/architecture.md',size=17)
    s.arrow(235,501,235,550);s.arrow(730,550,730,501)
    s.card(65,550,405,125,'internal/commands + internal/dao',['Write decisions and private persistence','Queries and handlers may use own DAO'],C['sand'],CODE+'.arch-lint.yaml',size=17)
    s.card(500,550,465,125,'handlers + authz',['Owned leaf reactions; domain-owned policy','Explicit profiles for Audit and Tagging'],C['lav'],CODE+'architecture/domain_topology_test.go',size=17)
    s.text(65,721,'A surface is an outer adapter even when its directory lives inside the domain.',18,bold=True)
    s.text(65,755,'Solid arrows: selected source dependencies. Adjacency alone does not grant access.',17,cls='muted')
    s.card(1020,230,220,270,'Peer context',['Reads public queries','Consumes public events','Uses shared model types','Owns its own writes'],C['ice'],CODE+'docs/architecture.md',size=15)
    s.arrow(1020,472,965,472)
    s.card(1020,550,220,205,'Build checks',['Go internal visibility','arch-lint consumer rules','Topology vocabulary','Composition coverage'],C['green'],CODE+'architecture/arch_lint_test.go',size=15)
    s.save('02-domain-slice.svg')


def transaction():
    s=SVG(1500,850,'03','One command, one local commit','Dashed numbered arrows describe execution. The preparation barrier applies separately to each event.')
    s.rect(35,175,1430,410,C['sand'],stroke=C['gold'])
    s.text(55,208,'ONE DOMAIN COMMAND CLAIMS THE SQL TRANSACTION',17,bold=True)
    steps=[('1 · Load + authorize',['Trusted current input','Policy inside transaction'],'pkg/middleware/run.go'),('2 · Decide + authorize',['Mutate source state','Authorize resulting resource'],'pkg/middleware/run.go'),('3 · Dispatch events',['Prepare, then apply','All interested owners'],'pkg/dispatcher/dispatcher_gen.go'),('4 · Audit + commit',['Record successful activity','Commit all domain writes'],'pkg/middleware/chains.go')]
    for i,(title,lines,path) in enumerate(steps):
        x=55+i*355
        s.card(x,235,325,130,title,lines,C['panel'],CODE+path,size=17)
        if i<3:s.arrow(x+325,300,x+354,300,True)
    s.card(55,402,385,140,'The source fact',['Ingredients → IngredientDeleted','Retirement, withdrawal, replacement'],C['green'],CODE+'app/domains/ingredients/events/ingredient-deleted.go',size=17)
    s.arrow(440,468,485,468,True)
    s.card(485,402,410,140,'Prepare every applicable receiver',['Calculate from pre-reaction state','Menus projects stock + recipe changes'],C['ice'],CODE+'app/domains/menus/handlers/prepared.go',size=17)
    s.arrow(895,468,940,468,True)
    s.card(940,402,505,140,'Apply leaf reactions in the same transaction',['Drinks · Inventory · Menus · Orders','HandlerContext has no AddEvent'],C['lav'],CODE+'pkg/middleware/context.go',size=17)
    s.card(40,620,685,140,'Failure when this operation owns the transaction',['Roll back domain changes and the success activity.','Record the failed attempt separately after rollback.','One command activity includes every leaf effect.'],C['panel'],CODE+'pkg/middleware/uow.go',size=17)
    s.card(755,620,705,140,'Ownership and cost',['An external transaction admits one command; its caller completes it.','One slow or failing reaction affects the originating command.','Per-event preparation is a protocol tested with handler permutations.'],C['panel'],CODE+'app/cross_domain_regression_test.go',size=17)
    s.save('03-transaction.svg')


def foundations():
    s=SVG(1400,880,'04','Shared code has more than one job','The package prefix is not the architecture: distinguish common values, mechanisms, and concrete wiring.')
    s.card(40,170,840,126,'Domain contexts and public contracts',['Ingredients · Drinks · Inventory · Menus · Orders · Audit · Tagging','Owner-local models, queries, and events express supported collaboration.'],C['ice'],CODE+'docs/architecture.md')
    s.card(925,170,435,126,'Concrete presentation',['Domain surfaces + main composition','CLI / TUI / GUI remain independent.'],C['green'],CODE+'app/domains/readme.md',size=17)
    s.arrow(450,296,450,345);s.arrow(1130,296,1130,345)
    s.card(40,345,840,130,'app/kernel: shared vocabulary and narrow ports',['Typed IDs · money · measurement · quality · tags · tag.Repository','Domains depend on these values; the kernel does not import domains.'],C['green'],CODE+'app/kernel/readme.md')
    s.card(925,345,435,130,'pkg/toolkits/{cli,tui,gui}',['Framework-specific mechanics','No application or sibling-toolkit imports'],C['green'],CODE+'pkg/toolkits/readme.md',size=17)
    s.card(40,520,635,240,'Named mechanisms and concrete adapters',['middleware: configured operation pipeline','store: owned SQLite persistence and query types','filter: typed syntax, safe pushdown, exact evaluation','errors / log / telemetry: common application mechanics','Cedar entities appear in public models and IDs.'],C['sand'],CODE+'pkg/middleware/chains.go',size=17)
    s.card(705,520,655,240,'Application wiring, including generated code',['app.New constructs modules and supplies dependencies.','pkg/dispatcher imports concrete domain handlers and events.','pkg/authz assembles domain policy material.','Generators also produce entity IDs and typed error helpers.','These packages are not all domain-independent libraries.'],C['lav'],CODE+'app/app.go',size=17)
    s.save('04-foundations.svg')


def polar(cx,cy,r,a):
    a=math.radians(a);return cx+r*math.cos(a),cy+r*math.sin(a)

def sector(s,cx,cy,r1,r2,a,b,fill):
    p1=polar(cx,cy,r2,a);p2=polar(cx,cy,r2,b);p3=polar(cx,cy,r1,b);p4=polar(cx,cy,r1,a)
    s.parts.append(f'<path d="M {p1[0]} {p1[1]} A {r2} {r2} 0 0 1 {p2[0]} {p2[1]} L {p3[0]} {p3[1]} A {r1} {r1} 0 0 0 {p4[0]} {p4[1]} Z" fill="{fill}" stroke="{C["line"]}" stroke-width="1.5"/>')


def complete():
    s=SVG(2000,2010,'05','Explicit Architecture, with a Go accent','A detailed map of Mixology: conceptual responsibility, supported dependencies, execution, and evidence.')
    s.text(40,163,'DRIVING SIDE',17,bold=True); s.text(1535,163,'DRIVEN TOOLS + OWNED ADAPTERS',17,bold=True)
    # Main map: seven conceptual slices, with a common operation boundary.
    cx,cy=1000,585
    s.parts.append(f'<circle cx="{cx}" cy="{cy}" r="410" fill="{C["ice"]}" stroke="{C["blue"]}" stroke-width="3"/>')
    domains=[('Ingredients',['Catalog · substitutions','Retirement and replacement'],'ingredients'),('Drinks',['Recipes · preparation','Active / review required'],'drinks'),('Inventory',['Stock · reservations','Disposition · movements'],'inventory'),('Menus',['Curation · publication','Readiness · availability'],'menus'),('Orders',['Acceptance · current plan','Amendments · lifecycle'],'orders'),('Audit',['Append-only activities','Touches · participants · effects'],'audit'),('Tagging',['Associations · target registry','Prepared tag event reactions'],'tagging')]
    for i,(title,lines,path) in enumerate(domains):
        a=-90-360/14+i*360/7;b=a+360/7
        s.link(CODE+f'app/domains/{path}/module.go')
        sector(s,cx,cy,142,363,a,b,[C['green'],C['sand'],C['ice'],C['lav']][i%4])
        x,y=polar(cx,cy,256,-90+i*360/7)
        s.text(x,y-19,title,24,bold=True,anchor='middle')
        s.lines(x,y+11,lines,15,23,anchor='middle')
        s.endlink()
    s.parts.append(f'<circle cx="{cx}" cy="{cy}" r="141" fill="{C["panel"]}" stroke="{C["teal"]}" stroke-width="2"/>')
    s.lines(cx,cy-42,['DOMAIN DECISIONS','Values · lifecycle','Historical commitments','Pure transition rules'],19,30,anchor='middle')
    s.text(cx,164,'PUBLIC APPLICATION OPERATIONS',17,bold=True,anchor='middle')
    s.text(cx,1015,'TYPED FACADES + CONFIGURED PIPELINE',16,bold=True,anchor='middle')
    # Driving adapters and selected real source dependencies.
    for y,title,lines,path in [(195,'CLI · main/cli',['urfave/cli flags + command hierarchy','Parse args / JSON; print results','Fresh invocation context'],'main/cli/README.md'),(397,'TUI · main/tui',['Bubble Tea messages + commands','ViewModel / Interaction ownership','Forms, dialogs, keys, text frames'],'main/tui/README.md'),(599,'GUI · main/gui',['Fyne presenters + retained widgets','Executor → UI dispatcher','Live input and request generations'],'main/gui/README.md')]:
        s.card(40,y,410,169,title,lines,C['green'],CODE+path,size=18)
    s.card(40,801,410,166,'Independent adapter mechanics',['surfaces/{cli,tui,gui} per domain','Matching pkg/toolkits only','main/seed supplies sample data'],C['green'],CODE+'pkg/toolkits/readme.md',size=18)
    s.arrow(450,480,595,480);s.text(468,451,'calls public',16,cls='muted');s.text(468,471,'operations',16,cls='muted')
    s.card(1535,195,425,193,'pkg/store → SQLite',['Owned Store / Tx / Query[T]','Private DAO rows → JSON records','Registration → indexes + constraints','WAL readers; serialized writers','Revision predicate rejects stale writes'],C['sand'],CODE+'pkg/store/README.md',size=17)
    s.card(1535,415,425,164,'Domain authz → Cedar',['Policies and schemas owned per context','Input and result authorization','Public models expose Cedar entities','Generated policy assembly in pkg/authz'],C['lav'],CODE+'pkg/authz/README.md',size=17)
    s.card(1535,606,425,164,'Typed filtering → Expr + SQL',['Domain schema → checked expression','Safe SQL candidate constraints','Hydration → complete predicate','Authorized paging yields visible matches'],C['sand'],CODE+'pkg/filter/README.md',size=17)
    s.card(1535,797,425,170,'Store changes → client refresh',['Connection-local data_version monitor','Coalesced invalidation; no record payload','TUI / GUI repeat authorized queries','Separate from transactional domain events'],C['sand'],CODE+'pkg/store/changes.go',size=17)
    s.arrow(1405,480,1535,480);s.text(1430,451,'uses policy',16,cls='muted');s.text(1430,471,'contracts',16,cls='muted')
    s.text(515,1043,'Circle = responsibility map, not a literal import graph. Public contracts remain coupled to their named owners.',18,cls='muted')
    # Fine-grained slice vocabulary.
    s.card(40,1060,1920,130,'WITHIN A REGULAR CONTEXT / OWNERSHIP AND VISIBILITY',['surfaces → public facade → typed pipeline → internal/commands + internal/dao; queries and handlers may use their own DAO.','models / queries / events are public contracts. Tagging reacts through handlers and owns association writes in internal/dao.','Peer reads use supported query contracts. Commands publish only their own events. Handlers cannot import facades or commands.'],C['ice'],CODE+'.arch-lint.yaml',size=19)
    # Transaction timeline, all constraints inside one box.
    s.rect(40,1220,1920,256,C['sand'],stroke=C['gold'])
    s.text(60,1254,'EXECUTION / ONE LOCAL TRANSACTION / NUMBERED DASHED ARROWS',18,bold=True)
    steps=[('1 · Load + authorize',['Trusted input','Current principal']),('2 · Execute + authorize',['Source mutation','Resulting resource']),('3 · Dispatch each event',['Prepare every receiver','Apply leaf reactions']),('4 · Success audit',['Domain effects','Same transaction']),('5 · Commit',['All writes together','One result to caller'])]
    for i,(title,lines) in enumerate(steps):
        x=60+i*380
        s.card(x,1275,350,115,title,lines,C['panel'],CODE+('pkg/dispatcher/dispatcher_gen.go' if i==2 else 'pkg/middleware/run.go'),size=17)
        if i<4:s.arrow(x+350,1332,x+379,1332,True)
    s.text(60,1420,'Retirement: IngredientDeleted → Drinks / Inventory / Menus / Orders. Preparation is per event; HandlerContext cannot AddEvent.',19,bold=True)
    s.text(60,1452,'Failure: owner rolls back, then records failed attempt. One command claims each transaction; nested and sequential command composition is rejected.',18,cls='muted')
    # Foundation taxonomy and observation.
    s.card(40,1510,610,240,'SHARED VALUES + NARROW PORTS',['app/kernel: typed entity IDs, money,','measurement, quality, tags, tag.Repository.','Common identity and unit semantics.','Tagging owns associations; registered','domain loaders preserve target ownership.','Kernel does not depend on domains.'],C['green'],CODE+'app/kernel/readme.md',size=18)
    s.card(680,1510,640,240,'MECHANISMS + EXPLICIT WIRING',['middleware: transactions, activity, dispatch.','app.New injects dispatcher + audit writer.','pkg/dispatcher imports domain receivers.','pkg/authz assembles domain policy material.','Generators: events, policies, IDs, errors.','pkg is not uniformly domain-independent.'],C['lav'],CODE+'app/app.go',size=18)
    s.card(1350,1510,610,240,'OBSERVATION + PRESENTATION',['Gets authorize results; lists elide denials.','Action state: hidden / disabled / enabled.','Commands repeat policy and prerequisites.','Errors keep typed, transport-neutral meaning.','Log + metrics surround operation paths.','Audit explains effects; it is not a replay log.'],C['ice'],CODE+'pkg/presentation/actions/README.md',size=18)
    s.rect(40,1780,1920,133,C['panel'],stroke=C['teal'])
    s.text(60,1813,'EXECUTABLE EVIDENCE',20,bold=True)
    for x,title,path in [(60,'Types + Go internal','pkg/middleware/context.go'),(425,'Captured import rules','.arch-lint.yaml'),(790,'Topology + registration','architecture/domain_topology_test.go'),(1220,'Permutation + rollback','app/cross_domain_regression_test.go'),(1625,'Independent clients','main/gui/README.md')]:
        s.link(CODE+path);s.text(x,1850,title,18,bold=True);s.endlink()
    s.text(60,1887,'Current scope: seven contexts and three UI runtimes. Procurement, Analytics, process managers, brokers, and outboxes are future design pressures.',18,cls='muted')
    s.arrow(50,1940,100,1940);s.text(115,1946,'Selected dependency / contract use',16,cls='muted')
    s.arrow(535,1940,585,1940,True);s.text(600,1946,'Execution sequence (not imports)',16,cls='muted')
    s.text(1100,1946,'Colored regions group responsibilities; linked panels provide the code trace.',16,cls='muted')
    s.save('05-complete.svg')


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    boundaries();domain_slice();transaction();foundations();complete()
    print('Generated five SVG diagrams in',OUT.relative_to(ROOT))
