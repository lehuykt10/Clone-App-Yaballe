# Brief tìm nhà cung cấp — biến thể bịt tai chống ồn cho chó

Ảnh trong thư mục này là **ảnh thiết kế concept (minh họa vector)**, không phải ảnh chụp sản phẩm thật. Dùng để:
- gửi cho xưởng trên 1688/Alibaba khi hỏi làm OEM theo yêu cầu (`01`, `02`, `03`, `04`);
- giải thích cho xưởng điểm khác biệt so với hàng có sẵn.

Để **tìm bằng hình ảnh** (tính năng tìm theo ảnh của 1688 / Alibaba / AliExpress), hãy dùng ảnh chụp các sản phẩm tham chiếu thật ở bảng dưới. Ảnh vẽ thường cho kết quả tìm theo ảnh kém.

| Ảnh | Nội dung |
|---|---|
| `01-coolfit-hood-hero.png` | Biến thể A: 5 điểm cải tiến |
| `02-coolfit-hood-techpack.png` | Tech pack: hình trải phẳng, mặt cắt đệm tai, bảng vật liệu (BOM) |
| `03-size-fit-guide.png` | Bảng size XS–XL + 2 form (Standard / Wide-face) |
| `04-calm-kit-bundle.png` | Biến thể B: bộ kit 14 ngày trong hộp quà |
| `05-sound-hood-phase2.png` | Biến thể C (giai đoạn 2): mũ có loa |

Sửa ảnh: chỉnh file trong `src/*.html` rồi chạy `NODE_PATH=$(npm root -g) node render.js`.

## Phát hiện quan trọng khi research

Từng tính năng riêng lẻ **đã có người bán**, nhưng chưa thấy sản phẩm nào **gộp tất cả**:

| Tính năng | Đã có trên thị trường | Ví dụ tham chiếu |
|---|---|---|
| Mũ trùm chui đầu, không velcro | Có | [Dog Calming Hood – No Hook-Loop](https://www.amazon.com/Hook-Loop-Reducing-Thunderstorms-Firework-Grooming/dp/B0H3NJYC83), [Dog Calming Head Wrap](https://www.amazon.com/Calming-Head-Cover-Noise-Protection/dp/B0H6QJZ8LV) |
| Vải sợi mát (làm ướt để mát) | Có, nhưng **không có đệm tai cách âm** | [VIPTUVI Cooling Snood](https://www.amazon.com/VIPTUVI-Polyester-Adjustable-Protection-Breathable/dp/B0GV2751Z6), [Kodervo Cooling Head Wrap](https://www.amazon.com/Kodervo-Cooling-Instant-Breathable-Bandana/dp/B0GVHDJXQV) |
| Khóa nam châm | Có, nhưng ở dạng **tai nghe cứng ABS** | [PETSEAR 29dB, magnetic buckle](https://www.amazon.com/clp/B0GJ4CJBWM) |
| Tai nghe phát nhạc cho chó | Có | [Famikako Music Headphones](https://www.amazon.com/Famikako-Music-Headphones-Anxiety-Relief/dp/B0DP1W51PW), [PAWNIX](https://pawnix.com/) |
| Mũ trùm có đệm foam | Có (velcro/neoprene) | [Etsy neoprene hood](https://www.etsy.com/listing/4488459965/happy-hood-dogs-noise-cancelling-dog) |
| Hàng sỉ | Có | [AliExpress dog ear muffs](https://www.aliexpress.us/w/wholesale-dog-ear-muffs.html) |

→ Lợi thế của bạn = **gộp** (vải mát + đệm cách âm tháo rời + không velcro + form theo dáng đầu) **+ bộ kit có chương trình tập**. Đây là khác biệt về cách phối hợp, chưa phải phát minh mới. Cần kiểm tra bằng sáng chế trước khi làm khuôn.

## Từ khóa tìm xưởng

| Hạng mục | 1688 (中文) | Alibaba (EN) |
|---|---|---|
| Mũ trùm lõi | 宠物降噪耳罩头套 · 狗狗安抚头套 · 宠物耳罩 弹力 · 狗狗吹水头套 | dog ear muffs snood, dog calming hood, pet noise reduction ear cover |
| Vải mát | 凉感纱 针织面料 · 冰丝 3D网眼布 | cooling yarn knit fabric, 3D air mesh fabric |
| Đệm tai cách âm | 高密度隔音棉 · 吸音海绵 定制 | acoustic foam custom shape, sound absorbing PU foam |
| Khóa nam châm | 磁吸扣 织带 · 磁力安全扣 | magnetic buckle webbing 20mm |
| Silicone chống trượt | 硅胶防滑 印花 | silicone dot grip print |
| Áo ép cho kit | 宠物安抚衣 · 狗狗雷雨衣 | dog anxiety vest, calming wrap |
| Thảm liếm | 宠物舔食垫 吸盘 硅胶 | lick mat suction silicone |
| Hộp quà | 牛皮纸礼盒 磁吸 定制logo | kraft magnetic gift box custom |

## Tin nhắn mẫu gửi xưởng (EN / 中文)

> Hello, we are developing a dog calming hood (see attached design 01–03). We need: cooling-yarn knit outer, removable high-density acoustic foam ear pods in zip pockets, silicone grip, magnetic buckle (no hook-and-loop), sizes XS–XL + wide-face cut. Can you make samples? Please quote sample cost, lead time, MOQ per color, and unit price at 300 / 1000 / 3000 pcs.
>
> 您好，我们在开发一款狗狗安抚降噪头套（见附图01–03）。要求：凉感纱针织外层，可拆卸高密度隔音棉耳垫（拉链口袋），硅胶防滑，磁吸扣（不要魔术贴），尺码XS–XL及宽脸版。请报样品费、打样周期、每色起订量，以及300/1000/3000件单价。

## Checklist chọn xưởng

- [ ] Đã làm hàng thú cưng/mũ trùm (xem ảnh sản phẩm có sẵn trong shop)
- [ ] Đồng ý may mẫu theo bản vẽ, phí mẫu ≤ $50
- [ ] MOQ ≤ 300/màu
- [ ] Gửi được chứng nhận/test vải (OEKO-TEX, phai màu)
- [ ] Đặt mẫu ở 2–3 xưởng song song, so sánh độ giảm tiếng (dB, đo bằng app trên điện thoại) và độ bám khi chó lắc đầu
