"""Writes theme/templates/product.glow-wings-es.json: Spanish (Latin American, tú) Glow Wings page.

Same sections as product.glow-wings.json; open it with ?view=glow-wings-es on the Glow Wings product.
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "glow-wings"))
from build_template import HDR, TEMPLATE  # noqa: E402

T = copy.deepcopy(TEMPLATE)
S = T["sections"]


def setb(sec, key, **kw):
    S[sec]["blocks"][key]["settings"].update(kw)


m = S["main"]["settings"]
m.update({
    "stock_line": "6 ESTILOS DE ALAS · PARA LA MAYORÍA DE COLLARES",
    "bundle_heading": "Ahorra en paquete", "show_description": False, "sticky_label": "Agregar al carrito",
    "trust_1": "Envío gratis a todo el mundo", "trust_2": "Garantía de 30 días", "trust_3": "Impuestos y aranceles incluidos",
    "tier_1_label": "1 luz Glow Wings", "tier_2_label": "2 luces · combina estilos", "tier_2_badge": "PARA 2 PERROS",
    "tier_3_label": "3 luces · combina estilos", "tier_3_badge": "MEJOR PRECIO",
    "label_add": "Agregar al carrito", "label_sold_out": "Agotado", "label_timer": "¡Date prisa! La oferta termina en:",
    "label_size_link": "📏 ¿No sabes qué talla? Abre la guía de tallas", "label_description": "Descripción",
    "label_you_save": "Ahorras", "label_save": "Ahorra", "label_item": "Artículo", "label_your_pick": "Tu elección",
    "label_item_one": "artículo", "label_item_other": "artículos", "label_free": "GRATIS",
    "label_sold_out_error": "Uno de tus artículos está agotado. Elige otro estilo.",
})
setb("main", "perk-1", text="Proyecta alas brillantes en el suelo alrededor de tu perro")
setb("main", "perk-2", text="La luz lateral ayuda a autos y ciclistas a ver a tu perro de noche")
setb("main", "perk-3", text="Correa ajustable para la mayoría de collares y arneses")
setb("main", "perk-4", text="6 estilos: mariposas, dragones y ángeles")
setb("main", "acc-1", title="Cómo se ve en la vida real", content=
     "<p>La luz proyecta el diseño de alas en el suelo, al lado y detrás de tu perro. Se ve más brillante sobre superficies "
     "oscuras y lisas como caminos, banquetas y nieve, y más suave sobre el pasto o bajo luces de calle muy fuertes.</p>"
     "<p>Las fotos del producto son ilustraciones del efecto. Las alas aparecen en el suelo, no pegadas a tu perro.</p>")
setb("main", "acc-2", title="Qué incluye", content=
     "<ul><li>1 luz Glow Wings con correa ajustable, en el estilo que elijas</li><li>1 cable de carga USB</li></ul>")
setb("main", "acc-3", title="Batería y carga", content=
     "<p>Batería recargable integrada. Cárgala con el cable USB incluido en cualquier cargador USB o laptop. Una carga "
     "alcanza para varios paseos nocturnos; cuando la luz empiece a bajar, vuelve a cargarla.</p>")
setb("main", "acc-4", title="Ajuste, cuidado y seguridad", content=
     "<ul><li>Enrolla la correa en el collar o arnés de tu perro y ajústala para que la luz apunte hacia atrás.</li>"
     "<li>No es un juguete. No dejes que tu perro muerda la luz.</li>"
     "<li>Resiste lluvia ligera y nieve. No la sumerjas ni dejes que tu perro nade con ella.</li>"
     "<li>Límpiala con un paño seco.</li>"
     "<li>Siempre pasea con correa y mantente visible tú también. La luz es un extra, no reemplaza el equipo reflectante.</li></ul>")
setb("main", "acc-5", title="Envío", content=
     "<p>Envío gratis a todo el mundo con seguimiento. Los pedidos a EE. UU. suelen llegar en 9–17 días; a Canadá, el Reino "
     "Unido y Australia en 10–20 días; a la mayoría de los demás países en 12–25 días. Todos los impuestos y aranceles están "
     "incluidos, así que no pagas nada extra al recibir. <a href=\"/pages/shipping-policy\">Política de envío completa</a></p>")
setb("main", "acc-6", title="Nuestra garantía", content=
     "<p>Si llega dañado o con fallas, envía una foto a support@suzeno.com dentro de los 30 días y te devolvemos el dinero "
     "o te enviamos un reemplazo.</p>")

S["band"]["settings"].update(before="Paseos nocturnos", circled="mágicos",
                             text="Alas brillantes en el camino. Una luz lateral que ayuda a los conductores a verte.")
S["story"]["settings"].update(
    eyebrow="Por qué les encanta", heading="Oscurece temprano, pero tu perro sigue", circled="brillando",
    text="<p>Desde noviembre, casi todos los paseos son de noche. Tu perro desaparece en la oscuridad y cada auto parece "
         "pasar demasiado cerca.</p><p>Glow Wings se enrolla en el collar y proyecta un par de alas brillantes en el camino "
         "alrededor de tu perro, mientras una luz a cada lado ayuda a que los demás los vean. Elige mariposas, dragones o "
         "ángeles.</p><p>Colócala, enciéndela y a caminar. Tu paseo nocturno se convierte en la mejor foto del día.</p>")
S["hotspots"]["settings"].update(eyebrow="Pequeña luz, gran efecto", heading="Cómo funciona Glow Wings")
setb("hotspots", "h-1", title="Lente de proyección", text="Proyecta el diseño de alas hacia abajo y atrás, sobre el suelo.")
setb("hotspots", "h-2", title="Luz lateral", text="Brilla a ambos lados para que tu perro se vea mejor.")
setb("hotspots", "h-3", title="Correa ajustable", text="Se enrolla en la mayoría de collares y correas de arnés.")
setb("hotspots", "h-4", title="Hebilla metálica", text="Mantiene la correa firme para que la luz siga apuntando hacia atrás.")
S["how"]["settings"].update(heading="Lista en 10 segundos")
setb("how", "s-1", title="Colócala", text="Enrolla la correa en el collar con el lente hacia atrás.")
setb("how", "s-2", title="Enciéndela", text="Presiona el botón. Las alas aparecen en el suelo detrás de tu perro.")
setb("how", "s-3", title="Camina y brilla", text="Se ve mejor en caminos oscuros, banquetas y nieve. Apágala al llegar a casa.")
S["faq"]["settings"].update({
    "heading": "Bueno saber", "tracking_url": "https://t.17track.net/es#nums=",
    "label_contact": "Contáctanos", "label_contact_text": "¿Preguntas sobre tu pedido? Envíanos un mensaje y te respondemos en 1 día hábil.",
    "label_name": "Nombre", "label_email": "Correo electrónico", "label_order": "Número de pedido (opcional)",
    "label_message": "Tu mensaje", "label_send": "Enviar mensaje", "label_thanks": "¡Gracias! Recibimos tu mensaje.",
    "label_email_us": "O escríbenos a", "label_track": "Rastrea tu pedido", "label_tracking_number": "Número de rastreo",
    "label_track_button": "Rastrear paquete"})
FAQ = {
    "q-1": ("¿Se verá como en las fotos?", "<p>Las fotos muestran el efecto. En la vida real, las alas se proyectan en el suelo alrededor de tu perro. Se ven más brillantes sobre superficies oscuras y lisas, y más suaves sobre el pasto o bajo luces de calle.</p>"),
    "q-2": ("¿Le queda al collar de mi perro?", "<p>La correa ajustable se enrolla en la mayoría de collares y correas de arnés. Funciona para perros pequeños y grandes.</p>"),
    "q-3": ("¿Mantiene seguro a mi perro de noche?", "<p>Las luces laterales ayudan a conductores y ciclistas a ver a tu perro, pero ninguna luz garantiza la seguridad. Siempre usa correa y mantente visible tú también.</p>"),
    "q-4": ("¿Cómo la cargo?", "<p>Conecta el cable USB incluido a cualquier cargador USB o laptop. Una carga alcanza para varios paseos nocturnos.</p>"),
    "q-5": ("¿Puedo elegir estilos diferentes en un mismo pedido?", "<p>Sí. En los paquetes de 2 y 3 luces eliges un estilo para cada luz.</p>"),
    "q-6": ("¿Cuándo llega mi pedido?", "<p>Los pedidos a EE. UU. suelen llegar en 9–17 días; a Canadá, el Reino Unido y Australia en 10–20 días; a la mayoría de los demás países en 12–25 días. Recibes un enlace de seguimiento por correo en cuanto se envía.</p>"),
    "q-7": ("¿Tendré que pagar aduana o impuestos?", "<p>No. Nuestros precios incluyen todos los impuestos y aranceles, así que el precio al pagar es el precio final.</p>"),
    "q-8": ("¿Qué pasa si llega dañado o no funciona?", "<p>Escríbenos a support@suzeno.com dentro de los 30 días posteriores a la entrega y te devolvemos el dinero o te enviamos un reemplazo.</p>"),
}
for k, (q, a) in FAQ.items():
    setb("faq", k, question=q, answer=a)
S["reviews"]["settings"].update(heading="Lo que dicen nuestros clientes")

if __name__ == "__main__":
    leftover = [b for sec in S.values() for b in sec.get("blocks", {}).values()
                if any(w in json.dumps(b["settings"]) for w in (" the ", " your ", "Wrap "))]
    assert not leftover, leftover
    out = Path(__file__).resolve().parent.parent / "theme/templates/product.glow-wings-es.json"
    out.write_text(HDR + json.dumps(T, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", out)
