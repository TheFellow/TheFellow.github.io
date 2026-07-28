#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "fileutils"
require "cgi"
require "yaml"

ROOT = File.expand_path("..", __dir__)
SITE_URL = "https://thefellow.github.io"

# Deliberately authored rather than mechanically truncated. These are the two
# smallest levels of each page's pyramid; the front-matter excerpt is the next.
SUMMARIES = {
  "/" => ["Engineering notes", "Public notes connecting software architecture to working projects."],
  "/projects/" => ["Project catalog", "Open-source projects with design context beyond their repository READMEs."],
  "/guides/" => ["Practical guides", "Long-form guides turning architecture principles into testable working designs."],
  "/notes/" => ["Technical notes", "Focused observations drawn from active projects, experiments, and research."],
  "/resume/" => ["Engineering experience", "Staff-level experience in authorization, architecture, delivery, and technical leadership."],
  "/404.html" => ["Missing page", "Navigation help when a requested page cannot be found."],
  "/projects/go-modular-monolith/" => ["Executable architecture", "A Go reference app enforcing modular boundaries and cross-cutting concerns."],
  "/projects/cedar-dotnet/" => ["Cedar for .NET", "A semantic Cedar implementation with idiomatic C# APIs and conformance tests."],
  "/projects/arch-lint/" => ["Enforced boundaries", "A Go analyzer that makes architectural dependency rules build-time checks."],
  "/projects/fkyeah/" => ["Agent pipelines", "An F# engine executing inspectable, resumable AI workflows from DOT graphs."],
  "/projects/enumstruct/" => ["Exhaustive unions", "A Go analyzer that detects missing pointer-union cases as models evolve."],
  "/projects/fluid/" => ["Fluid simulation", "An interactive Go playground for exploring two-dimensional Eulerian fluid dynamics."],
  "/projects/value-types/" => ["Structural equality", "A compact C# library for modeling value-object equality and composition."],
  "/guides/building-high-quality-software/" => ["Architecture lessons", "Eleven lessons that turn architectural intent into executable software constraints."],
  "/guides/building-an-application-tui-toolkit/" => ["Testable TUI", "How Mixology adapts MVVM and Elm ideas into an application toolkit."],
  "/notes/elliptic-curve-cryptography-from-first-principles/" => ["ECDSA foundations", "A ground-up route through groups, finite fields, curves, and signatures."],
  "/notes/porting-cedar-semantics-from-go-to-dotnet/" => ["Semantic porting", "How conformance tests preserve Cedar behavior while C# APIs remain idiomatic."]
}.freeze

def parse_document(path)
  text = File.read(path)
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
  raise "Missing front matter: #{path}" unless match

  data = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true) || {}
  data["source"] = path.delete_prefix("#{ROOT}/")
  data["body"] = match[2].strip
  data
end

def documents
  patterns = %w[_site_pages/*.md _projects/*.md _guides/*.md _posts/*.md]
  patterns.flat_map { |pattern| Dir[File.join(ROOT, pattern)] }.sort.map { |path| parse_document(path) }
end

def route_for(doc)
  return doc.fetch("permalink") if doc["permalink"]

  source = doc.fetch("source")
  return "/projects/#{File.basename(source, '.md')}/" if source.start_with?("_projects/")
  return "/guides/#{File.basename(source, '.md')}/" if source.start_with?("_guides/")

  raise "No public route for #{source}"
end

def markdown_path(route)
  return "index.md" if route == "/"
  return "#{route.delete_prefix('/')}index.md" if route.end_with?("/") && route == "/"

  "#{route.delete_prefix('/').sub(%r{/$}, '')}.md"
end

def clean_body(body)
  strip_layout_indentation = body.include?('class="resume-hero"')
  body = body.gsub(/\{\{\s*['\"]([^'\"]+)['\"]\s*\|\s*relative_url\s*\}\}/, '\\1')
  body = body.gsub(/\{:\s*[^}]+\}/, "")
  body = body.gsub(%r{<div class="project-meta">.*?</div>}m, "")
  body = body.gsub(%r{<svg\b.*?</svg>}m, "")
  body = body.gsub(%r{</?(?:section|article|div)(?:\s[^>]*)?>}i, "")
  body = body.gsub(%r{<h2[^>]*>(.*?)</h2>}mi, "## \\1")
  body = body.gsub(%r{<h3[^>]*>(.*?)</h3>}mi, "### \\1")
  body = body.gsub(%r{<h4[^>]*>(.*?)</h4>}mi, "#### \\1")
  body = body.gsub(%r{<p[^>]*>(.*?)</p>}mi, "\\1\n")
  body = body.gsub(%r{<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>}mi, '[\\2](\\1)')
  body = body.gsub(%r{<strong[^>]*>(.*?)</strong>}mi, '**\\1**')
  body = body.gsub(%r{<span[^>]*>(.*?)</span>}mi, '\\1')
  body = body.gsub(%r{<li[^>]*>(.*?)</li>}mi, "- \\1")
  body = body.gsub(%r{</?(?:ul|ol)(?:\s[^>]*)?>}i, "")
  body = body.gsub(/\[\s*\]\([^)]*\)/m, "")
  body = body.gsub(/\{%.+?%\}/m, "")
  body = body.lines.map(&:strip).join("\n") if strip_layout_indentation
  CGI.unescapeHTML(body.gsub(/\n{3,}/, "\n\n").strip)
end

def collection_index(doc, all_docs)
  route = route_for(doc)
  selected = case route
             when "/projects/" then all_docs.select { |item| item["source"].start_with?("_projects/") }
             when "/guides/" then all_docs.select { |item| item["source"].start_with?("_guides/") }
             when "/notes/" then all_docs.select { |item| item["source"].start_with?("_posts/") }
             else return nil
             end
  intro = clean_body(doc["body"].split(/<div class="feature-tiles">/, 2).first).strip
  links = selected.sort_by { |item| item["order"] || item["date"] || 0 }.map do |item|
    item_route = route_for(item)
    "- [#{item.fetch('title')}](#{item_route}) ([Markdown](/#{markdown_path(item_route)})): #{item.fetch('excerpt')}"
  end
  "#{intro}\n\n#{links.join("\n")}"
end

def home_body(all_docs)
  %w[/projects/ /guides/ /notes/ /resume/].map do |route|
    doc = all_docs.find { |item| route_for(item) == route }
    "- [#{doc.fetch('title')}](#{route}) ([Markdown](/#{markdown_path(route)})): #{SUMMARIES.fetch(route)[1]}"
  end.join("\n")
end

def render_page(doc, all_docs)
  route = route_for(doc)
  short, medium = SUMMARIES.fetch(route) { raise "Missing pyramid summary for #{route}" }
  body = if route == "/"
           home_body(all_docs)
         else
           collection_index(doc, all_docs) || clean_body(doc["body"])
         end
  excerpt = doc["excerpt"] || medium
  <<~MARKDOWN
    <!-- Generated from #{SITE_URL}#{route} by scripts/generate_llm_content.rb; do not edit. -->

    # #{doc.fetch("title")}

    Source: [#{SITE_URL}#{route}](#{SITE_URL}#{route})

    ## Pyramid summary

    - **~2 words:** #{short}
    - **~8 words:** #{medium}
    - **Expanded:** #{excerpt}

    ## Full content

    #{body}
  MARKDOWN
end

def write_if_changed(relative_path, content)
  path = File.join(ROOT, relative_path)
  FileUtils.mkdir_p(File.dirname(path))
  return if File.exist?(path) && File.read(path) == content

  File.write(path, content)
end

# Remove obsolete alternates when a source page is deleted or its route changes.
# Only files carrying this generator's marker are eligible.
Dir[File.join(ROOT, "**/*.md")].each do |path|
  first_line = File.open(path, &:readline) rescue ""
  FileUtils.rm_f(path) if first_line.include?("Generated from #{SITE_URL}") && first_line.include?("generate_llm_content.rb")
end

docs = documents
routes = docs.to_h { |doc| [route_for(doc), doc] }
missing = routes.keys - SUMMARIES.keys
stale = SUMMARIES.keys - routes.keys
raise "Missing summaries: #{missing.join(', ')}" unless missing.empty?
raise "Stale summaries: #{stale.join(', ')}" unless stale.empty?

rendered = routes.transform_values { |doc| render_page(doc, docs) }
rendered.each { |route, content| write_if_changed(markdown_path(route), content) }

core_routes = %w[/ /projects/ /guides/ /notes/ /resume/]
sections = {
  "Start Here" => core_routes,
  "Projects" => routes.keys.grep(%r{\A/projects/.+/$}),
  "Guides" => routes.keys.grep(%r{\A/guides/.+/$}),
  "Notes" => routes.keys.grep(%r{\A/notes/.+/$})
}
llms = [
  "# Ryan Harris — Engineering in Public",
  "",
  "> Software architecture, developer tools, authorization, and AI workflow notes connected to working open-source projects.",
  "",
  "This is the compact level of a three-level context pyramid: follow a Markdown link for a page summary and full article, or use [llms-full.txt](#{SITE_URL}/llms-full.txt) for the complete site corpus. Source repositories are linked from their project pages."
]
sections.each do |heading, section_routes|
  llms << "\n## #{heading}\n"
  section_routes.sort.each do |route|
    doc = routes.fetch(route)
    llms << "- [#{doc.fetch('title')}](#{SITE_URL}/#{markdown_path(route)}): #{SUMMARIES.fetch(route)[1]}"
  end
end
write_if_changed("llms.txt", "#{llms.join("\n")}\n")

full = [
  "# Ryan Harris — Full Site Context",
  "",
  "> Generated full-text companion to [llms.txt](#{SITE_URL}/llms.txt). Prefer the compact index when context is limited.",
  ""
]
routes.keys.reject { |route| route == "/404.html" }.sort.each do |route|
  full << rendered.fetch(route)
  full << "\n---\n"
end
write_if_changed("llms-full.txt", "#{full.join("\n")}\n")

puts "Generated #{rendered.size} page alternates, llms.txt, and llms-full.txt"
