# Design system: choosing colours, fonts and shape

Goal: look **clearly different from the competitor** while fitting what buyers in the
niche expect. Decide the brand *mood* first, then pick from the table, then adjust.

## Mood → starting palette (background / surface / text / primary / dark)

| Mood | Fits | background | surface | text | primary | dark | Fonts (heading / body) | radius |
|---|---|---|---|---|---|---|---|---|
| Warm & caring | pets, baby, gifts, memorial | #FAF7F2 | #EDE6DA | #2B2B28 | #B8573A | #3F5A4A | quicksand_n7 / nunito_sans_n4 | rounded |
| Fresh & clean | skincare, wellness, cleaning | #FFFFFF | #EEF4F1 | #1E2B26 | #2F7D63 | #173A30 | dm_sans_n6 / dm_sans_n4 | soft |
| Soft luxury | jewelry, beauty, fashion | #FBF9F7 | #F1ECE6 | #1C1A19 | #1C1A19 | #3A2E2A | cormorant_n6 / work_sans_n4 | sharp |
| Bold & energetic | fitness, gadgets, outdoor | #FFFFFF | #F2F2F2 | #111111 | #C2410C | #111111 | montserrat_n8 / karla_n4 | soft |
| Calm & natural | home decor, kitchen, eco | #FBF8F3 | #F1E9DD | #2A241F | #9C4A2F | #2F3B34 | lora_n7 / nunito_sans_n4 | rounded |
| Playful | kids, toys, novelty | #FFFDF7 | #FFF1D6 | #22223B | #C63D17 | #22223B | poppins_n7 / nunito_sans_n4 | rounded |
| Tech & precise | electronics, car accessories | #F7F8FA | #E9EDF2 | #0F172A | #2563EB | #0F172A | poppins_n6 / assistant_n4 | soft |

## Rules
1. **Contrast ≥ 4.5:1** for body text and button labels (WCAG AA). Check every pair:
   text/background, text/surface, primary_text/primary, dark_text/dark.
   Quick check in Python:
   ```python
   def L(h):
       c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
       c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
       return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
   def ratio(a,b):
       la,lb=sorted([L(a),L(b)],reverse=True); return (la+0.05)/(lb+0.05)
   print(round(ratio("#FFFFFF","#B8573A"),2))
   ```
2. **One accent colour** for buttons and badges. Do not use the competitor's button colour.
3. **Rhythm:** alternate scheme-1 and scheme-2 sections; one dark section (scheme-3)
   near the bottom gives the page an ending.
4. **Photography style** matters more than colour: decide one (bright daylight lifestyle,
   studio on colour background, UGC phone style) and brief it to the owner.
5. **Mobile first:** 70–85 % of ad traffic is mobile. Check the product page at 390 px:
   the price and Add to cart must be visible without scrolling past the first image.
6. Max 2 font families. Headings 1.1–1.3× scale. Body ≥ 16 px equivalent.
