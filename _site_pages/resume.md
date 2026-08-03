---
title: "Resume"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-08-03 08:23:08 -0700
permalink: /resume/
excerpt: "Staff software engineer specializing in authorization, platform architecture, API evolution, and durable systems."
layout: single
classes: wide
author_profile: false
---

<section class="resume-hero">
  <p class="resume-kicker">Staff Software Engineer</p>
  <h2>Architecture, authorization, and durable systems under real-world constraints</h2>
  <p>I design and deliver systems that have to remain understandable while they evolve. My work spans the full lifecycle: turning ambiguous requirements into technical models, building across product and platform surfaces, migrating production safely, operating what ships, and raising the engineering quality bar around it.</p>
  <div class="resume-contact">
    <a href="mailto:ThomasRyanHarris@gmail.com" aria-label="Email Ryan Harris" title="Email">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>
    </a>
    <a href="https://github.com/TheFellow" aria-label="Ryan Harris on GitHub" title="GitHub">
      <svg class="resume-icon--fill" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.48 2 2 6.58 2 12.23c0 4.52 2.87 8.35 6.84 9.71.5.1.68-.22.68-.49 0-.24-.01-1.05-.02-1.9-2.78.62-3.37-1.21-3.37-1.21-.45-1.18-1.11-1.49-1.11-1.49-.91-.64.07-.63.07-.63 1 .08 1.53 1.06 1.53 1.06.89 1.56 2.34 1.11 2.91.85.09-.66.35-1.11.63-1.36-2.22-.26-4.56-1.14-4.56-5.06 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.71 0 0 .84-.28 2.75 1.05A9.35 9.35 0 0 1 12 6.16c.85 0 1.7.12 2.5.35 1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.45.1 2.71.64.72 1.03 1.63 1.03 2.75 0 3.93-2.34 4.8-4.57 5.05.36.32.68.94.68 1.9 0 1.37-.01 2.47-.01 2.81 0 .27.18.59.69.49A10.25 10.25 0 0 0 22 12.23C22 6.58 17.52 2 12 2Z"/></svg>
    </a>
    <a href="https://www.youtube.com/user/nqramjets/featured" aria-label="Ryan Harris programming tutorials on YouTube" title="YouTube tutorials">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linejoin="round" aria-hidden="true"><path d="M21 8.1a2.7 2.7 0 0 0-1.9-1.9C17.4 5.75 12 5.75 12 5.75s-5.4 0-7.1.45A2.7 2.7 0 0 0 3 8.1 28 28 0 0 0 2.55 12 28 28 0 0 0 3 15.9a2.7 2.7 0 0 0 1.9 1.9c1.7.45 7.1.45 7.1.45s5.4 0 7.1-.45a2.7 2.7 0 0 0 1.9-1.9 28 28 0 0 0 .45-3.9A28 28 0 0 0 21 8.1Z"/><path d="m10 9 5 3-5 3V9Z"/></svg>
    </a>
  </div>
</section>

<section class="resume-section">
  <h2>Areas of focus</h2>
  <div class="resume-focus-grid">
    <article>
      <h3>Authorization systems</h3>
      <p>Fine-grained and context-aware access control, policy modeling, request-and-approval lifecycles, and Cedar-based evaluation.</p>
    </article>
    <article>
      <h3>Platform architecture</h3>
      <p>Modular systems, domain boundaries, event-driven coordination, relational data modeling, and backward-compatible evolution.</p>
    </article>
    <article>
      <h3>Developer platforms</h3>
      <p>Multi-language SDK and Terraform generation, API versioning, static analysis, CI, test infrastructure, and operational tooling.</p>
    </article>
    <article>
      <h3>Technical leadership</h3>
      <p>Requirements refinement, architecture documents, cross-functional delivery planning, migrations, mentoring, incident response, and internal training.</p>
    </article>
  </div>
</section>

<section class="resume-section">
  <h2>Experience</h2>

  <article class="resume-role">
    <div class="resume-role__meta">
      <span class="resume-role__date">2022–Present</span>
      <strong>StrongDM</strong>
      <span>Access and authorization platform · Acquired by <a href="https://delinea.com/news/delinea-acquires-strongdm-to-secure-ai-with-continuous-authorization">Delinea</a></span>
    </div>
    <div class="resume-role__body">
      <h3>Staff Software Engineer</h3>
      <div class="resume-achievements">
        <article class="resume-achievement--band">
          <h4>Post-acquisition platform integration</h4>
          <p>Help lead the integration of StrongDM's proxy and core access architecture into Delinea's microservice platform. Selectively preserve and adapt the highest-value product IP while moving from an AWS, Go, and PostgreSQL monolith to an Azure stack built on RabbitMQ, SQL Server, and Cosmos DB, aligning architecture and delivery across newly combined teams.</p>
        </article>
        <article>
          <h4>Cross-functional delivery</h4>
          <p>Lead authorization initiatives with cross-functional partners, turning ambiguous requirements into reviewed technical models and carrying them through sequenced delivery and safe rollout.</p>
        </article>
        <article>
          <h4>Access lifecycle ownership</h4>
          <p>Own the access-request and ephemeral approval domain end to end, from policy design through production operation.</p>
        </article>
        <article>
          <h4>Fine-grained access control</h4>
          <p>Designed and implemented delegated administrative access control that scopes permissions by resource context without granting full administration. Defined policy-safe state transitions and carried the model through every product surface and a backward-compatible migration path.</p>
        </article>
        <article>
          <h4>Unified authorization</h4>
          <p>Designed and implemented a context-aware authorization model that unifies standing, requestable, and time-bound access at a single policy decision point. Established canonical modeling and deterministic projections so intent remains consistent across every user and automation surface.</p>
        </article>
        <article>
          <h4>Production migration</h4>
          <p>Led a backward-compatible migration separating hierarchical group membership from role assignment without disrupting existing behavior or customer configurations.</p>
        </article>
        <article>
          <h4>Protocol observability</h4>
          <p>Designed a terminal protocol parser that reconstructs interactive commands across SSH and Kubernetes streams for structured query logging.</p>
        </article>
        <article>
          <h4>API evolution</h4>
          <p>Evolved SDK and Terraform code generation for versioned APIs while preserving stable client ergonomics and backward compatibility.</p>
        </article>
        <article>
          <h4>Integrations &amp; operations</h4>
          <p>Delivered reliable incident-response integrations. Share on-call ownership of the production system.</p>
        </article>
        <article>
          <h4>AI enablement</h4>
          <p>Facilitated week-long AI engineering bootcamps focused on <a href="https://factory.strongdm.ai/techniques">techniques developed and documented by StrongDM</a>. Helped teammates apply those techniques effectively in day-to-day engineering work.</p>
          <p>Build and maintain <a href="https://github.com/TheFellow/fkyeah">F#kYeah</a>, an open-source implementation of the public <a href="https://factory.strongdm.ai/products/attractor">Attractor specification</a>.</p>
          <p>Apply <a href="https://factory.strongdm.ai/techniques/semport">Semport</a> within an Attractor flow to maintain the C# port of the Cedar authorization language from its Go upstream, preserving behavior against the upstream conformance suite and documenting the <a href="{{ '/notes/porting-cedar-semantics-from-go-to-dotnet/' | relative_url }}">engineering lessons</a> from that work.</p>
        </article>
      </div>
    </div>
  </article>

  <article class="resume-role">
    <div class="resume-role__meta">
      <span class="resume-role__date">2010–2022</span>
      <strong>Applied Underwriters</strong>
      <span>Financial services technology</span>
    </div>
    <div class="resume-role__body">
      <h3>Software Development Team Leader II</h3>
      <div class="resume-achievements">
        <article>
          <h4>Solution architecture</h4>
          <p>Translated complex business and regulatory requirements into maintainable software, data models, and operational processes across thick-client, service, and REST API systems.</p>
        </article>
        <article>
          <h4>System modernization</h4>
          <p>Introduced domain-driven design, CQRS, functional techniques, and explicit architectural boundaries while modernizing long-lived applications under significant compatibility constraints.</p>
        </article>
        <article>
          <h4>Team building</h4>
          <p>Built and led two development teams, mentored future team leaders, and rewrote the department training program around object-oriented design, SOLID, GRASP, refactoring, and testability.</p>
        </article>
        <article>
          <h4>Data &amp; delivery operations</h4>
          <p>Designed relational schemas and queries, administered production SQL systems, coordinated high-availability migrations, and owned source-control, build, release, and audit workflows.</p>
        </article>
      </div>
    </div>
  </article>
</section>

<section class="resume-section">
  <h2>Selected engineering work</h2>
  <div class="resume-work-grid">
    <article>
      <h3><a href="https://github.com/TheFellow/cedar-dotnet">cedar-dotnet</a></h3>
      <p>An idiomatic C# implementation of the Cedar policy language and authorization engine, maintained against the upstream implementation and validated with its 124,000-case official conformance corpus. Benchmark-driven evaluator work made authorization up to 12 times faster while preserving that behavioral contract.</p>
    </article>
    <article>
      <h3><a href="https://github.com/TheFellow/fkyeah">F#kYeah</a></h3>
      <p>An open-source implementation of the public <a href="https://factory.strongdm.ai/products/attractor">Attractor specification</a> with durable graph execution and checkpoint-and-resume support.</p>
    </article>
    <article>
      <h3><a href="https://github.com/TheFellow/go-modular-monolith">go-modular-monolith</a></h3>
      <p>A Go reference application that makes modular boundaries and cross-cutting concerns executable across seven bounded contexts and independent CLI, TUI, and desktop clients. A shared pipeline coordinates transactions, events, audit, and Cedar authorization; static analysis and cross-surface tests keep those contracts intact.</p>
    </article>
    <article>
      <h3><a href="https://github.com/TheFellow/arch-lint">arch-lint</a> + <a href="https://github.com/TheFellow/enumstruct">enumstruct</a></h3>
      <p>Production-ready analyzers for architectural boundaries and exhaustive generated unions. Both use the go/analysis framework and integrate with established golangci-lint and go vet workflows.</p>
    </article>
  </div>
</section>

<section class="resume-section resume-section--split">
  <div>
    <h2>Teaching and communication</h2>
    <div class="resume-achievements resume-achievements--compact resume-achievements--no-leading-rule">
      <article>
        <h4>AI engineering enablement</h4>
        <p>Facilitator for internal AI engineering bootcamps focused on specification-driven development and durable agent workflows.</p>
      </article>
      <article>
        <h4>Technical writing and presentations</h4>
        <p>Write and present implementation-backed explanations of authorization, application architecture, testing, distributed algorithms, and mathematical software, ranging from cross-surface application design and RIBLT set reconciliation to a ground-up tour of ECDSA.</p>
      </article>
      <article>
        <h4>Programming education</h4>
        <p>Created more than 60 tutorials on neural networks, machine learning, and regular expressions, reaching more than 830,000 views and 5,000 subscribers.</p>
      </article>
      <article>
        <h4>Mathematics instruction</h4>
        <p>Former Cal Poly teaching associate for calculus, trigonometry, and algebra.</p>
      </article>
    </div>
  </div>
  <div>
    <h2>Education</h2>
    <h3>California Polytechnic State University, San Luis Obispo</h3>
    <p><strong>Master of Science, Mathematics</strong><br><strong>Bachelor of Science, Mathematics</strong></p>
    <div class="resume-achievements resume-achievements--compact">
      <article>
        <h4>Peer-reviewed research</h4>
        <p>Published in <em>Linear Algebra and its Applications</em>.</p>
      </article>
      <article>
        <h4>Mathematical modeling</h4>
        <p>Meritorious designation in the Mathematical Contest in Modeling while representing Cal Poly.</p>
      </article>
    </div>
  </div>
</section>

<section class="resume-section resume-technology">
  <h2>Technology</h2>
  <p>Go · C# · F# · PSQL · MSSQL · Cedar · GraphQL · gRPC and Protocol Buffers · Terraform · Kubernetes · domain-driven design · static analysis · API and SDK design · CI/CD · production operations</p>
</section>
