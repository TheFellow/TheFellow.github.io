<!-- Generated from https://thefellow.github.io/resume/ by scripts/generate_llm_content.py; do not edit. -->

# Resume

Source: [https://thefellow.github.io/resume/](https://thefellow.github.io/resume/)

## Pyramid summary

- **~2 words:** Engineering experience
- **~8 words:** Staff-level experience in authorization, architecture, delivery, and technical leadership.
- **Expanded:** Staff software engineer specializing in authorization, platform architecture, API evolution, and durable systems.

## Full content

Staff Software Engineer

## Architecture, authorization, and durable systems under real-world constraints
I design and deliver systems that have to remain understandable while they evolve. My work spans the full lifecycle: turning ambiguous requirements into technical models, building across product and platform surfaces, migrating production safely, operating what ships, and raising the engineering quality bar around it.

## Areas of focus

### Authorization systems
Fine-grained and context-aware access control, policy modeling, request-and-approval lifecycles, and Cedar-based evaluation.

### Platform architecture
Modular systems, domain boundaries, event-driven coordination, relational data modeling, and backward-compatible evolution.

### Developer platforms
Multi-language SDK and Terraform generation, API versioning, static analysis, CI, test infrastructure, and operational tooling.

### Technical leadership
Requirements refinement, architecture documents, cross-functional delivery planning, migrations, mentoring, incident response, and internal training.

## Experience

2022–Present
**StrongDM**
Access and authorization platform · Acquired by [Delinea](https://delinea.com/news/delinea-acquires-strongdm-to-secure-ai-with-continuous-authorization)

### Staff Software Engineer

#### Post-acquisition platform integration
Help lead the integration of StrongDM's proxy and core access architecture into Delinea's microservice platform. Selectively preserve and adapt the highest-value product IP while moving from an AWS, Go, and PostgreSQL monolith to an Azure stack built on RabbitMQ, SQL Server, and Cosmos DB, aligning architecture and delivery across newly combined teams.

#### Cross-functional delivery
Lead authorization initiatives with cross-functional partners, turning ambiguous requirements into reviewed technical models and carrying them through sequenced delivery and safe rollout.

#### Access lifecycle ownership
Own the access-request and ephemeral approval domain end to end, from policy design through production operation.

#### Fine-grained access control
Designed and implemented delegated administrative access control that scopes permissions by resource context without granting full administration. Defined policy-safe state transitions and carried the model through every product surface and a backward-compatible migration path.

#### Unified authorization
Designed and implemented a context-aware authorization model that unifies standing, requestable, and time-bound access at a single policy decision point. Established canonical modeling and deterministic projections so intent remains consistent across every user and automation surface.

#### Production migration
Led a backward-compatible migration separating hierarchical group membership from role assignment without disrupting existing behavior or customer configurations.

#### Protocol observability
Designed a terminal protocol parser that reconstructs interactive commands across SSH and Kubernetes streams for structured query logging.

#### API evolution
Evolved SDK and Terraform code generation for versioned APIs while preserving stable client ergonomics and backward compatibility.

#### Integrations & operations
Delivered reliable incident-response integrations. Share on-call ownership of the production system.

#### AI enablement
Facilitated week-long AI engineering bootcamps focused on [techniques developed and documented by StrongDM](https://factory.strongdm.ai/techniques). Helped teammates apply those techniques effectively in day-to-day engineering work.

Build and maintain [F#kYeah](https://github.com/TheFellow/fkyeah), an open-source implementation of the public [Attractor specification](https://factory.strongdm.ai/products/attractor).

Apply [Semport](https://factory.strongdm.ai/techniques/semport) within an Attractor flow to maintain the C# port of the Cedar authorization language from its Go upstream, preserving behavior against the upstream conformance suite and documenting the [engineering lessons](/notes/porting-cedar-semantics-from-go-to-dotnet.md) from that work.

2010–2022
**Applied Underwriters**
Financial services technology

### Software Development Team Leader II

#### Solution architecture
Translated complex business and regulatory requirements into maintainable software, data models, and operational processes across thick-client, service, and REST API systems.

#### System modernization
Introduced domain-driven design, CQRS, functional techniques, and explicit architectural boundaries while modernizing long-lived applications under significant compatibility constraints.

#### Team building
Built and led two development teams, mentored future team leaders, and rewrote the department training program around object-oriented design, SOLID, GRASP, refactoring, and testability.

#### Data & delivery operations
Designed relational schemas and queries, administered production SQL systems, coordinated high-availability migrations, and owned source-control, build, release, and audit workflows.

## Selected engineering work

### [cedar-dotnet](https://github.com/TheFellow/cedar-dotnet)
An idiomatic C# implementation of the Cedar policy language and authorization engine, maintained against the upstream implementation and validated with its 124,000-case official conformance corpus. Benchmark-driven evaluator work made authorization up to 12 times faster while preserving that behavioral contract.

### [F#kYeah](https://github.com/TheFellow/fkyeah)
An open-source implementation of the public [Attractor specification](https://factory.strongdm.ai/products/attractor) with durable graph execution and checkpoint-and-resume support.

### [go-modular-monolith](https://github.com/TheFellow/go-modular-monolith)
A Go reference application that makes modular boundaries and cross-cutting concerns executable across seven bounded contexts and independent CLI, TUI, and desktop clients. A shared pipeline coordinates transactions, events, audit, and Cedar authorization; static analysis and cross-surface tests keep those contracts intact.

### [arch-lint](https://github.com/TheFellow/arch-lint) + [enumstruct](https://github.com/TheFellow/enumstruct)
Production-ready analyzers for architectural boundaries and exhaustive generated unions. Both use the go/analysis framework and integrate with established golangci-lint and go vet workflows.

## Teaching and communication

#### AI engineering enablement
Facilitator for internal AI engineering bootcamps focused on specification-driven development and durable agent workflows.

#### Technical writing and presentations
Write and present implementation-backed explanations of authorization, application architecture, testing, distributed algorithms, and mathematical software, ranging from cross-surface application design and RIBLT set reconciliation to a ground-up tour of ECDSA.

#### Programming education
Created more than 60 tutorials on neural networks, machine learning, and regular expressions, reaching more than 830,000 views and 5,000 subscribers.

#### Mathematics instruction
Former Cal Poly teaching associate for calculus, trigonometry, and algebra.

## Education
### California Polytechnic State University, San Luis Obispo
**Master of Science, Mathematics**<br>**Bachelor of Science, Mathematics**

#### Peer-reviewed research
Published in <em>Linear Algebra and its Applications</em>.

#### Mathematical modeling
Meritorious designation in the Mathematical Contest in Modeling while representing Cal Poly.

## Technology
Go · C# · F# · PSQL · MSSQL · Cedar · GraphQL · gRPC and Protocol Buffers · Terraform · Kubernetes · domain-driven design · static analysis · API and SDK design · CI/CD · production operations
