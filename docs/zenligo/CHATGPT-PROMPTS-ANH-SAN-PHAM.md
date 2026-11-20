# Prompt ChatGPT: bộ ảnh sản phẩm Zenligo Calm Cap cho Shopify

Dùng trong **một cuộc trò chuyện ChatGPT duy nhất** để mọi ảnh giữ đúng một sản phẩm.
Ảnh xuất ra **vuông 1:1** (Shopify gallery). Ảnh cho section "Image with story" dùng **4:5**.

---

## BƯỚC 0: Đính kèm ảnh tham chiếu + dán prompt khóa sản phẩm

Đính kèm **5 ảnh** theo thứ tự:
1–3. Ba ảnh mũ gấp phẳng **chụp thật** (xanh nhạt, xanh denim, hồng). Dùng nguyên ảnh.
4. `ref-images/ref-4a-blackout-lying.jpg` (đã cắt bỏ tiêu đề và nhãn sai "Thermal/Cold therapy… migraines").
5. `ref-images/ref-4b-see-through-coffee.jpg` và `ref-images/ref-5-blackout-front.jpg` (đã cắt bỏ logo BAOZHIK và chữ Trung).

**Không** đính kèm ảnh gốc có chữ, logo hay nhãn. ChatGPT dễ chép lại chữ và logo vào ảnh mới.

```
I'm building product photos for my brand Zenligo. The attached photos show the exact product.
For every image I ask for in this chat, reproduce THIS product exactly. Do not redesign it.

PRODUCT LOCK — "Zenligo Calm Cap":
- A soft, stretchy, one-piece fabric hood that covers the whole head from forehead to nape.
- Fabric: heathered cotton-jersey knit with visible fine melange texture.
- Front: a padded, rounded eye-mask panel stitched onto the hood, shaped like a sleep mask
  with a gentle notch at the nose.
- The eye panel has white embroidery: two open palms facing up, decorated with wavy lines and a
  crescent moon, surrounded by small four-point stars and tiny circles. Keep this embroidery exact.
- 2-in-1: "Blackout mode" = hood pulled fully down, the padded panel covers the eyes.
  "See-through mode" = the panel is flipped up onto the forehead, revealing a goggle-shaped
  opening around the eyes; the fabric still covers the forehead, temples, cheekbones and back of head.
- An opening at the crown lets a bun or ponytail come through the top.
- No straps, no Velcro, no buttons, no visible logos or text on the product.
- Colors: Sky Blue (light, cotton-like), Denim Blue (heathered mid-blue), Rose Pink (heathered).
  Default color is Denim Blue unless I say otherwise.
- Flat size: 16.5 cm top width, 22.5 cm bottom width, 17 cm height.

STYLE LOCK (all images):
- Photorealistic commercial photography, natural soft light, calm and premium mood.
- Palette: soft indigo, misty blue, warm off-white, light oak wood.
- Real-looking adults (25–55), relaxed, natural skin texture, no exaggerated smiles, no celebrities.
- NO text, letters, logos or watermarks in the image unless I explicitly ask for them.
- Square 1:1, high resolution, product clearly visible and sharp.

REFERENCE PRIORITY:
- The flat-lay photos are REAL product photos: they are the ground truth for fabric, color and
  embroidery. The embroidery is real thread stitching, tone-on-tone and slightly raised
  (white thread on Sky Blue, pale-blue thread on Denim Blue, pale-pink thread on Rose Pink),
  NOT a bold white print.
- The worn photos are AI mock-ups from the supplier: use them ONLY to understand the shape and
  how the cap sits on the head in each mode. Ignore their flat white printed look.

Reply "Locked" and wait for my first image request.
```

---

## BƯỚC 1: 12 ảnh (dán từng prompt một, mỗi lần một ảnh)

### Ảnh 1 · Hero gallery: GÓC "Tôi vẫn phải làm việc"
```
Image 1 (square). A woman in her 30s at a home desk by a window, mid-morning light, typing on a
laptop. She wears the Calm Cap in Denim Blue in SEE-THROUGH MODE: eye panel flipped up on her
forehead, her eyes visible through the goggle-shaped opening, bun coming out of the top opening.
Calm, focused expression, a mug of tea beside the laptop. Laptop screen shows a soft blurred
spreadsheet. Camera at eye level, 3/4 angle so the cap's shape and embroidery are clear.
```

### Ảnh 2 · Packshot nền trắng (ảnh sản phẩm chuẩn)
```
Image 2 (square). Studio packshot of the Calm Cap in Denim Blue, folded flat exactly like the
reference photo, embroidered eye panel facing the camera, centered on a pure white background
(#FFFFFF), soft natural shadow underneath, shot from slightly above. Product fills about 75% of the frame.
```

### Ảnh 3 · Hai chế độ (ảnh giải thích quan trọng nhất)
```
Image 3 (square). Split image, two halves, same woman, same plain warm off-white background.
Left: Calm Cap in BLACKOUT MODE, panel fully covering her eyes, relaxed smile.
Right: SEE-THROUGH MODE, panel flipped up, eyes visible through the opening.
Add two small clean labels at the bottom of each half in a modern sans-serif:
"Blackout mode" and "See-through mode". No other text.
```

### Ảnh 4 · GÓC "Ngủ trưa che sáng hoàn toàn"
```
Image 4 (square). A woman lying on a light linen sofa in a dim afternoon room, curtains half
closed, soft daylight from the side. She wears the Calm Cap in Sky Blue in BLACKOUT MODE,
fully relaxed, a knitted throw over her legs. Quiet, peaceful mood. Camera from above at a slight angle.
```

### Ảnh 5 · GÓC "Ngày dài trước màn hình"
```
Image 5 (square). Evening at home: a man in his 40s on a sofa, laptop on his lap, warm lamp
light plus cool screen glow. He wears the Calm Cap in Denim Blue in SEE-THROUGH MODE, leaning
back and exhaling, visibly winding down after a long screen day. Cozy, calm, realistic.
```

### Ảnh 6 · GÓC "Sáng hôm sau bữa tiệc" (Tết Dương lịch / sau tiệc)
```
Image 6 (square). Bright late morning after a New Year's Eve party: a woman curled up on a
sofa in pajamas, a few gold confetti pieces and an empty party hat on the coffee table, a glass
of water and coffee nearby. She wears the Calm Cap in Rose Pink in BLACKOUT MODE, playful and
cozy, slightly amused. Light, humorous tone, not messy.
```

### Ảnh 7 · GÓC "Quà cho mẹ"
```
Image 7 (square). Christmas morning in a warm living room with a softly lit tree in the background.
A woman in her 50s opens a gift box and lifts out the Calm Cap in Sky Blue, smiling. Her adult
daughter sits beside her. Kraft paper box with a navy ribbon, no text on the box. Warm, genuine moment.
```

### Ảnh 8 · Lạnh hoặc ấm
```
Image 8 (square). Clean split image on a light oak kitchen counter.
Left half, cool tones: the Calm Cap in Denim Blue being taken out of an open refrigerator by a
hand, a light frosty feel. Right half, warm tones: the same cap folded next to a cup of herbal
tea and a soft warm glow. Small labels at the bottom: "Cold" and "Warm". No other text.
```
> Lưu ý: chưa xác nhận cách làm ấm với NCC. Nếu NCC nói làm ấm bằng lò vi sóng, có thể thay nửa phải bằng cảnh lò vi sóng.

### Ảnh 9 · Kích thước và cách đeo
```
Image 9 (square). Flat lay of the Calm Cap in Denim Blue on a pure white background, folded flat,
viewed straight from above. Add thin dark-grey measurement lines with labels:
"16.5 cm" across the top edge, "22.5 cm" across the bottom edge, "17 cm" on the right side.
Small inset circle at the top-right corner showing the crown opening with a bun coming through.
Clean infographic style, no other text.
```

### Ảnh 10 · Bảng màu
```
Image 10 (square). Three Calm Caps folded flat side by side on a warm off-white background:
Sky Blue, Denim Blue, Rose Pink, embroidery facing the camera, evenly lit, soft shadows,
slightly overhead angle. No text.
```

### Ảnh 11 · Dùng cho section "Feature hotspots" (đặt chấm giải thích)
```
Image 11 (square). Studio shot of the Calm Cap in Denim Blue worn on a plain light-grey
mannequin head, 3/4 front view, SEE-THROUGH MODE with the panel flipped up so both the
embroidered panel and the eye opening are visible, top opening visible. Pure white background,
even light, every detail sharp. No text.
```
> Trên Shopify, kéo 4 chấm vào: eye panel · gel quanh thái dương · lỗ búi tóc · vải co giãn.

### Ảnh 12 · Section "Image with story" (khung dọc 4:5)
```
Image 12, PORTRAIT 4:5 this time. Close, intimate shot of a woman at a kitchen table in morning
light, both hands around a coffee mug, wearing the Calm Cap in Denim Blue in SEE-THROUGH MODE,
eyes open, calm and present. Soft background with plants. Leave some calm empty space at the top.
```

---

## BƯỚC 2: Sửa ảnh khi sai (dán prompt này)

```
Fix this image. Keep everything else identical, only correct the product so it matches the
PRODUCT LOCK: [ví dụ: the embroidery must be two open palms with a crescent moon and stars /
the eye opening must be goggle-shaped / remove the strap / remove any text / remove the logo].
```

**Kiểm tra mỗi ảnh trước khi dùng:**
- Hình thêu đúng 2 bàn tay, có trăng và sao.
- Khe mắt hình kính bơi khi lật panel lên.
- Có lỗ búi tóc trên đỉnh.
- Không có dây, velcro, chữ lạ hay logo.
- Tay và ngón tay bình thường, mặt không méo.

---

## BƯỚC 3: Đưa lên Shopify

| Thứ tự gallery | Ảnh | Alt text (tiếng Anh, dán vào Shopify) |
|---|---|---|
| 1 | Ảnh 1 | Woman working at a laptop wearing the Zenligo Calm Cap in see-through mode |
| 2 | Ảnh 3 | Zenligo Calm Cap blackout mode and see-through mode side by side |
| 3 | Ảnh 2 | Zenligo Calm Cap in Denim Blue, folded flat on white |
| 4 | Ảnh 4 | Woman resting on a sofa wearing the Calm Cap in blackout mode |
| 5 | Ảnh 5 | Man winding down after a long screen day wearing the Calm Cap |
| 6 | Ảnh 8 | Calm Cap can be chilled or warmed |
| 7 | Ảnh 6 | Relaxing the morning after a party in the Calm Cap |
| 8 | Ảnh 7 | Calm Cap as a gift for mom |
| 9 | Ảnh 9 | Calm Cap size: 16.5 cm top, 22.5 cm bottom, 17 cm tall, with bun opening |
| 10 | Ảnh 10 | Calm Cap colors: Sky Blue, Denim Blue, Rose Pink |
| Section Feature hotspots | Ảnh 11 | |
| Section Image with story | Ảnh 12 | |

- Xuất **PNG/JPG 2048×2048** (dùng upscale nếu ChatGPT trả ảnh nhỏ hơn).
- Đặt tên file kiểu `zenligo-calm-cap-see-through-desk.jpg` để tốt cho SEO.

## Quy tắc (bắt buộc)
- Không có chữ "migraine", "headache relief" hay "pain" trên ảnh.
- Người mẫu AI chỉ dùng làm ảnh minh họa, không trình bày như khách hàng thật hay review.
- Khi có hàng mẫu, thay dần bằng ảnh và video thật (nhất là ảnh 2, 9, 10).
- Nếu bán nhiều màu, tạo variant màu trong Shopify và gắn ảnh 10 hoặc ảnh riêng của từng màu.

---

## PHỤ LỤC: Ánh sáng "chân thật" kiểu UGC (cho ảnh keyframe video Reels)

Tham chiếu: reel herbtantra (Migraine Go Cap). Ánh sáng ban ngày qua rèm mỏng, chụp bằng camera trước điện thoại, không có đèn studio.

### Khóa phong cách UGC (dán thêm vào cuối prompt ảnh)
```
UGC REALISM LOCK — this must look like a real iPhone front-camera selfie, NOT a studio or
stock photo:
- Light: soft overcast daylight from one window to the side, filtered through a sheer white
  curtain. Neutral-cool white balance. Gentle falloff into soft shadows on the far side of the
  face. No studio lights, no rim light, no golden-hour glow, no dramatic contrast.
- Camera: iPhone front camera at arm's length, slightly above eye level, 24–26 mm wide-angle,
  vertical 9:16, face close and filling the upper-middle frame, slightly off-center.
  Deep focus like a phone (background only mildly soft), no cinematic bokeh.
- Image quality: slight phone noise in the shadows, mild smartphone HDR, a touch of motion
  softness, imperfect framing.
- Person: real-looking, no or minimal makeup, visible skin texture and pores, slightly messy
  hair, tired-but-calm natural expression, not posing, not smiling for the camera.
- Setting: an ordinary lived-in room: plain off-white wall, a rumpled grey fleece blanket,
  a muted dusty-rose pillow, nothing styled or perfect.
- NO text, captions, stickers, logos or UI elements in the image.
```

### Ví dụ 1: Blackout mode (giống khung hình tham chiếu)
```
Vertical 9:16. A woman in her late 20s lying on a sofa under a grey fleece blanket, head on a
dusty-rose pillow, filming herself with her phone. She wears the Calm Cap in Denim Blue in
BLACKOUT MODE, eye panel down, only her nose, lips and chin visible, relaxed, one hand resting
near her cheek. [UGC REALISM LOCK]
```

### Ví dụ 2: See-through mode (góc "tôi vẫn phải làm việc", điểm khác biệt của Zenligo)
```
Vertical 9:16. Same woman, same sofa and light, now half sitting up, eye panel flipped up so
her eyes look straight into the phone camera through the goggle-shaped opening, a laptop
glowing softly at the bottom edge of the frame. Calm, slightly tired, a hint of a smile.
[UGC REALISM LOCK]
```

### Mẹo
- Có thể đính kèm ảnh chụp màn hình reel kèm câu: *"Use this screenshot ONLY as a reference for
  lighting, camera angle and mood. Do not copy the person, the product, the text or any brand."*
- Nếu ảnh vẫn "quá đẹp", gửi tiếp: *"Make it less polished: flatter light, more phone noise, less
  perfect skin, more ordinary room."*
- Ảnh ra quá ấm hoặc vàng thì gửi: *"cooler, neutral daylight white balance"*.
- Hậu kỳ (CapCut/Lightroom): giảm độ nét 10–15, thêm grain 10–20, giảm saturation một chút.
- Dùng ảnh này làm keyframe cho video Seedance/Wan (skill viral-video-recreation).

### Không chép từ reel đối thủ
- Hook "I hated taking medicines… until I found this" là tuyên bố y tế. Zenligo không dùng.
  Thay bằng: *"My heavy-head days used to mean lying in the dark. Now I can still see my screen."*
- Không trình bày người mẫu AI như khách hàng thật; gắn nhãn nội dung AI khi nền tảng yêu cầu.
