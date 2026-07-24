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
      <span class="resume-role__date">2022 — Present</span>
      <strong>StrongDM</strong>
      <span>Access and authorization platform</span>
    </div>
    <div class="resume-role__body">
      <h3>Staff Software Engineer</h3>
      <div class="resume-achievements">
        <article>
          <h4>Cross-functional delivery</h4>
          <p>Lead authorization initiatives across product, security, design, and engineering: refine ambiguous requirements into reviewed technical models, sequence the deliverables, and coordinate implementation and production rollout.</p>
        </article>
        <article>
          <h4>Access lifecycle ownership</h4>
          <p>Own major portions of the access-request and approval domain, from data model and policy evaluation through API, CLI, administrative UI, notifications, audit, and production operation.</p>
        </article>
        <article>
          <h4>Production migration</h4>
          <p>Led a backward-compatible migration that separated hierarchical group membership from role assignment while preserving behavior across services, SDKs, CLI workflows, audit, and existing customer configurations.</p>
        </article>
        <article>
          <h4>Protocol observability</h4>
          <p>Designed a terminal protocol parser that reconstructs interactive commands across SSH and Kubernetes streams for structured query logging, accounting for escape sequences, resizing, pasted input, command history, and interactive applications.</p>
        </article>
        <article>
          <h4>API evolution</h4>
          <p>Evolved multi-language SDK and Terraform code generation to support versioned APIs and complex union types without exposing transport plumbing or breaking existing clients.</p>
        </article>
        <article>
          <h4>Integrations &amp; operations</h4>
          <p>Delivered incident-response integrations with resilient synchronization and lifecycle handling; operate the production system through on-call rotations, incident response, observability, and failure recovery.</p>
        </article>
        <article>
          <h4>AI enablement</h4>
          <p>Facilitate internal AI engineering bootcamps and apply specification-driven agent workflows to production work; build and maintain F#kYeah, an open-source F# implementation of the public <a href="https://factory.strongdm.ai/products/attractor">Attractor specification</a>.</p>
        </article>
      </div>
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
      <p>A C# implementation of the Cedar policy language, semantically ported from cedar-go and validated against the official conformance corpus.</p>
    </article>
    <article>
      <h3><a href="https://github.com/TheFellow/fkyeah">F#kYeah</a></h3>
      <p>An F# implementation listed among the community implementations of the public <a href="https://factory.strongdm.ai/products/attractor">Attractor specification</a>, with checkpoints, simulation, and multi-provider execution.</p>
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
