---
description: Phân tích website đối thủ và lập kế hoạch vượt đối thủ
argument-hint: "<link sản phẩm hoặc trang chủ đối thủ>"
---
Competitor URL: $ARGUMENTS (if empty, take it from `brand/brand-brief.md`; if none, ask).

1. Delegate to the **competitor-analyst** subagent with the URL and the brief path. It captures the site,
   reads the screenshots, writes `teardown/<host>/teardown.md` and drafts `teardown/plan.md`.
2. Read the plan yourself and check it follows the hard rules in CLAUDE.md (no copied assets, no
   unprovable claims, bundle discounts real).
3. Present to the student in Vietnamese, short:
   - Đối thủ đang làm tốt gì (5 ý) → mình giữ lại cấu trúc nào
   - Họ yếu ở đâu (5 ý) → 10 điểm mình sẽ làm tốt hơn (có số đo cụ thể)
   - Hướng khác biệt cho thương hiệu (màu, giọng văn, 1 section riêng)
   - Sơ đồ trang (trang chủ, trang sản phẩm, FAQ, About…)
4. ⛔ Ask for approval or changes. Record the decision in PROGRESS.md. Next: `/thuong-hieu`.
