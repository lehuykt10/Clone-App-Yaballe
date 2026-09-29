---
description: Sửa website theo yêu cầu (màu, chữ, giá combo, thời gian giao, thêm/bớt section…)
argument-hint: "<mô tả thay đổi bằng tiếng Việt>"
---
Change request: $ARGUMENTS

1. Classify: brand.json content/style change · new/changed section (Liquid) · store data (product, discount,
   page, menu) · policy text. Several may apply (e.g. delivery days → brand.json + FAQ + shipping policy:
   keep them consistent).
2. Theme changes → **theme-builder** subagent (edit brand.json, rebuild, theme check).
   Store data → connector (get-shop-info first) or a click-by-click guide.
3. Push to the staging/unpublished theme only (`/xem-truoc` flow). Never the live theme.
4. Tell the student in Vietnamese what changed, the preview link, and what to check. Update PROGRESS.md.
