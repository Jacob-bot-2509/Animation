"""Root policy and local metadata candidate v2. NOT native authorization."""
from __future__ import annotations
import copy, datetime as dt, hashlib, json, re, os, uuid
from pathlib import Path

SCHEMA = "exec-native-roots-v2"
PREFIX = "reviews/exec-native/"
HEX = re.compile(r"[0-9a-f]{64}")
ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
GUID = re.compile(r"[0-9a-f]{32}")
OLD_ROOTS = (
    "reviews/codex-supervision/2026-10-05-three-gates",
    "reviews/codex-supervision/2026-10-06-all43-sandbox-repair",
    "reviews/2026-10-06-exec-isolation-full-surface")
ENTRY_KEYS = {"root_id","root_path","purpose","cohort","bound_paths","status","created_at"}
COHORT_KEYS = {"collector_sha256","verifier_sha256","bound_files_sha256_map"}
TOOLS = {"collector_sha256","verifier_sha256"}

def sha_object(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()

def relative(value):
    if type(value) is not str or not value or len(value)>1024:
        raise ValueError("R_PATH:type_or_length")
    parts=value.split("/")
    reserved={"con","prn","aux","nul",*(f"com{i}" for i in range(1,10)),*(f"lpt{i}" for i in range(1,10))}
    if any(not p or p in (".","..") or p.endswith(("."," ")) or not re.fullmatch(r"[A-Za-z0-9_.-]+",p)
           or p.split(".")[0].casefold() in reserved for p in parts):
        raise ValueError("R_PATH:noncanonical_windows_relative")
    return value

def overlaps(a,b):
    a,b=a.casefold(),b.casefold()
    return a==b or a.startswith(b+"/") or b.startswith(a+"/")

def hash_map(value):
    if type(value) is not dict or not value:
        raise ValueError("R3:empty_or_invalid_binding_map")
    names=set()
    for path,sha in value.items():
        normalized=relative(path).casefold()
        if normalized in names or type(sha) is not str or not HEX.fullmatch(sha):
            raise ValueError("R3:binding_path_or_hash")
        names.add(normalized)

def entry(value):
    if type(value) is not dict or set(value)!=ENTRY_KEYS:
        raise ValueError("R_SCHEMA:entry")
    rid=value["root_id"]
    if type(rid) is not str or not ID.fullmatch(rid):
        raise ValueError("R7:root_id")
    path=relative(value["root_path"])
    if path!=PREFIX+"run-"+rid or any(overlaps(path,old) for old in OLD_ROOTS):
        raise ValueError("R2:root_location")
    if value["purpose"] not in ("transport","surface","joint","external"):
        raise ValueError("R_SCHEMA:purpose")
    bp=value["bound_paths"]
    if type(bp) is not list or not bp or any(type(p) is not str for p in bp):
        raise ValueError("R8:bound_paths_type_or_empty")
    if len(bp)!=len(set(bp)) or not set(bp)<={"raw","work","media"}:
        raise ValueError("R8:bound_paths_not_closed")
    if value["status"] not in ("REGISTERED","ACTIVE","FROZEN"):
        raise ValueError("R7:status")
    stamp=value["created_at"]
    if type(stamp) is not str or dt.datetime.fromisoformat(stamp).utcoffset() is None:
        raise ValueError("R_SCHEMA:created_at")
    cohort=value["cohort"]
    if type(cohort) is not dict or set(cohort)!=COHORT_KEYS:
        raise ValueError("R3:cohort_schema")
    for key in TOOLS:
        if type(cohort[key]) is not str or not HEX.fullmatch(cohort[key]):
            raise ValueError("R3:tool_hash")
    hash_map(cohort["bound_files_sha256_map"])

def snapshot(reg, allow_empty=False):
    if type(reg) is not dict or set(reg)!={"schema","entries","previous_registry_sha256"} or reg["schema"]!=SCHEMA:
        raise ValueError("R_SCHEMA:registry")
    previous=reg["previous_registry_sha256"]
    if previous is not None and (type(previous) is not str or not HEX.fullmatch(previous)):
        raise ValueError("R7:previous_hash")
    rows=reg["entries"]
    if type(rows) is not list or (not rows and not allow_empty):
        raise ValueError("R1:empty_or_invalid_entries")
    ids=set();paths=[]
    for row in rows:
        entry(row)
        if row["root_id"] in ids or any(overlaps(row["root_path"],p) for p in paths):
            raise ValueError("R2_R7:duplicate_or_nested_root")
        ids.add(row["root_id"]);paths.append(row["root_path"])

def check_registry(reg,current_bound_map,*,current_tool_hashes=None,history=None,
                   existing_paths=(),reparse_paths=()):
    """Only validates supplied model facts. Caller must supply independently trusted context."""
    try:
        snapshot(reg);hash_map(current_bound_map)
        if type(current_tool_hashes) is not dict or set(current_tool_hashes)!=TOOLS:
            raise ValueError("R3:trusted_tool_pins_missing")
        if any(type(v) is not str or not HEX.fullmatch(v) for v in current_tool_hashes.values()):
            raise ValueError("R3:trusted_tool_pins_invalid")
        if history is None:
            raise ValueError("R7:trusted_history_missing")
        history_doc=history_check(reg,history)
        if reg["previous_registry_sha256"]!=hashlib.sha256(history).hexdigest():
            raise ValueError("R7:history_hash")
        old={e["root_id"]:e for e in history_doc["entries"]}
        new={e["root_id"]:e for e in reg["entries"]}
        if not old.keys()<=new.keys():
            raise ValueError("R7:history_deleted")
        if not isinstance(existing_paths,(list,tuple,set)) or not isinstance(reparse_paths,(list,tuple,set)):
            raise ValueError("invalid_filesystem_facts")
        existing=[relative(p) for p in existing_paths]
        reparses=[relative(p) for p in reparse_paths]
        transitions={("REGISTERED","REGISTERED"),("REGISTERED","ACTIVE"),("ACTIVE","ACTIVE"),
                     ("ACTIVE","FROZEN"),("FROZEN","FROZEN")}
        for rid,e in new.items():
            path=e["root_path"]
            if rid in old:
                if any(e[k]!=old[rid][k] for k in ENTRY_KEYS-{"status"}):
                    raise ValueError("R7:historical_fields_changed")
                if (old[rid]["status"],e["status"]) not in transitions:
                    raise ValueError("R7:status_transition")
            else:
                if e["status"]!="REGISTERED":
                    raise ValueError("R7:new_root_must_be_registered")
                # Existing containers are permitted; a new target itself or its descendants are not.
                if any(p.casefold()==path or p.casefold().startswith(path+"/") for p in existing):
                    raise ValueError("R2:existing_target_or_descendant")
            if any(path.casefold()==p.casefold() or path.casefold().startswith(p.casefold()+"/") for p in reparses):
                raise ValueError("R_PATH:reparse_ancestor")
            # Frozen historical cohorts keep their exact old hashes, never re-sign them as current.
            if e["status"]!="FROZEN":
                c=e["cohort"]
                if c["bound_files_sha256_map"]!=current_bound_map or any(c[k]!=current_tool_hashes[k] for k in TOOLS):
                    raise ValueError("R3:current_cohort_mismatch")
        return []
    except (ValueError,TypeError,KeyError,AttributeError,UnicodeError,RecursionError) as exc:
        return [str(exc) or "R_BAD_INPUT"]

def selected(reg,root_id,current_bound_map,context):
    if check_registry(reg,current_bound_map,**context):
        return None
    return next((e for e in reg["entries"] if e["root_id"]==root_id and e["status"]=="ACTIVE"),None)

def _model_write(reg,root_id,write_rel,*,current_bound_map,writer="parent",**context):
    e=selected(reg,root_id,current_bound_map,context)
    if e is None or writer not in ("parent","child"):
        return False
    try:
        parts=relative(write_rel).split("/")
        if len(parts)<2 or parts[0] not in e["bound_paths"] or writer=="child" and parts[0]=="raw":
            return False
        full=e["root_path"]+"/"+write_rel
        return not any(full.casefold()==relative(p).casefold() or full.casefold().startswith(relative(p).casefold()+"/")
                       for p in context.get("reparse_paths",()))
    except (ValueError,TypeError):
        return False

# These APIs intentionally require a complete registry plus independent context.
def is_hex64(value):
    return type(value) is str and HEX.fullmatch(value) is not None

def valid_root_id(value):
    return type(value) is str and ID.fullmatch(value) is not None

def root_path_of(root_id):
    if not valid_root_id(root_id):
        raise ValueError("invalid_root_id")
    return PREFIX + "run-" + root_id

def literal_relpath_issues(value):
    try:
        relative(value)
        return []
    except (ValueError, TypeError):
        return ["noncanonical_windows_relative"]

def strict_loads(raw):
    if type(raw) is not bytes or len(raw) > 4 * 1024 * 1024:
        raise ValueError("history_bytes_or_size")
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate_json_key")
            out[key] = value
        return out
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)

def history_check(reg, previous):
    snapshot(reg)
    old_doc = strict_loads(previous)
    snapshot(old_doc, True)
    if reg["previous_registry_sha256"] != hashlib.sha256(previous).hexdigest():
        raise ValueError("previous_exact_bytes_sha_mismatch")
    old = {e["root_id"]: e for e in old_doc["entries"]}
    new = {e["root_id"]: e for e in reg["entries"]}
    if not old.keys() <= new.keys():
        raise ValueError("history_deleted")
    allowed = {("REGISTERED","REGISTERED"),("REGISTERED","ACTIVE"),
               ("ACTIVE","ACTIVE"),("ACTIVE","FROZEN"),("FROZEN","FROZEN")}
    for rid, row in new.items():
        if rid not in old:
            if row["status"] != "REGISTERED":
                raise ValueError("new_root_must_start_REGISTERED")
        elif any(row[k] != old[rid][k] for k in ENTRY_KEYS - {"status"}):
            raise ValueError("immutable_history_changed")
        elif (old[rid]["status"],row["status"]) not in allowed:
            raise ValueError("illegal_status_transition")
    return old_doc

class HistoryChain:
    """One-step exact-byte chain. Caller must retain an independent trusted tip.
    Does not establish multi-step custody, registry persistence or ACLs."""
    def __init__(self, previous_snapshot_bytes):
        self.prev_bytes = previous_snapshot_bytes
        self.prev_sha = (hashlib.sha256(previous_snapshot_bytes).hexdigest()
                         if type(previous_snapshot_bytes) is bytes else None)

    def verify_against(self, registry_doc):
        try:
            history_check(registry_doc, self.prev_bytes)
            return True, ""
        except (ValueError, TypeError, KeyError, AttributeError, UnicodeError) as exc:
            return False, str(exc) or "invalid_history"

    def next_registry(self, entries):
        doc = {"schema": SCHEMA, "entries": copy.deepcopy(entries),
               "previous_registry_sha256": self.prev_sha}
        ok, reason = self.verify_against(doc)
        if not ok:
            raise ValueError(reason)
        return doc

def check_registry_entries(registry_doc, current_bound_map, *, current_tool_hashes=None,
                           previous_snapshot_bytes=None, existing_paths=(), reparse_paths=()):
    issues = check_registry(registry_doc, current_bound_map,
        current_tool_hashes=current_tool_hashes, history=previous_snapshot_bytes,
        existing_paths=existing_paths, reparse_paths=reparse_paths)
    return not issues, issues

def check_receipt_root(reg, root_id, expected_run_id, cohort_digest, *, receipt=None,
                       current_bound_map=None, **context):
    try:
        e = selected(reg,root_id,current_bound_map,context)
        if e is None or not is_hex64(cohort_digest) or cohort_digest != sha_object(e["cohort"]):
            return False, "receipt_context_or_cohort"
        expected = {"root_id":root_id,"root_path":e["root_path"],"run_id":expected_run_id,
                    "cohort_sha256":cohort_digest}
        ok = (type(expected_run_id) is str and GUID.fullmatch(expected_run_id) is not None
              and type(receipt) is dict and receipt == expected)
        return bool(ok), "" if ok else "actual_receipt_identity_mismatch"
    except (ValueError, TypeError, KeyError, AttributeError):
        return False, "invalid_receipt"

PROJECT = Path(r"D:\Animation-Model-Training")

def guarded_path(value):
    """Best-effort lstat checks, NOT a handle-based TOCTOU security boundary."""
    text = os.fspath(value)
    if type(text) is not str or not text or not Path(text).is_absolute():
        raise ValueError("absolute_project_path_required")
    # Check raw spelling before Path can discard dot segments.
    if any(x in (".","..") for x in text.replace("\\","/").split("/")):
        raise ValueError("dot_segment")
    p = Path(text)
    try:
        relative(p.relative_to(PROJECT).as_posix())
    except ValueError:
        raise ValueError("outside_project_or_noncanonical")
    for q in (p,*p.parents):
        if q.exists() or q.is_symlink():
            st = q.lstat()
            if q.is_symlink() or getattr(st,"st_file_attributes",0) & 0x400:
                raise ValueError("reparse_path")
            if q.is_file() and st.st_nlink > 1:
                raise ValueError("hardlinked_file")
            if q.is_dir() and (q/"delivery-manifest.json").exists():
                raise ValueError("frozen_directory")
        if q == PROJECT:
            break
    return p

def write_new_json(path, data):
    p = guarded_path(path)
    with p.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(data,f,sort_keys=True,separators=(",",":"),ensure_ascii=True)
        f.flush()
        os.fsync(f.fileno())

class JobReservation:
    """Local metadata candidate only; never creates or authorizes native work roots.
    Existing unfrozen project base is required. Atomic mkdir reserves (cohort,job).
    Uncertain/crashed placeholders and locks stay reserved; no automatic retry.
    No power-loss directory durability, malicious-peer ACL or TOCTOU claim."""
    def __init__(self, base):
        self.base = guarded_path(base)
        if not self.base.is_dir():
            raise ValueError("existing_metadata_base_required")

    def _place(self,cohort_id,job_id):
        if not is_hex64(cohort_id) or type(job_id) is not str or not GUID.fullmatch(job_id):
            raise ValueError("cohort_sha_and_job_uuid_required")
        return guarded_path(self.base/("cohort-"+cohort_id)/("job-"+job_id))

    def reserve(self,cohort_id,job_id):
        place = None
        try:
            place = self._place(cohort_id,job_id)
            parent = guarded_path(place.parent)
            parent.mkdir(exist_ok=True)  # No parents=True; base must already exist.
            guarded_path(parent)
            place.mkdir()               # Sole cross-process reservation linearization point.
            write_new_json(place/"intent.json",self._intent(cohort_id,job_id,"RESERVED"))
            return True, ""
        except (ValueError, OSError, TypeError) as exc:
            # Even an incomplete directory is retained. Never erase and retry.
            return False, "reserved_or_uncertain:"+str(exc)

    @staticmethod
    def _intent(cohort_id,job_id,state):
        return {"schema":"root-job-intent-v2","cohort_id":cohort_id,"job_id":job_id,
                "state":state}

    def inspect(self,cohort_id,job_id):
        try:
            place = self._place(cohort_id,job_id)
            if not place.exists():
                return "ABSENT"
            if not place.is_dir() or (place/".busy").exists():
                return "UNCERTAIN"
            f = guarded_path(place/"intent.json")
            data = strict_loads(f.read_bytes())
            state = data.get("state") if type(data) is dict else None
            if state not in ("RESERVED","FINALIZED") or data != self._intent(cohort_id,job_id,state):
                return "UNCERTAIN"
            if set(p.name for p in place.iterdir()) != {"intent.json"}:
                return "UNCERTAIN"
            return state
        except (ValueError, OSError, TypeError, UnicodeError):
            return "UNCERTAIN"

    def finalize(self,cohort_id,job_id):
        # Serialized with exclusive-create persistent lock. Crash leaves .busy;
        # an operator must investigate, never erase uncertainty automatically.
        lock = None
        try:
            place = self._place(cohort_id,job_id)
            if self.inspect(cohort_id,job_id) != "RESERVED":
                return False,"not_RESERVED_or_uncertain"
            lock = guarded_path(place/".busy")
            with lock.open("x",encoding="ascii") as f:
                f.write("LOCAL_METADATA_TRANSITION_ONLY")
                f.flush();os.fsync(f.fileno())
            f = guarded_path(place/"intent.json")
            data = strict_loads(f.read_bytes())
            if data == self._intent(cohort_id,job_id,"FINALIZED") and set(p.name for p in place.iterdir()) == {"intent.json",".busy"}:
                guarded_path(lock).unlink()
                return False,"already_FINALIZED"
            if data != self._intent(cohort_id,job_id,"RESERVED"):
                raise ValueError("not_exact_RESERVED_intent")
            if set(p.name for p in place.iterdir()) != {"intent.json",".busy"}:
                raise ValueError("unexpected_job_files")
            tmp = guarded_path(place/(".intent-"+uuid.uuid4().hex+".tmp"))
            write_new_json(tmp,self._intent(cohort_id,job_id,"FINALIZED"))
            guarded_path(f);os.replace(tmp,f)
            guarded_path(lock).unlink()
            return True, ""
        except (ValueError, OSError, TypeError, UnicodeError) as exc:
            return False, "transition_rejected_or_uncertain:"+str(exc)

def check_write(reg, root_id, write_rel, cohort_digest=None, *, current_bound_map=None,
                writer="parent", **context):
    try:
        e=selected(reg,root_id,current_bound_map,context)
        if e is None or not is_hex64(cohort_digest) or cohort_digest != sha_object(e["cohort"]):
            return False,"full_cohort_required"
        ok=_model_write(reg,root_id,write_rel,current_bound_map=current_bound_map,
                        writer=writer,**context)
        return bool(ok),"" if ok else "write_policy_denied"
    except (ValueError,TypeError,KeyError,AttributeError):
        return False,"invalid_write_context"
