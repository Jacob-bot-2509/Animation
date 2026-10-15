# 当前修订的复验入口

从 D:/Animation-Model-Training 运行；以下命令仅核验并打印，不覆写旧回执：

    .venv/Scripts/python.exe -X utf8 -B tools/verify_codex_supervision.py
    .venv/Scripts/python.exe -X utf8 -B tools/verify_math_corrections_30.py
    .venv/Scripts/python.exe -X utf8 -B tools/verify_math_admission_v1.py --input reviews/codex-supervision/2026-10-07-core-verifier-followup/admission-v2

如需保存输出，使用 --out 指定一个项目 reviews 内尚不存在的新文件。重新构建必须使用 build_math_admission_v1.py --out 指定全新目录；已有 v1/v2 不重写。

当前通过仅证明具名30条正文与场景文本的版本/来源一致及相关格式，实际准入、新渲染、全761数学和核心范围语义隔离仍待完成。
