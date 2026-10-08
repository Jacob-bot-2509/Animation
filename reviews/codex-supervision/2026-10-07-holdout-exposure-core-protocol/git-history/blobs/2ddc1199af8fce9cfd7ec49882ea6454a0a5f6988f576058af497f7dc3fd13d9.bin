# data/ — 数据目录规范

## 目录约定

```
data/
├── raw/       # 外部拉入原始数据(只读,登记来源/许可证后不再改)
├── train/     # 训练数据(JSONL,每行一条样本)
├── eval/      # 评测数据(独立锁定,与 train 零精确重叠)
├── test/      # 测试/预留(与 train 零精确重叠)
├── manifest.json  # 数据登记账本(由 tools/make_manifest.py 生成)
└── README.md
```

## manifest 规则(硬约束)

- 每个数据文件一条 entry:path/sha256/size/source/license/split/notes
- 许可证必须真实标注;白名单 apache-2.0 / mit / internal-generated / cc-by-sa-4.0;
  **未标注 → quarantine,禁入训练**
- 评测集/测试集与训练集**精确重叠零容忍**(样本按整行内容哈希比对,
  前项目 20/20 评测污染教训)
- SHA256 是登记时实测值;文件改动后必须重新生成 manifest

## 数据检查命令(dry-run)

```bash
python tools/data_check.py --dry-run                # 骨架自检
python tools/make_manifest.py --dir data --out data/manifest.json \
    --name animation-data-v1 --source <来源> --license <许可证>
python tools/data_check.py --manifest data/manifest.json   # 正式校验
python tools/data_check.py --scan data                     # 扫描临时校验
```

## 当前状态

尚无数据文件。数据就位前请先补 source/license 再入 train/eval。
