---
description: Bắt đầu dự án mới - kiểm tra máy, hỏi thông tin, tạo hồ sơ thương hiệu
argument-hint: "[link đối thủ] (tuỳ chọn)"
---
Start a new store project. Speak Vietnamese. Competitor link (optional): $ARGUMENTS

1. **Check the computer** (run each, report ✅/❌ in one table): `node -v` (≥ 20), `python --version` or `py --version` (≥ 3.10), `git --version`, `shopify version`, `npx playwright --version`.
   For any ❌, give the exact fix from HUONG-DAN (run `setup/setup-windows.ps1` on Windows or `bash setup/setup-mac.sh` on macOS) and continue with what works.
2. If this folder is not a git repo: `git init` (explain: để lưu lịch sử, sửa sai quay lại được).
3. Create `PROGRESS.md` if missing (sections: Store, Done, Next, Open questions, IDs).
4. Interview the student with the AskUserQuestion tool or short numbered questions, max 6 at a time, to fill
   `.claude/skills/shopify-competitor-clone/templates/brand-brief.md` → `brand/brand-brief.md`:
   competitor URL(s), brand name + domain, store `xxx.myshopify.com`, product(s) + price + supplier link,
   target market + currency, delivery times from the supplier, tax/duty situation, photos available.
   Suggest brand names only if asked; check the domain idea is free is the student's job.
5. Identify the niche and tell the student which playbook you'll use (`niche-playbooks`).
6. Update PROGRESS.md, then say the next command: `/phan-tich-doi-thu <link>`.
