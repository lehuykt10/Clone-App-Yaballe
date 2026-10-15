# Chế độ B — Kênh YouTube ngách chia sẻ giá trị (video dài + Shorts)

Kênh giá trị sống nhờ **lòng tin và thời gian xem**, không nhờ một lần viral. Mỗi video phải giải quyết một câu hỏi cụ thể của một nhóm người cụ thể (vd: "mẹ bỉm lần đầu chọn máy hút sữa", "người mới làm dropshipping eBay tính phí"). Nội dung bán hàng chỉ là hệ quả: video hữu ích → người xem tin → bấm link/mua.

## Mục lục
1. Chính sách cần biết trước (kiếm tiền + AI)
2. Kịch bản: cấu trúc giữ chân
3. Dựng video dài 16:9
4. Cắt Shorts từ video dài
5. Tiêu đề, thumbnail, mô tả, chương
6. QA trước khi đăng

## 1. Chính sách cần biết trước
- **Nội dung không xác thực (inauthentic content)** — YouTube không cho kiếm tiền với nội dung sản xuất hàng loạt, lặp khuôn, ít giá trị thêm (vd slideshow ảnh stock + giọng AI đọc bài viết lại từ nguồn khác). Kênh AI vẫn được kiếm tiền nếu có **góc nhìn, kiến thức, trải nghiệm thật** của chủ kênh: số liệu tự đo, sai lầm tự mắc, so sánh tự làm, ví dụ cụ thể.
- **Tiết lộ nội dung chỉnh sửa/tổng hợp**: bật "Altered or synthetic content" khi upload nếu video có người/sự kiện/địa điểm trông như thật nhưng do AI tạo. Không bắt buộc với hoạt hình rõ ràng, chỉnh màu, phụ đề, hay AI chỉ hỗ trợ viết kịch bản.
- Clip, nhạc, hình của người khác: chỉ dùng khi có quyền (royalty-free, Thư viện âm thanh YouTube, hoặc tự quay). Clip NCC dùng được khi NCC cho phép — hỏi và lưu lại tin nhắn.
- Ngách sức khỏe / tài chính / trẻ em: không khẳng định y khoa, không cam kết lợi nhuận; dẫn nguồn trên màn hình. Nội dung cho trẻ em xem phải đánh dấu "Made for kids" (mất bình luận và một số tính năng).

## 2. Kịch bản: cấu trúc giữ chân (video 6–12 phút)
| Đoạn | Thời lượng | Việc cần làm |
|---|---|---|
| Hook | 0–15s | Nói thẳng kết quả/nỗi đau người xem nhận ra mình; **giữ lời hứa của tiêu đề + thumbnail** ngay câu đầu. Không chào hỏi, không "trước khi bắt đầu hãy subscribe" |
| Bối cảnh | 15–45s | Vì sao điều này quan trọng, ai nên xem, video sẽ đi qua gì (3 ý) |
| Thân | 3–4 khối | Mỗi khối: luận điểm → bằng chứng/ví dụ cụ thể → hành động người xem làm được. Cuối mỗi khối "mở vòng" sang khối sau ("nhưng điều thứ 3 mới là cái làm mình mất tiền…") |
| Tổng kết | 20–40s | 1 câu tóm mỗi ý + 1 việc làm ngay hôm nay |
| CTA | ≤ 15s | Gợi ý **một** video tiếp theo cụ thể (end screen) hoặc link sản phẩm/tài liệu. Đừng kết bằng "cảm ơn đã xem" kéo dài |

Viết kịch bản theo câu ngắn để đọc thành tiếng; đánh dấu `[B-ROLL: …]` cho hình minh họa ở từng câu và `[CHỮ: …]` cho chữ nhấn mạnh. Bảng `[B-ROLL]` này chính là danh sách cảnh cần tạo/quay → đưa sang `ai-video-director` nếu cần tạo bằng AI.

## 3. Dựng video dài 16:9
- Định dạng `16:9`, 1920×1080, 30fps. Voice (người thật hoặc AI) là xương sống: dựng hình theo voice.
- **Đổi hình mỗi 4–8 giây**: luân phiên A-roll (người nói / màn hình) ↔ B-roll ↔ chữ/sơ đồ. Cảnh nói liền > 8s → chèn `zoom: 1.1` ở nửa sau để tạo cảm giác cắt.
- Cắt bỏ khoảng lặng > 0.4s và câu nói vấp trong voice trước khi dựng (xem `ffmpeg-cookbook.md` → "Cắt khoảng lặng").
- Chữ nhấn mạnh (`texts`) cho số liệu và từ khóa quan trọng, `position: bottom` hoặc `center`, size 56–64.
- Phụ đề: dùng `make_captions.py --style youtube` cho bản đốt cứng **hoặc** (khuyến nghị cho video dài) tải file `.srt` lên YouTube làm phụ đề rời — tìm kiếm được và người xem tắt được.
- Nhạc nền rất nhỏ (0.06–0.10) và duck; đổi nhạc giữa các khối để báo hiệu chuyển ý.
- Video dài nhiều cảnh: chia EDL theo khối (`khoi1.json`, `khoi2.json`…), render từng khối, rồi nối bằng một EDL chứa các file khối đã render. Sửa một khối không phải render lại tất cả.

## 4. Cắt Shorts từ video dài (1 video dài → 3–5 Shorts)
- Chọn đoạn tự đứng được: một mẹo, một con số gây bất ngờ, một sai lầm. Mỗi Short 20–50s (YouTube Shorts cho tới 3 phút, nhưng ngắn giữ chân tốt hơn).
- Câu đầu của Short phải là hook, không bắt đầu giữa ý ("…và vì thế"). Có thể ghi thêm 1 câu voice mở đầu riêng.
- Khung 9:16: `--format 9:16` với `fit: blur` cho cảnh ngang, hoặc `fill` + `zoom` khi chủ thể ở giữa. Phụ đề `--style shorts`.
- Kết Short bằng gợi ý xem video dài (dùng tính năng "Related video" khi upload để liên kết).

## 5. Tiêu đề, thumbnail, mô tả, chương
- **Tiêu đề** ≤ 60 ký tự, có từ khóa người ta gõ tìm + lý do bấm (con số, kết quả, sai lầm). Viết 5 phương án, chọn 2 để A/B test bằng tính năng "Test & compare" của YouTube Studio.
- **Thumbnail** 1280×720: 1 chủ thể lớn, tương phản mạnh, ≤ 4–5 chữ **không lặp tiêu đề** (tiêu đề nói "cái gì", thumbnail nói "cảm xúc/kết quả"). Dùng `thumbnail.py sheet` để lấy khung ứng viên → `thumbnail.py make`. Làm 3 bản để test.
- **Mô tả**: 2 câu đầu nhắc lại lời hứa + từ khóa; link sản phẩm/tài liệu; nguồn tham khảo; dòng tiết lộ affiliate nếu có link hoa hồng.
- **Chương (chapters)**: dòng đầu `00:00`, ít nhất 3 chương, mỗi chương ≥ 10s. Lấy mốc từ thời điểm bắt đầu mỗi khối trong timeline (in ra từ tổng thời lượng các clip).

## 6. QA trước khi đăng
- [ ] 15s đầu giữ đúng lời hứa của tiêu đề/thumbnail
- [ ] Không đoạn nào > 8s hình đứng yên
- [ ] Mọi số liệu / khẳng định đều có nguồn hoặc là trải nghiệm thật đã ghi rõ
- [ ] Phụ đề đúng chính tả (tên riêng, thuật ngữ ngách)
- [ ] Âm lượng ≈ -14 LUFS, voice rõ hơn nhạc
- [ ] Đã bật "Altered or synthetic content" nếu có cảnh AI trông như thật
- [ ] Có ≥ 1 yếu tố chỉ kênh này có (số liệu tự đo, ví dụ thật, góc nhìn riêng) — điều kiện để không bị coi là nội dung không xác thực
