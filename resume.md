---
title: "Resume"
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
    <a href="mailto:ThomasRyanHarris@gmail.com">ThomasRyanHarris@gmail.com</a>
    <a href="https://github.com/TheFellow">GitHub</a>
    <a href="https://www.youtube.com/user/nqramjets/featured">Technical tutorials</a>
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
      <p>Architecture documents, cross-team migrations, mentoring, incident response, internal training, and AI-assisted development workflows.</p>
    </article>
  </div>
</section>

<section class="resume-section">
  <h2>Experience</h2>

  <article class="resume-role">
    <div class="resume-role__meta">
      <span class="resume-role__date">2022 — Present</span>
      <strong>StrongDM</strong>
      <span>Access and authorization platform</span>
    </div>
    <div class="resume-role__body">
      <h3>Staff Software Engineer</h3>
      <p class="resume-role__subtitle">Promoted from Senior Software Engineer</p>
      <ul>
        <li>Own major portions of the access-request and approval domain, from data model and policy evaluation through API, CLI, administrative UI, notifications, audit, and production operation.</li>
        <li>Designed fine-grained and context-aware authorization architectures that unify standing access, just-in-time requests, conditional policy, and reusable configuration behind a coherent model.</li>
        <li>Led a backward-compatible production migration that separated hierarchical group membership from role assignment while preserving behavior across services, SDKs, CLI workflows, audit, and existing customer configurations.</li>
        <li>Extended policy enforcement and discovery for Kubernetes and delivered third-party incident-response integrations with resilient synchronization, lifecycle cleanup, permissions, rate limits, and end-to-end tests.</li>
        <li>Evolved multi-language SDK and Terraform code generation to support versioned APIs and complex union types without exposing transport plumbing or breaking existing clients.</li>
        <li>Operate the production system through on-call rotations and incident response, carrying design decisions through deployment, observability, failure recovery, and long-term maintenance.</li>
        <li>Facilitate internal AI engineering bootcamps and apply specification-driven agent workflows to production work; build and maintain F#kYeah, an open-source F# implementation of the Attractor pipeline model.</li>
      </ul>
    </div>
  </article>

  <article class="resume-role">
    <div class="resume-role__meta">
      <span class="resume-role__date">2010 — 2022</span>
      <strong>Applied Underwriters</strong>
      <span>Financial services technology</span>
    </div>
    <div class="resume-role__body">
      <h3>Software Development Team Leader II</h3>
      <p class="resume-role__subtitle">Progressed from Financial Technical Analyst through Team Leader I and II</p>
      <ul>
        <li>Translated complex business and regulatory requirements into maintainable software, data models, and operational processes across thick-client, service, and REST API systems.</li>
        <li>Introduced domain-driven design, CQRS, functional techniques, and explicit architectural boundaries while modernizing long-lived applications under significant compatibility constraints.</li>
        <li>Built and led two development teams, mentored future team leaders, and rewrote the department training program around object-oriented design, SOLID, GRASP, refactoring, and testability.</li>
        <li>Designed relational schemas and queries, administered production SQL systems, coordinated high-availability migrations, and owned source-control, build, release, and audit workflows.</li>
      </ul>
    </div>
  </article>
</section>

<section class="resume-section">
  <h2>Selected engineering work</h2>
  <div class="resume-work-grid">
    <article>
      <h3><a href="https://github.com/TheFellow/cedar-dotnet">cedar-dotnet</a></h3>
      <p>A C# implementation of the Cedar policy language, semantically ported from cedar-go and validated against the official conformance corpus.</p>
    </article>
    <article>
      <h3><a href="https://github.com/TheFellow/fkyeah">F#kYeah</a></h3>
      <p>An F# engine for graph-defined, multi-stage AI workflows with checkpoints, simulation, multi-provider execution, and a broad conformance suite.</p>
    </article>
    <article>
      <h3><a href="https://github.com/cedar-policy/cedar-go">cedar-go contributor</a></h3>
      <p>Contributions to the official Go implementation include EntityUID serialization and stricter parsing behavior for Cedar extension types.</p>
    </article>
    <article>
      <h3><a href="https://github.com/TheFellow">Architecture and analysis tools</a></h3>
      <p>Open-source work includes architectural dependency enforcement, exhaustive union handling, modular-monolith reference applications, and simulation projects.</p>
    </article>
  </div>
</section>

<section class="resume-section resume-section--split">
  <div>
    <h2>Teaching and communication</h2>
    <ul>
      <li>Facilitator for internal AI engineering bootcamps focused on specification-driven development and durable agent workflows.</li>
      <li>Presenter of technical talks that make difficult material approachable, including a ground-up tour of elliptic-curve cryptography from groups and finite fields through ECDSA.</li>
      <li>Created more than 60 programming tutorials on neural networks, machine learning, and regular expressions, reaching more than 830,000 views and 5,000 subscribers.</li>
      <li>Former Cal Poly teaching associate for calculus, trigonometry, and algebra.</li>
    </ul>
  </div>
  <div>
    <h2>Education</h2>
    <h3>California Polytechnic State University, San Luis Obispo</h3>
    <p><strong>Master of Science, Mathematics</strong><br><strong>Bachelor of Science, Mathematics</strong></p>
    <ul>
      <li>Published peer-reviewed research in <em>Linear Algebra and its Applications</em>.</li>
      <li>Received a Meritorious designation representing Cal Poly in the Mathematical Contest in Modeling.</li>
      <li>Summer research participant, 2008.</li>
    </ul>
  </div>
</section>

<section class="resume-section resume-technology">
  <h2>Technology</h2>
  <p>Go · C# · F# · PostgreSQL · Cedar · GraphQL · gRPC and Protocol Buffers · Terraform · Kubernetes · domain-driven design · static analysis · API and SDK design · CI/CD · production operations</p>
</section>
