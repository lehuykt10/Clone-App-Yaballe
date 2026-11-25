# Ad Library Scout: tìm sản phẩm winning trên Meta Ad Library

**Bản web (không cần cài đặt):** https://claude.ai/artifact/AHFLBQNShF8NFA6QcqLwMa (mã nguồn: `web/ad-library-scout.html`). Bản web nhận JSON từ Graph API Explorer hoặc CSV nhập tay; bản dòng lệnh bên dưới dùng khi cần lấy hàng nghìn quảng cáo.

Tool dòng lệnh (Python 3.9+, không cần cài thêm thư viện) để:
1. Lấy các quảng cáo **đang chạy trong N ngày gần nhất** theo từ khóa, qua **Meta Ad Library API chính thức**.
2. Gom quảng cáo theo **nhà quảng cáo / domain store**.
3. Chấm **điểm winning 0–100** cho mỗi store.
4. **Ước tính** chi tiêu (tổng và theo ngày) và số đơn.
5. Xuất báo cáo `.md` (đọc nhanh) và `.csv` (mở bằng Excel/Google Sheets).

## ⚠️ Giới hạn cần hiểu trước

| Điều | Thực tế |
|---|---|
| Thị trường | Với quảng cáo thương mại, API **chỉ trả quảng cáo chạy ở EU** (theo luật DSA). Quảng cáo chỉ chạy ở Mỹ thì API không trả. |
| Chi tiêu | Meta **không công bố** chi tiêu và số hiển thị của quảng cáo thương mại. Tool **ước tính** từ reach EU, hoặc từ số ads × số ngày chạy. |
| Số đơn | Là **ước tính** = chi tiêu × ROAS giả định ÷ AOV. Chỉ dùng để **so sánh các store với nhau**, không phải doanh số thật. |
| Quảng cáo Mỹ | Tự sưu tầm trên website Ad Library rồi nhập file CSV (mục 4). **Không** dùng bot cào website Ad Library, vì vi phạm điều khoản của Meta. |

Mẹo: store nào đang scale mạnh ở EU thường cũng chạy ở Mỹ. Dùng EU làm "radar", rồi mở trang Ad Library của store đó để xem quảng cáo Mỹ.

## 1. Lấy access token (một lần)
1. Xác minh danh tính để truy cập Ad Library API: https://www.facebook.com/ID
2. Tạo tài khoản và app tại https://developers.facebook.com (loại app: Business).
3. Mở **Graph API Explorer**, chọn app, bấm **Generate Access Token**, rồi copy token.
   Token ngắn hạn sống khoảng 1–2 giờ. Đổi sang token dài hạn (60 ngày) bằng Access Token Debugger → *Extend*.
4. Đặt biến môi trường (không dán token vào code hoặc commit):
   ```bash
   export META_ACCESS_TOKEN="..."
   # tùy chọn: export META_GRAPH_VERSION="v23.0"
   ```

## 2. Chạy
```bash
# Tìm + phân tích luôn (6 nước EU mặc định, ads hiển thị trong 30 ngày qua)
python3 tools/ads_library_scout/scout.py run --terms "migraine cap" "headache hat" "ice head wrap" --aov 35

# Toàn EU, 14 ngày, lọc store có ≥ 5 ads đang chạy
python3 tools/ads_library_scout/scout.py run --terms "dog raincoat" --countries EU --days 14 --min-active 5

# Chỉ lấy dữ liệu thô, phân tích sau
python3 tools/ads_library_scout/scout.py fetch --terms "calm cap" --out ad-scout-reports/raw.json
python3 tools/ads_library_scout/scout.py analyze --raw ad-scout-reports/raw.json --aov 35
```
Báo cáo được lưu trong thư mục `ad-scout-reports/`.

## 3. Điểm winning (0–100)
| Thành phần | Điểm tối đa | Ý nghĩa |
|---|---|---|
| Số ads đang chạy | 30 | Nhiều creative đang chạy cùng lúc, tối đa ở 30 ads |
| Đã chạy ≥ 30 ngày | 25 | Quảng cáo sống lâu thường là đang có lãi |
| Ads mới trong 7 ngày | 20 | Đang thêm creative, tức là đang scale |
| Reach EU | 15 | Tối đa ở 1 triệu người |
| Số quốc gia | 10 | Đang mở rộng thị trường, tối đa ở 5 nước |

**Gợi ý đọc:** ≥ 60 là đáng nghiên cứu ngay · 40–59 là đang test hoặc đang lên · < 40 là mới hoặc nhỏ.

## 4. Nhập tay quảng cáo Mỹ (hoặc bất kỳ nước nào)
Mở https://www.facebook.com/ads/library, lọc *Active ads*, và ghi lại theo mẫu `examples/manual_ads_example.csv`:

| Cột | Ví dụ |
|---|---|
| page_name | Tên trang |
| domain | store.com (dòng link dưới quảng cáo) |
| start_date | 2026-10-05 ("Started running on…") |
| end_date | để trống nếu còn chạy |
| ad_url | link "See ad details" |
| text | câu đầu của nội dung quảng cáo |
| countries | US hoặc "US,CA" |

```bash
python3 tools/ads_library_scout/scout.py analyze --manual my_us_ads.csv --aov 35
```

## 5. Chỉnh giả định ước tính
| Tham số | Mặc định | Ghi chú |
|---|---|---|
| `--aov` | 40 | Giá trị đơn trung bình của sản phẩm đối thủ |
| `--cpm-low` / `--cpm-high` | 6 / 12 USD | CPM EU; Mỹ thường cao hơn (12–25) |
| `--frequency` | 1.4 | Số lần hiển thị trên mỗi người được tiếp cận |
| `--roas-low` / `--roas-high` | 1.2 / 2.5 | Doanh thu ÷ chi tiêu quảng cáo |
| `--daily-per-ad-low` / `-high` | 10 / 50 USD | Dùng khi không có reach (dữ liệu nhập tay) |

## 6. Kiểm thử
```bash
python3 -m unittest discover -s tools/ads_library_scout/tests -v
```
Test chạy offline bằng dữ liệu giả, không gọi API thật.
