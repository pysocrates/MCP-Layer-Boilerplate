---
feature_id: architecture.routing
area: architecture
system: application-platform

summary: "Portable guide to request routing, layer boundaries, and service placement."

description: 
  This document explains a framework-agnostic request lifecycle for web
  applications, APIs, and worker-driven systems. It helps developers and agents
  decide where logic belongs, how responsibilities should be separated, and how
  the same business rules can be reused across HTTP requests, background jobs,
  and internal automation.

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
  - 01-architecture-and-routing.md
source_globs: []

keywords:
  - architecture
  - routing
  - middleware
  - controllers
  - services
  - data-layer
  - observability

capabilities:
  - architecture.reference
  - request-flow
  - code-placement
  - docs.review

permissions: []

related_docs:
  - 00-index.md

events_emitted: []
automations: []

tasks:
  - determine where new code should live
  - explain the request lifecycle to developers and agents
  - keep framework-specific details separate from architectural rules

invariants:
  - routers stay thin
  - middleware handles cross-cutting concerns
  - controllers translate inputs and outputs
  - services own business rules
  - the data layer owns persistence and external I/O

edge_cases:
  - webhook handlers that need both signature validation and business logic
  - background jobs that reuse service logic without an HTTP request
  - multi-tenant systems that resolve tenant context before business logic runs
---

# Architecture and Routing

Purpose: define a portable request flow that works across most modern backend
stacks.

## Portable request lifecycle

```text
Client or Event Source
  -> Edge Layer
  -> Router
  -> Middleware
  -> Controller or Handler
  -> Service Layer
  -> Data Layer
  -> Response or Side Effect
```

This flow applies to:

- browser requests
- mobile API calls
- webhook deliveries
- internal automation
- background jobs

## Layer responsibilities

### 1. Edge layer

Typical concerns:

- TLS termination
- CDN caching
- request size limits
- coarse rate limiting
- bot or network filtering

Rule: keep business logic out of the edge layer.

### 2. Router

The router decides which handler receives a request.

Typical concerns:

- URL matching
- API versioning
- method-based dispatch
- grouping routes by namespace

Rule: the router should map, not decide.

Bad pattern:

```text
router -> database query -> branching business logic
```

Correct pattern:

```text
router -> controller -> service
```

### 3. Middleware

Middleware handles cross-cutting concerns that apply before or after a handler.

Typical concerns:

- authentication
- tenant resolution
- request logging
- metrics and tracing
- schema validation
- idempotency checks

Rule: middleware should be reusable and should not own domain workflows.

### 4. Controller or handler

Controllers translate an incoming request into a service call and then translate
the result into an HTTP response or job outcome.

Typical concerns:

- parsing input
- invoking the right service
- mapping errors to response codes
- formatting output

Rule: controllers coordinate; they should not contain the core rules of the
business.

### 5. Service layer

The service layer contains the logic that matters to the product or operation.

Examples:

- create an order
- schedule an appointment
- issue a refund
- synchronize a record with an external system

Rule: services should be reusable from more than one entry point. If the same
logic is needed from an API endpoint, a CLI command, and a worker, the logic
belongs here.

### 6. Data layer

The data layer handles persistence and external I/O.

Examples:

- SQL or NoSQL access
- object storage
- message queues
- third-party APIs

Rule: the data layer should not make product decisions. It should store,
retrieve, and transmit data reliably.

## Real-world implications

These rules matter because they reduce rewrite risk:

- A new mobile app can reuse the same services as the web API.
- A worker can process retries without duplicating business rules.
- A webhook handler can validate signatures in middleware and pass the payload
  into an existing service.
- A framework migration is easier when domain logic is not trapped inside
  routes, controllers, or ORM models.

## Where new logic should go

Use these decision rules:

- If it chooses the destination handler, it belongs in the router.
- If it applies broadly to many requests, it belongs in middleware.
- If it converts input or output, it belongs in a controller or handler.
- If it enforces product or workflow rules, it belongs in a service.
- If it stores data or talks to another system, it belongs in the data layer.

## Minimal example

For `POST /orders`:

- router matches `POST /orders`
- middleware authenticates the caller and attaches request metadata
- controller parses the payload and calls `create_order`
- service validates inventory, pricing, and workflow rules
- data layer writes the order and calls any external systems
- controller returns the created order or a structured error

The same `create_order` service should also be usable from:

- an admin CLI tool
- a retry worker
- a bulk import job

## Observability

Every important path should expose:

- structured logs
- metrics
- trace or request identifiers

This makes production debugging possible without coupling observability logic to
business rules.

## Common mistakes

- placing business logic in controllers because it feels faster initially
- letting middleware become a second service layer
- querying the database directly from routing code
- embedding framework-specific assumptions into otherwise reusable services

## How agents should use this document

Agents should use this document as a placement guide before creating code. It is
meant to answer: "where should this logic live?" without needing a full scan of
the repository.
