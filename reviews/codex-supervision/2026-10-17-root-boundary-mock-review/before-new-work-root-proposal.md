# 新工作根与统一边界方案(设计稿 v1)

状态:DESIGN(方案先行;不本轮改造 BOUND_FILES、不补采、不创建证书)。
依据:Codex 870/871 口径——补采前先交 collector/transport/verifier 同版本统一边界、
旧证据兼容与拒绝夹具;"不能只改 --work 或放宽 bound_path"。

## 1. 现状(已核)

- 三个硬编码根:`sandbox_execution.WORK_ROOT` 与 `full_surface_evidence.WORK_ROOT`
  = reviews/codex-supervision/2026-10-05-three-gates;`full_surface_evidence.REVIEW_ROOT`
  与 `sandbox_surface_acceptance.HERE` = reviews/codex-supervision/2026-10-06-all43-sandbox-repair;
  `production_isolation_acceptance.OUT` = three-gates。
- 既有 `bound_path()` 提供"根包含"校验,但根是常量;新增根只能改代码 → 改 BOUND_FILES。
- 当前 43 点重算:30 GREEN / 2 PARTIAL(F2,F4)/ 11 GAP(Codex 870);旧 joint-v2 有 9 项
  绑定差异不能继承;证书不存在。

## 2. 方案:版本化根注册表 + cohort 统一边界

### 2.1 根注册表

新文件 `reviews/exec-native/ROOTS.v1.json`(独立新根区,不与任何旧根重叠):

```json
{
  "schema": "exec-native-roots-v1",
  "entries": [
    {
      "root_id": "n<run-seq>",
      "root_path": "reviews/exec-native/run-<root_id>",
      "purpose": "transport|surface|joint|external",
      "cohort": {
        "collector_sha256": null,
        "verifier_sha256": null,
        "bound_files_sha256_map": null
      },
      "bound_paths": ["raw", "work", "media"],
      "status": "REGISTERED|ACTIVE|FROZEN",
      "created_at": null
    }
  ]
}
```

约束:
- root_path 必须位于 reviews/exec-native/ 下且不与三个旧根及任何既有目录重叠;
- root_id 唯一且不可复用;历史 entry 不可删改(只允许 status 流转 REGISTERED→ACTIVE→FROZEN);
- bound_paths 为闭合白名单(相对 root_path 的一层子目录),禁止空列表、禁止 ".." 或绝对路径、禁止根级通配。

### 2.2 cohort(同版本统一边界)

- 一次补采 = 一个 cohort:绑定当时 **BOUND_FILES 全集 SHA 映射** + collector/verifier 脚本 SHA;
- 运行期间任一绑定文件变化 → cohort 作废,后续回执全部拒绝;
- 运行写入只允许落在该 cohort 的 bound_paths 内(沿用 bound_path 根包含语义,不放宽);
- cohort 冻结后不可改绑定、不可复用其产物作新轮实测。

### 2.3 工具改造点(方案批准后实施)

把上述三个硬编码常量改为"按当前 cohort 解析注册表":
- `sandbox_execution.WORK_ROOT` / `full_surface_evidence.WORK_ROOT、REVIEW_ROOT`
- `production_isolation_acceptance.OUT` / `sandbox_surface_acceptance.HERE`
- 改造必然改变 BOUND_FILES 的 SHA → 旧证据按 named-window 只读继承,不重签;
  改造版本需 Codex 复核后方可用于新 cohort。

### 2.4 旧证据兼容规则

- 旧冻结回执只读;引用必须带 (path, sha256) 且路径落在旧根内;
- 旧 run 的 implementation_before/after 与旧 BOUND_FILES 绑定原样保留;
- 新 cohort 不得引用旧 run 产物冒充"本轮实测";LAN D9 仅继承具名窗口;
- 证书候选的 raw_path / surface_raw_path 必须落在对应 cohort 新根内,否则拒绝。

## 3. 拒绝矩阵(mock 校验器已实现)

| 编号 | 场景 | 判定 |
|---|---|---|
| R1 | 根未在注册表登记 | REFUSE |
| R2 | 根路径与旧根/既有目录重叠 | REFUSE |
| R3 | cohort 绑定与当前 BOUND_FILES 映射不一致 | REFUSE |
| R4 | 写路径越出 bound_paths(../、绝对路径) | REFUSE |
| R5 | 旧回执(旧根路径)冒充本轮材料 | REFUSE |
| R6 | 同 cohort 重复运行/复用产物 | REFUSE |
| R7 | 注册表历史被回改(root_id 复用/删除历史) | REFUSE |
| R8 | 放宽 bound_path(空列表/通配/根级) | REFUSE |

夹具实现:exec-isolation/mock_root_boundary_checker.py,纯内存 mock(不建真实根、
不跑原生探针),每场景真实 assert,失败退出非零。mock 校验只证明拒绝规则逻辑,
不构成任何原生验收证据。

## 4. 实施顺序

1. 本方案经 Codex 审查定稿;
2. 工具改造(BOUND_FILES 变化,Codex 复核新绑定);
3. 新 cohort 注册 → 用户授权范围内由 claude-code 执行补采;
4. Codex 独立复算 → 按 §2.6 提证书候选(仍不自行创建证书)。

提交时间以 git 记录为准;本文件不含时间戳字段。
