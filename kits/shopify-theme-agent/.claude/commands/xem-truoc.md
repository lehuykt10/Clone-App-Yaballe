---
description: Đưa theme lên Shopify dưới dạng bản nháp (chưa xuất bản) và gửi link xem trước
argument-hint: "[tên-store.myshopify.com]"
---
Store: $ARGUMENTS (else from PROGRESS.md / brand-brief; else ask).

1. `shopify theme check --path theme` must be at baseline; fix first if not.
2. If PROGRESS.md already has a staging theme ID (unpublished): push to it
   `shopify theme push --path theme --theme <ID> --store <store>`.
   Otherwise `shopify theme push --path theme --unpublished --json --store <store>` and save the new ID.
   Never push to the live theme. If the only theme with our files is live, ask the student to click
   **Duplicate** in Online Store → Themes and push to the copy.
   First time: the CLI opens the browser to log in; tell the student to log in and come back.
3. If push fails (SSL "bad record mac", network, antivirus) run
   `python .claude/skills/shopify-theme-kit/scripts/zip_theme.py` and guide the upload:
   Online Store → Themes → Add theme → Upload zip file → chọn `dist/theme.zip`.
4. Give the preview link `https://<store>/?preview_theme_id=<ID>` and a 6-point check list for the
   student (xem trên điện thoại, bấm thử combo, đổi màu từng sản phẩm, thêm vào giỏ, xem thời gian giao,
   mở FAQ). ⛔ Only the student publishes (Online Store → Themes → … → Publish).
5. Update PROGRESS.md (theme ID, date).
