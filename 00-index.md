---
feature_id: mcp_example.index
area: documentation
system: mcp-example

summary: "Portable index for a small MCP-ready documentation set."

description: >
  This document is the entry point for a minimal knowledge base that can be
  shipped with an MCP example repository. It is intentionally generic so the
  structure can be reused across products, frameworks, and deployment models.
  Each linked document should explain a single topic well enough for both
  humans and agents to act without scanning the entire codebase.

personas:
  - developer
  - operator
  - agent

surfaces:
  - docs
  - knowledge_base
  - internal_reference

ui_routes: []
api_endpoints: []

related_models: []
source_files:
  - 00-index.md
  - 01-architecture-and-routing.md
source_globs: []

keywords:
  - documentation
  - index
  - architecture
  - routing
  - knowledge-base
  - mcp

capabilities:
  - docs.discover
  - docs.navigation
  - docs.reference
  - architecture.reference

permissions: []

related_docs:
  - 01-architecture-and-routing.md

events_emitted: []
automations: []

tasks:
  - find the correct document for a question
  - understand how the example knowledge base is organized
  - extend the documentation set without introducing repo-specific assumptions

invariants:
  - every listed document must exist
  - every document should cover one topic clearly
  - examples should stay framework-agnostic unless a framework is the topic

edge_cases:
  - a document becomes too broad and overlaps another topic
  - an index entry points to a file that no longer exists
  - a supposedly generic example starts depending on one product domain
---

# Documentation Index

Purpose: provide a small, portable map of the documentation shipped with this
MCP example.

## Current documents

- `01-architecture-and-routing.md`: explains the request lifecycle, layer
  boundaries, and where new logic should live in a typical web application or
  API service.

## Why this structure works for a proof of concept

- It is small enough to understand quickly.
- It uses metadata that an MCP server or agent can index reliably.
- It focuses on decisions that matter in real systems: routing, service
  boundaries, observability, and portability.

## How to extend this example

Add new documents only when they represent a distinct concern. Good next topics
for a real repository would be:

- authentication and authorization
- background jobs and task processing
- integrations and external APIs
- data models and persistence
- observability and operations

## Authoring rules

- Keep file names stable so agents can reference them consistently.
- Prefer generic patterns over business-specific workflows.
- Include concrete examples, but avoid coupling the examples to one company,
  one framework, or one deployment platform.
