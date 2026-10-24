---
name: OnHandRecallLedger
description: Retrieve bounded historical context and manage explicitly submitted Knowledge through scoped real-use validation.
---

# OnHandRecallLedger

Version 1.0.0. OnHand Family Closed-Source Distribution License (see LICENSE). Copyright (c) 2026 OnHand Core.

Call when the Host explicitly requests historical Recall, admits/publishes a
chosen Recall item, submits a Knowledge claim, supplies real-use validation,
declares a lifecycle relation, or authorizes erasure. No self-activation.
The Host owns semantic judgment, present applicability, and workflow continuation.
Recall is non-authority; Trusted Knowledge is not current Authority.

## Standalone installation and entry

This distribution requires Windows x64 CPython 3.12.14, magic cb0d0d0a,
optimization 0. Python is obtained separately. From the clean extracted home,
run `python -B install.py --skill-area <chosen ONHAND_SKILL_AREA root>`.
Only a fresh owned home is installed; no source build, pip install, automatic
Host configuration, formal registration or migration occurs. The thin launcher
is `python -B <installed home>/invoke.py --skill-area <chosen root>`.
Send one UTF-8 JSON request on stdin; stdout returns JSON. Module/console
installation is not provided by this directory distribution. See INSTALLATION.md.

## Legacy public contract 1.0 (17 operations)

Schema `ONHAND_RECALLLEDGER_PUBLIC_OPERATION_V1`, contract version `1.0`.
Required request keys: `contract_version`, `operation_name`, `operation_id`,
`owner_namespace`, `request_digest`, `payload`. Existing revision-bearing mutation
targets additionally require `expected_record_revision`. Digest is SHA-256 of
UTF-8 JSON with sorted keys, no whitespace, literal Unicode, and no nonfinite
numbers; exclude the digest field itself. IDs are nonempty strings of at most
512 characters; top_k is an integer from 1 through 100.

These are the 17 legacy public operations, retaining request/response contract 1.0; fields listed here are required payload facts. The complete current set has 18 operations; host.material.request uses contract 1.1 as specified below.

| Operation | Payload |
| --- | --- |
| recall.retrieve | generalized_query, scopes, top_k |
| recall.admit | task_run_id, semantic_revision, source_id, items |
| recall.publish | publication_operation_id, working_item_id, task_run_id, semantic_revision, content_digest |
| recall.lifecycle.mutate | capsule_id, action, expected_record_revision |
| recall.cleanup.preview | selection_criteria, top_k |
| recall.settings.read | {} |
| recall.settings.update | recall_enabled, expected_settings_revision |
| knowledge.candidate.submit | knowledge_body, claim_scope, classification_path (three opaque labels) |
| knowledge.search | query, top_k |
| knowledge.read | knowledge_id; optional content_revision |
| knowledge.validation.open | knowledge_id, content_revision, knowledge_body_digest, validation_use_id, validation_epoch, operation_id |
| knowledge.validation.settle | ticket_id, knowledge_id, content_revision, knowledge_body_digest, validation_use_id, validation_epoch, outcome, evidence_refs |
| knowledge.conflict.apply | affected (exact identities/revisions/digests), decision |
| knowledge.revision.apply | action, targets (exact identities/revisions/digests), action-specific facts |
| event.ingest | event_id, event_kind, task_run_id, semantic_revision, scope_id, sequence, payload_digest, contract_version, payload |
| run.lifecycle.apply | action, task_run_id, lifecycle_owner_ref, lifecycle_owner_revision, action-specific revision facts |
| erasure.execute | delete_operation_id, delete_scope, erasure_authorization, scope-specific target |

Recall admission items carry semantic_body and scope; scopes are GLOBAL or an
explicit PROJECT identity. Admission requires an explicitly registered accepted
task revision; it creates non-retrievable working items. Publication identity
matches the public operation id. Lifecycle actions are SUPERSEDE (explicit
successor_capsule_id) or RETIRE. Settings default recall_enabled=true. OFF returns
DISABLED for retrieval and new admission/publication, preserves existing Recall,
and leaves Knowledge unaffected. No Profile engine or legacy auto-migration.

Validation binds the exact current record revision, content digest, use and epoch;
task_run_id/task_semantic_revision and expected evidence refs apply when present.
PASS, FAIL or INCONCLUSIVE is supplied by the Host. Countable PASS requires valid
immutable validation_effective_at. One logical use counts at most once. Candidate
needs three consecutive PASS; Trusted expires on access after seven days. Search
and read never validate. Conflict decisions are REAL_CONFLICT, FALSE_CONFLICT,
INCONCLUSIVE; explicit resolution supplies action and targets. Revision actions
are CREATE_CONTENT_REVISION (new_body, new_scope, current_claim_identity) or
APPLY_REPLACEMENT_RELATION (replaced_identity, replacement_identity). Old replaced
body is removed immediately; semantic revisions inherit no Trust.

Legal events are ROOT_CAPSULE, WORK_UNIT_COMPLETED, RUN_FINALIZED, with exact
portable kind-specific bodies and digests. AUTHORITY_CAPSULE is private and illegal
ingress. Raw reasoning is forbidden. REGISTER_OWNER requires semantic_revision;
ACCEPT_SUCCESSOR_REVISION requires old_semantic_revision, new_semantic_revision,
expected_lifecycle_record_revision and exact owner proof. No automatic replay,
backfill, Recall publication, or Knowledge creation follows an event.

Erasure requires erasure_authorization=true and delete_operation_id matching the
public operation id. OBJECT supplies object_type (RECALL or KNOWLEDGE), object_id
and expected revision when applicable; SOURCE_REVISION supplies source_id and
source_revision; SOURCE_LINEAGE supplies source_id. Barrier commits first.
PENDING/PARTIAL retries resume the same operation; COMPLETE covers managed
surfaces only and never unknown external copies.

Result keys: contract_version, operation_name, operation_id, status, result_class,
result_digest; data/error when applicable. Digest excludes result_digest. Status:
OK, NO_MATCH, DISABLED, PENDING, PARTIAL, COMPLETE, NOT_FOUND, STALE, CONFLICT,
MALFORMED, UNSUPPORTED_VERSION, REJECTED. Malformed or missing facts fail closed;
ambiguous facts are never semantically guessed. Same operation id/digest replays
the committed result or idempotent acknowledgement; different digest conflicts.
Debug, index, transaction, restore and importer internals are not public.

## Host capsule/material request — two triggers

This Skill never reasons. Where semantic capsule material is required the Host
performs the semantic judgment; the Skill only detects the need and offers the
request. Both triggers below use the SAME existing Host-request boundary over the
public operation contract. That boundary is a request/response boundary, not a
runtime, service, coordinator or shared store.

A required capsule/source semantic object may be requested from Host when EITHER:

TRIGGER A (original) — an operation requires a Capsule/source semantic object and
no legal ingress or producer supplies it.

TRIGGER B (light-task result) — all of the following hold together:

- the task correctly received DRUDGE_ADMISSION=LIGHT_TASK_BYPASS;
- the task reached a meaningful completion/evidence boundary;
- the completed result contains materially reusable information already inside
  this Skill's existing admission, knowledge or recall scope;
- no suitable legal capsule/material is already available.

DRUDGE_ADMISSION=LIGHT_TASK_BYPASS alone implies neither RECALL_VALUE=YES nor a
capsule/material request.

After either trigger the downstream path is the existing one only: Host supplies
the legal existing capsule/material, the Skill mechanically validates and adopts
it, and the existing Candidate/Trusted, Knowledge and Recall lifecycle applies.
There is no second downstream pipeline.

Preserved without exception:

- Fast no-op path. A light task with no meaningful reusable information produces
  no request and no durable mutation. This Skill is not a task log: typo
  corrections, routine successful commands, ordinary build/test passes with no
  reusable discovery, temporary one-off execution facts, and information already
  adequately represented remain no-ops.
- Duplicate/convergence. Existing duplicate, convergence and no-useful-update
  semantics stay authoritative; completing a new task never creates log noise.
- Completion/evidence gate. Guesses, speculative causes, unverified fixes,
  incomplete results and transient intermediate state never become durable
  knowledge. Existing Candidate/Trusted and evidence rules stay authoritative.
- Scope. Requesting material never expands what this Skill may retain; only
  existing admission/knowledge/recall scope is eligible.
- Non-reasoning. The Skill only mechanically decides that a defined request
  condition is met. It never authors the semantic conclusion, and no reasoning
  engine or LLM reasoning is added inside it.
- Drudge independence. Drudge is never invoked to manufacture knowledge input and
  is never modified. No STRUCTURED admission, Decomposed Hybrid, Work Unit, JIT
  execution JSON, handoff, or completion/seal evidence is generated for this
  path, and no false Drudge lineage is created.
- No shared runtime. No shared Hybrid Capsule runtime, shared capsule database,
  capsule lifecycle coordinator, new cross-Skill writable state, second shared
  runtime or global capsule owner is created.
- No new producer schema. Only the existing legal Host-supplied material forms
  are used; no producer, requested_by, origin or admission-type fields are
  introduced.
- Lifecycle. SESSION_RESIDENT does not authorize polling, file watching,
  background scanning, a hidden scheduler, a global task observer or autonomous
  interception. Trigger B is evaluated only through the existing legal
  Host/Skill interaction boundary, and the Host supplies light-task
  completion/evidence context through that existing public path.
- No replay/backfill. This rule is prospective only: historical light tasks are
  never scanned, reconstructed or backfilled.
- Validation. Material returned by Host is validated exactly as before. Neither
  trigger bypasses, weakens or replaces validation.

## Current eighteenth operation and full public references

host.material.request is the eighteenth public operation, with EVALUATE and SETTLE.
Both request and response use contract_version="1.1". The preceding 17 operations
accept and return "1.0", and reject "1.1" with UNSUPPORTED_VERSION. The new operation
rejects "1.0" with UNSUPPORTED_VERSION. Nested material_operation is a legal "1.0"
knowledge.candidate.submit or recall.admit request. Product version remains 1.0.0.

Host MUST read [the full material request contract](references/public-material-request.md)
and [the operation/version and exact-field inventory](references/public-contract.json)
relative to this SKILL.md before using EVALUATE/SETTLE. They are required public
package contents, not private construction reports. Missing or hash-mismatched
references make the package incomplete and mounting fails.
[Distribution manifest](RELEASE_MANIFEST.json) fixes the SHA256 of
this entry and references; it grants no review, registration or deployment.

EVALUATE checks Host snapshot and current accepted task revision without saving
historical pending. SETTLE atomically commits adoption plus receipt in the target's
owning transaction: Knowledge Store for Candidate, Recall history for Working.
Knowledge's final EventLifecycle current-revision check is under the owning gate
held through stage/install. Exact retry rechecks lifecycle, lineage, deletion
barrier and Recall enabled state before replay. Candidate is not automatically
Trusted; Working is not automatically published. Receipt does not prove Host
semantic correctness, identity authenticity, evidence truth or historical sending.
Full fields, digest/identity rules and recovery boundaries are in the references.

## Windows, optional WSL, and resident entry

The CLI uses --skill-area and optional --current-project; ONHAND_SKILL_AREA and
ONHAND_CURRENT_PROJECT remain Windows Host edge defaults. The WSL adapter uses
only Windows Python and the same Windows root. Example argument shape:
`python3 wsl_entry.py --windows-python <Windows python.exe path> --skill-area <WSL path to chosen Windows ONHAND_SKILL_AREA>`.
WSL interoperation is not revalidated for this bytecode build. Native Linux and
macOS Core are unsupported. There is one Windows root LockFileEx domain.
Unknown legacy residue, linked roots and old module-cache origins fail closed;
no automatic migration, lock deletion or PID-based cleanup is provided.

resident_entry.py remains a thin entry to the same single Core. Its startup
isolated_target.json has exactly series_root, an absolute canonical root generated
at installation. It is not a second store. A fresh executor is required after a
version change. This distribution adds interpreter preflight only at its edges.

## Optional formal connection boundary

COMBINED_MODE = SUPPORTED subject to a compatible separately installed
Thoroughfare and this distribution's own bounded wiring review and registration.
ATTACHMENT_MODE = SESSION_RESIDENT. FINAL_RETURN_TOPOLOGY = RESIDENT_LINE.
PUBLIC_SESSION_ATTACHMENT_ENTRY = OnHandRecallLedger/resident_entry.py.
COMMON_HOST_RETURN = NOT REQUIRED. A direct resident call is not formal attachment.
One Skill identity, one Core and one resident attachment carry Recall, Knowledge,
common operations and event.ingest. No separate semantic providers are created.
Do not copy another installation's Binding/line numbers or session attachments.
This distribution has changed public-contract bytes; prior review of another
digest does not approve these bytes. No new Combined registration is authorized.
The public references' retained historical labels do not approve this distribution.

The Host owns semantic judgment and authorization. event.ingest does not itself
admit or publish Recall, submit Knowledge or award PASS. Returned results never
grant current execution authority. SELF_ACTIVATION = NO. POLLING = NO.
HOST_SCAN = NO. PROMPT_INTERCEPTION = NO. BACKGROUND_DAEMON = NONE.
DRUDGE_HARD_DEPENDENCY = NONE. Standalone requires no other Skill.
Session end invalidates the Host-side attachment; no automatic reconnect occurs.

## Program removal and data boundary

Stop new calls and drain work before disabling Host discovery or closing the legal
Combined session. `manage.py uninstall --skill-area <chosen root> --quiescent --retain-data`
removes only manifest-listed program members while holding the existing Core root
lock. It retains state, barriers, journals, anchor and the installation record.
Only the same artifact can restore program files using install.py --restore-program.
This is not an erasure or migration API. User-authorized erasure.execute remains
the only public content erasure operation, with its existing bounded guarantees.
