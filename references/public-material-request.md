# Public material request contract

Product 1.0.0; schema ONHAND_RECALLLEDGER_PUBLIC_OPERATION_V1.
Required public reference. New distribution wiring review remains separate.

## Common envelope, digests and types

host.material.request has exactly six request keys: contract_version,
operation_name, operation_id, owner_namespace, request_digest, payload.
contract_version="1.1"; operation_name="host.material.request".
Existing 17 operations remain "1.0", including nested material. Other versions
return UNSUPPORTED_VERSION.

H(x) is lower-case hexadecimal SHA256 of canonical UTF-8 JSON:
ensure_ascii=false, sort_keys=true, separators=(",",":"), allow_nan=false.
request_digest=H(entire request excluding only request_digest).
Original and nested envelopes each have an independently checked request_digest.
result_digest=H(entire response excluding only result_digest).
Strings are not trimmed/normalized. Digests do not authenticate Host identity.
Identity is a non-whitespace-only string of 1–512 characters.
Revision is a strict nonnegative integer (not bool), or identity string.
source_revision is explicitly present: null or revision. Binding checks require
equal values AND exact types.

Responses contain contract_version, operation_name, operation_id, status,
result_class, result_digest; data/error as applicable. Material responses use
"1.1" and "PUBLIC_NON_AUTHORITY". PublicSurface errors use error={"code":status}.
Host startup failure before dispatch uses "1.0", invalid operation_name/operation_id,
status REJECTED, error={"code":"INVALID_HOST_INPUT"}. CLI exits 0 for
OK/NO_MATCH/DISABLED/PENDING/PARTIAL/COMPLETE, 2 for other statuses. Adapter startup
errors may exit without JSON. Read SKILL.md for Windows/WSL invocation.

## EVALUATE exact request

payload has exactly action, trigger, task_run_id, semantic_revision,
target_operation, request_key, source_id, source_revision, host_facts, evidence_refs.
action="EVALUATE"; trigger="A" or "B"; target_operation is only
knowledge.candidate.submit or recall.admit. task_run_id/request_key/source_id
are identities; semantic_revision is revision.

A host_facts has exactly strict bool fields:
semantic_object_required, legal_ingress_or_producer_absent.
A evidence_refs has exactly requirement, material_availability.

B host_facts has exactly strict bool fields:
legal_light_task_bypass, meaningful_completion_evidence, within_existing_scope,
materially_reusable, suitable_legal_material_absent.
B evidence_refs has exactly admission, completion, scope, reusable_value,
material_availability.

Each evidence_refs value is a list of 1–16 opaque identities. Complete exact keys;
null/string/number cannot substitute for bool. All chosen trigger facts must be
true to request material. A/B are independent; LIGHT_TASK_BYPASS alone is
insufficient. Host owns semantic judgments, real admission, reusable value,
completion, scope and availability. Skill validates explicit structure/facts,
not semantic truth or reference authenticity.

## Identity and EVALUATE response

evaluation_digest=H(EVALUATE payload).
request_id="material-"+H([owner_namespace,request_key,task_run_id,semantic_revision,
target_operation,source_id,source_revision]).
settlement_operation_id="material-settle-"+H([owner_namespace,request_id]).

Evaluate operation_id, trigger, transport and unknown future material digest
are absent from logical identity, but original/outer envelope digests still bind
their exact content. Changing original evaluation identity/trigger can change
SETTLE outer digest and conflict with a committed receipt.

Evaluation binding has exactly request_id, settlement_operation_id,
evaluation_digest, owner_namespace, request_key, task_run_id, semantic_revision,
source_id, source_revision, target_operation.

Before true OR false result check registered owner/run/current accepted revision,
open/nontransition lifecycle, exact registered source lineage, current deletion
barrier; Recall target also requires recall_enabled.

Legal False: status OK, data exactly {"requested":false}.
All True: status PENDING; data is the evaluation binding plus requested=true and
allowed_material_operation=target_operation.
This is a returned request only, no historical pending, business receipt or
material persistence. Existing domain initialization/journal recovery may occur.
SETTLE may contain a legal original EVALUATE snapshot never actually sent; there
is no persisted send proof. Later-produced material does not refute the original
suitable_legal_material_absent Host snapshot.

## SETTLE exact request and legal nested material

payload has exactly action, original_evaluation, request_id, evaluation_digest,
material_operation; action="SETTLE".
original_evaluation is the exact legal 1.1 EVALUATE envelope with all facts true.
Recompute original digest, evaluation_digest and deterministic identities.
Outer owner equals original owner; outer operation_id and nested operation_id
both equal settlement_operation_id; payload request_id/evaluation_digest match.

material_operation is a legal 1.0 envelope targeting the original target_operation,
matching owner and settlement ID. Independently validate nested request_digest.
source_id/source_revision must explicitly match original values AND types.

Knowledge payload requires knowledge_body (nonblank human-language string <=32768),
claim_scope (identity), classification_path (three opaque identities), plus explicit
source_id/source_revision for SETTLE. Optional provenance_refs: <=100 identities.
Knowledge material forbids task_run_id, semantic_revision, task_semantic_revision:
task binding belongs in the outer receipt. raw_reasoning, chain_of_thought,
reasoning, event_kind, capsule_body are rejected. Original legal 1.0 rules remain.

Recall payload requires task_run_id, semantic_revision, source_id, source_revision,
items. Task fields match binding by value and type; SETTLE requires 1–100 items.
Each item has exactly semantic_body (nonblank string <=8192), scope, and optional
provenance_refs (<=16 identities). Scope is "GLOBAL" or
"PROJECT:<explicit-project-identity>", respecting current-project boundaries.
Extra item fields/raw reasoning fail closed. The nonempty constraint here is
SETTLE-specific; ordinary 1.0 recall.admit keeps its existing legal rules.

## Success response and Atomic Receipt

Status OK; data has exactly request_id, settled=true, target_operation, binding,
adoption_result. binding is the evaluation binding plus material_digest (nested
request_digest) and outer_request_digest (SETTLE request_digest): 12 exact keys.

Knowledge adoption_result has exactly knowledge_id, content_revision,
knowledge_body_digest, status, validation_epoch, pass_streak, fail_streak,
conflict_lock, record_revision, authority.
knowledge_id="knowledge-"+H([owner_namespace,settlement_operation_id])[:32].
content_revision=1; status="CANDIDATE"; validation_epoch=1; pass_streak=0;
fail_streak=0; conflict_lock=false; record_revision=1;
authority="SUPPORT_ONLY_NON_AUTHORITY"; knowledge_body_digest=H(knowledge_body).

Recall adoption_result has exactly items. Each item has exactly working_item_id,
content_digest. working_item_id="w-"+H([owner_namespace,settlement_operation_id,
task_run_id,semantic_revision,item_index]); content_digest=H({"semantic_body":body,
"scope":scope,"provenance_refs":refs}), with refs default [].

Knowledge Store and Recall history each own their respective transaction.
Each commits adoption plus outer receipt in the SAME after snapshot and one
existing transact stage/install. No cross-store transaction, Request Store,
second Core or second transaction framework. Receipt stores binding and non-body
adoption facts, not original envelopes/evidence/material body copies.
Receipt proves mechanical adoption only. Knowledge remains Candidate, no PASS/
Trust; Recall remains WORKING and unretrievable until explicit legal publish.

Knowledge final current() checks EventLifecycle current accepted task revision
inside owning protected_gate held through stage/install under root ownership.
Recall uses existing admission guard/gate and final current/revision checks.
Both require current owner/run/revision, exact lineage, open lifecycle and deletion
barrier; Recall also requires enabled state.

## Exact retry, recovery and deletion boundary

Exact SETTLE retry checks current lifecycle/lineage/barrier/enabled BEFORE replay,
then returns saved receipt without new adoption. Replay is not unconditional:
successor/closed/transition/noncurrent tasks cannot settle/retry as current.
Different committed outer digest is CONFLICT. A wrong deterministic SETTLE ID is
REJECTED by binding validation; already-used IDs can first hit global CONFLICT.
Original cross-domain operation identity conflicts remain.

Valid durable stage is existing finish-same decision; recovery completes it,
not a new SETTLE. Lifecycle successor/terminal restores staged owning journals
under same root/gate first. Deletion remains barrier-first with existing discard,
cleanup and recovery validators; material bodies cannot resurrect.
Knowledge receipt cleanup and deterministic identity/tombstone block reconstruction;
Recall cleanup retains erased acknowledgement without rebuilding Working.

Recovery is existing trusted Host internal PublicSurface.recover_existing, not a
public JSON operation/background worker/Host retry planner. Windows root LockFileEx
protects compliant writers and active owners; arbitrary writers bypassing this
protocol are outside that guarantee.

## Rejections and Authority

MALFORMED: missing/extra exact fields, illegal shapes/types/action.
UNSUPPORTED_VERSION: operation/version matrix violation.
REJECTED: digest mismatch, false original facts, wrong owner/source/target or
deterministic binding; current deletion barrier.
STALE: unknown/noncurrent accepted task revision, closed or transition lifecycle.
CONFLICT: committed/global identity with differing digest, or active root owner.
DISABLED: Recall disabled.
Error precedence follows actual validation/global guards, not an invented fixed
priority for requests that violate multiple constraints.

Host remains semantic Authority/workflow owner. Opaque references/digests do not
prove truth, Host identity or historical sending. Recall/Knowledge/receipt never
grant current execution Authority. Trust validation and publish remain explicit.
No polling/watcher/observer, Drudge-generated lineage, backfill/interception or
scope expansion. One Skill, one Core, intended unchanged B0002/R0001 topology.
