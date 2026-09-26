# 🎬 Video Studio — tool tạo video AI kiểu Topview (tự host)

Tool tạo video quảng cáo sản phẩm từ **ảnh sản phẩm + video mẫu viral**.

1. **Phân tích video mẫu:** tool tải video (link TikTok/Reels/Shorts hoặc file upload), cắt khung hình và nghe lời thoại bằng Whisper. Sau đó **Claude** phân tích hook, cấu trúc, phong cách của video và viết storyboard gồm prompt cho từng cảnh cùng lời voiceover tiếng Anh.
2. **Duyệt và sửa storyboard:** anh sửa prompt, thời lượng, lời đọc, hoặc chọn đoạn nào trong video mẫu cần "copy chuyển động".
3. **Tạo clip:** tool gửi prompt và ảnh sản phẩm làm tham chiếu (`@Image1…`) sang **Seedance reference-to-video** trên fal.ai. Các đoạn cần copy chuyển động được cắt từ video mẫu và gửi kèm (`@Video1…`).
4. **Ghép video:** tool thêm giọng đọc ElevenLabs, phụ đề và nhạc nền, rồi xuất file `final.mp4` tỉ lệ 9:16.

Nhiều cảnh được gộp vào **một lần gọi** model (tối đa 15 giây, dùng scene cut). Nhờ vậy sản phẩm và ánh sáng đồng nhất giữa các cảnh, và không bị tính phí thời lượng tối thiểu nhiều lần.

## Chi phí (ước tính, kiểm tra lại trên fal.ai)

| Model | 480p | 720p | Video 12s @720p |
|---|---|---|---|
| Seedance 2.0 Fast | ~$0.108/s | ~$0.242/s | ~$2.9 |
| Seedance 2.0 | ~$0.134/s | ~$0.302/s | ~$3.6 |
| Seedance 2.5 | ~$0.23/s | ~$0.52/s | ~$6.2 |

- Nếu có gửi video tham chiếu, fal nhân giá với **0.6**.
- Claude phân tích một video mẫu tốn khoảng vài cent.
- Giọng đọc 12 giây tốn khoảng $0.01.
- Giá được khai báo trong `app/video_models.py`. Khi fal đổi giá thì sửa `usd_per_1k_tokens` ở file này.

**Mẹo:** render nháp bằng *Seedance 2.0 Fast 480p* (~$1.3 cho 12 giây). Khi ưng prompt thì mới render bản 720p.

## Cài đặt

Cần **Python 3.10+** và **ffmpeg** (máy Mac: `brew install ffmpeg`; Ubuntu: `sudo apt install ffmpeg`; Windows: `winget install ffmpeg`).

```bash
cd video-studio
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # rồi điền FAL_KEY và ANTHROPIC_API_KEY
uvicorn app.main:app --port 8100
```

Sau đó mở http://localhost:8100

### API key cần có
- **FAL_KEY:** lấy tại https://fal.ai/dashboard/keys và nạp credit. Key này dùng chung cho Seedance, ElevenLabs TTS và Whisper.
- **ANTHROPIC_API_KEY:** lấy tại https://console.anthropic.com. Mặc định tool dùng model `claude-opus-5`, đổi được qua biến `CLAUDE_MODEL`. Nếu Claude từ chối yêu cầu, tool tự chuyển sang model dự phòng mà Anthropic khuyên dùng.

### Chạy thử không tốn tiền
Đặt `DEMO_MODE=1` trong `.env`. Chế độ này không gọi API nào: storyboard là mẫu cố định, clip là màn hình màu tạo bằng ffmpeg. Dùng để làm quen giao diện và kiểm tra ffmpeg đã cài đúng.

## Cấu trúc code

```
app/
  main.py          FastAPI: REST API + phục vụ giao diện
  pipeline.py      Điều phối: phân tích → storyboard → tạo clip → giọng đọc → ghép
  analyzer.py      Claude: prompt hệ thống "đạo diễn quảng cáo", xuất storyboard dạng JSON có cấu trúc
  generator.py     fal.ai: upload, Seedance reference-to-video, TTS, Whisper; gộp cảnh thành lần gọi
  media.py         ffmpeg: cắt khung hình, cắt clip tham chiếu, chuẩn hoá, ghép, phụ đề
  video_models.py  Danh sách model, giới hạn, bảng giá
  schemas.py       Storyboard / Project / Segment
static/            Giao diện (HTML + JS thuần, không cần build)
tests/             pytest (chạy ở DEMO_MODE, không tốn tiền)
data/projects/     Dữ liệu từng project (ảnh, clip, final.mp4) — không commit
```

Thêm model mới (Kling, Veo, Wan…): khai báo thêm một `VideoModel` trong `app/video_models.py`. Nếu tên tham số của model đó khác Seedance thì sửa thêm `generate_segment`.

## Chạy test

```bash
pytest -q
```

## Lưu ý
- Chỉ nên dùng video mẫu để học cấu trúc, nhịp và góc máy. Tool đã dặn Claude không copy người, logo hay thương hiệu trong video mẫu.
- Lời voiceover được viết để tránh cam kết y tế hoặc phóng đại, nhưng anh vẫn nên đọc lại trước khi đăng.
- Seedance 2.5 đang được giới hạn 15 giây mỗi lần gọi cho an toàn. Khi fal xác nhận hỗ trợ 30 giây thì tăng `max_duration` trong `app/video_models.py`.
