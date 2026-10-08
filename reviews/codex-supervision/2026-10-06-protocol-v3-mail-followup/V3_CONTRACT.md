# V3 local proposal contract

Status: implemented validator, pending live independent acceptance. All paths and review evidence must resolve within the project. Run the CLI from the project root. No active-data publisher is provided here.

## Density ledger

Use schema `linalg048-train-variant-density-v1`. A completed input requires status `INDEPENDENT_VERIFIED`, reviewer, review_evidence, manifest_sha256 and policy_sha256.

Each review_evidence is {"path": "project/relative/review-file", "raw_sha256": "64 lowercase hex characters"}. It must name a nonempty real review artifact; the validator verifies its bytes. The artifact must actually identify and justify the subjects claimed as reviewed. A hash alone does not prove independent reasoning.

record_reviews must cover every active train ID exactly once, with canonical full record SHA computed by holdout_contract.object_sha, independent_math_verified=true, independent_core_verified=true, core_family_id and review_evidence. The current pending template covers47 records. The producer must also preserve manifest and all4 training source raw hashes; these are checked by the publisher and included in its source bindings.

families must be nonempty. Each family needs:
- id; unique member_ids covering the full training pool; concept_id from the bound policy; variant_kind.
- core_signature with nonempty object, conditions, goal, solution_structure; normalize variable names and numeric substitutions according to mathematical equivalence, and justify any distinct task.
- reason and review_evidence containing full-task mathematical comparison, concept and form attribution.

Every member has exactly one primary family and agrees with record_reviews. Each family contributes exactly one independent task and one form to its primary concept. Exact identical signatures cannot be assigned separate families; differently worded equivalent signatures still require semantic review.

Optional claimed_concept_counts and concept_coverage_complete must agree with computed results. If independent_tasks exceeds target_max_per_concept, density_notes[concept_id] needs reviewer, reason and review_evidence. The target remains soft; such a note does not certify training.

## Manual acceptance

Use schema `linalg048-manual-acceptance-v3`. A completed input requires independent_semantic_review_status=`COMPLETE`, reviewer, review_evidence, and exact raw SHA bindings for render_evidence, candidate, scene, media, density; labeling_rule_sha256 must equal holdout_contract.RULE_SHA.

visual needs verdict=`ACCEPT`, a genuine visual reason and review_evidence. semantic_pairs must cover every unique (split,id,problem_sha256) from the genuine render receipt exactly once; the current pending template contains296 identities.

Every pair needs verdict, reason and review_evidence.
- DIFFERENT_CORE_TASK: substantive difference across the whole object/conditions/goal/solution structure; shared facts do not alone imply leakage.
- SAME_CORE_TRAIN_VARIANT: train only, peer and candidate share the ledger's core_family_id; label also needs matching core_family_id and a nonempty equivalence_mapping explaining axes/symbols/numeric transformation and invariant task structure.
- SAME_CORE_CROSS_SPLIT, UNCERTAIN, blank, incomplete and unknown labels cannot pass.

Workflow-v2, v2 manual files, auto-renamed schemas and pending templates are not substitutes for actual independent acceptance. New review files must keep prior raw artifacts intact.

## Fresh inactive publication

Use tools/apply_linalg048_admission_v3.py with --out NEW_PATH --render-evidence ORIGINAL_BOUND_RECEIPT --acceptance NEW_COMPLETED_V3 --density NEW_REVIEWED_LEDGER.

The old render verifier runs on a fresh snapshot with its exact original binding set. Those verified bytes are merged and rechecked with the admission inputs. The result records original_render_source_bindings separately from current_admission_source_bindings.

Output is a local INACTIVE proposal. training_admitted, active_data_modified, global_leakage_free_certified, calibration_eligible and formal_training_readiness_certified are all false. Full concept coverage can still be false without misrepresenting a completed local ledger. No current selector, manifest, lock or asset index changes.

The density and semantic validators verify source-bound attestations, not the truth of mathematical claims. Completion status is not permission for formal promotion, training, native rendering or production release. Those require the existing independent gates and versioned publication process.
