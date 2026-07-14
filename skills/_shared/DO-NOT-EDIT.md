# 不要改这个目录

本目录由 `tools/sync_shared.py` 从仓库根的 `shared/` 生成。
改动请改 `shared/`，然后跑：

```bash
python3 tools/sync_shared.py sync --root .
```

CI 会检查两边是否一致，不一致直接 fail。
