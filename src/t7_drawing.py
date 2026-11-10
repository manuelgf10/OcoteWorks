"""Ilustración de línea de una moto de aventura tipo Ténéré 700 (dibujo propio OcoteWorks, vista lateral derecha,
frente a la derecha). Escala 0.4 px/mm con medidas reales aproximadas: distancia entre ejes 1595, asiento 875,
altura con parabrisas 1455, rines 21"/18". Piso en y=566."""
import math

S = 0.4
GROUND = 566
RA = (200, GROUND - 667 * S / 2)   # eje trasero (150/70-18)
FA = (838, GROUND - 695 * S / 2)   # eje delantero (90/90-21)


def wheel(cx, cy, r, rim, front=False):
    t = r - rim
    s = [f'<circle cx="{cx}" cy="{cy}" r="{r - t / 2:.1f}" class="t7-tire" style="stroke-width:{t:.1f}"/>']
    for i in range(30 if front else 28):  # tacos
        a = i * 2 * math.pi / (30 if front else 28)
        x1, y1 = cx + (r - 1) * math.cos(a), cy + (r - 1) * math.sin(a)
        x2, y2 = cx + (r - 7) * math.cos(a), cy + (r - 7) * math.sin(a)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="t7-knob"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{rim:.1f}" class="t7-l"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{rim - 6:.1f}" class="t7-thin"/>')
    for i in range(18):  # rayos
        a = i * math.pi / 9
        x1, y1 = cx + 12 * math.cos(a + .55), cy + 12 * math.sin(a + .55)
        x2, y2 = cx + (rim - 6) * math.cos(a), cy + (rim - 6) * math.sin(a)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="t7-spoke"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{44 if front else 34}" class="t7-l t7-disc"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="13" class="t7-l t7-fill"/>')
    return "".join(s)


def svg():
    p = []
    p.append(f'<line x1="10" y1="{GROUND + 1}" x2="1030" y2="{GROUND + 1}" class="t7-ground"/>')
    # basculante + amortiguador
    p.append('<path class="t7-l t7-fill" d="M200 433 L486 362 Q496 360 498 372 L500 382 L208 448 Z"/>')
    p.append('<path class="t7-l" d="M452 250 L430 362"/><path class="t7-spring" d="M447 268 L433 340"/>')
    # rueda trasera y delantera
    p.append(wheel(*RA, 133.4, 91.4))
    p.append(wheel(*FA, 139, 106.7, front=True))
    p.append('<path class="t7-l" d="M63.4 396.0 L67.1 384.2 L71.8 372.8 L77.5 361.9 L84.2 351.5 L91.7 341.7 L100.0 332.6 L109.1 324.3 L118.9 316.8 L129.3 310.1 L140.2 304.4 L151.6 299.7 L163.4 296.0 L175.4 293.3 L187.7 291.7 L200.0 291.2 L212.3 291.7 L224.6 293.3 L236.6 296.0 L248.4 299.7 L259.8 304.4 L270.7 310.1"/>')
    # escape corto (lado derecho), hacia arriba
    p.append('<path class="t7-l t7-fill" d="M318 268 L424 250 Q436 248 438 260 L442 288 Q443 298 432 300 L326 316 Q314 318 312 306 Z"/>')
    p.append('<path class="t7-thin" d="M330 276 L428 260 M332 304 L432 290"/>')
    p.append('<path class="t7-l" d="M440 280 Q500 284 520 340"/>')
    # motor (bicilíndrico en línea, cilindros inclinados al frente) y cubrecárter
    p.append('<path class="t7-l t7-fill" d="M500 318 L652 300 Q676 298 680 322 L688 404 Q690 430 664 434 L532 444 Q504 446 500 418 Z"/>')
    p.append('<path class="t7-l t7-fill" d="M598 304 L648 252 Q660 240 674 252 L708 288 Q716 298 704 308 L682 322"/>')
    p.append('<path class="t7-thin" d="M618 290 L664 262 M628 302 L684 276 M534 348 L650 336 M538 374 L656 364"/>')
    p.append('<circle cx="566" cy="400" r="24" class="t7-l"/><circle cx="566" cy="400" r="9" class="t7-thin"/>')
    p.append('<path class="t7-l t7-skid" d="M496 440 L684 428 L712 448 L664 472 L516 474 Z"/>')
    p.append('<path class="t7-thin" d="M540 452 L540 470 M580 450 L580 471 M620 447 L620 470"/>')
    # chasis tubular visible
    p.append('<path class="t7-l" d="M706 168 L620 262 L524 318 M706 168 L700 258 L688 322 M486 362 L524 318"/>')
    # horquilla invertida (27°), barras y botellas
    p.append('<path class="t7-l t7-fill" d="M694 156 L712 152 L768 330 L748 336 Z"/>')
    p.append('<path class="t7-l t7-fill" d="M748 316 L774 308 L846 422 L826 430 Z"/>')
    p.append('<path class="t7-l t7-fill" d="M684 168 L730 156 L736 172 L690 184 Z"/>')
    # salpicadera delantera baja
    p.append('<path class="t7-l t7-fill" d="M709.8 353.0 L716.8 342.1 L724.6 331.9 L733.3 322.3 L742.9 313.6 L753.1 305.8 L764.0 298.8 L775.5 292.9 L787.4 287.9 L799.7 284.0 L812.3 281.2 L825.1 279.6 L838.0 279.0 L850.9 279.6 L863.7 281.2 L876.3 284.0 L888.6 287.9 L900.5 292.9 L912.0 298.8 L922.9 305.8 L933.1 313.6 L942.7 322.3 L951.4 331.9 L959.2 342.1 L966.2 353.0 L974.8 348.0 L967.4 336.4 L959.0 325.4 L949.7 315.3 L939.6 306.0 L928.6 297.6 L917.0 290.2 L904.8 283.8 L892.0 278.5 L878.9 274.4 L865.4 271.4 L851.8 269.6 L838.0 269.0 L824.2 269.6 L810.6 271.4 L797.1 274.4 L784.0 278.5 L771.2 283.8 L759.0 290.2 L747.4 297.6 L736.4 306.0 L726.3 315.3 L717.0 325.4 L708.6 336.4 L701.2 348.0 Z"/>')
    # cola: subchasis, porta placa y calavera
    p.append('<path class="t7-l" d="M118 220 L86 298 L112 302"/><rect x="74" y="298" width="46" height="30" rx="3" class="t7-l t7-fill"/>')
    p.append('<path class="t7-l t7-fill" d="M110 198 L330 194 L372 222 L316 236 L146 216 Z"/>')
    p.append('<path class="t7-l t7-tl" d="M104 196 L122 196 L124 218 L108 222 Z"/>')
    # tapa lateral
    p.append('<path class="t7-l t7-fill" d="M352 232 L502 214 L516 230 L494 296 L380 302 Z"/>')
    # asiento largo y plano
    p.append('<path class="t7-l t7-seat" d="M298 194 Q298 184 314 184 L548 202 Q572 204 586 216 L564 222 L318 206 Q300 204 298 194 Z"/>')
    # tanque alto y angosto + cubiertas del radiador
    p.append('<path class="t7-l t7-fill" d="M560 214 Q588 168 652 158 L700 154 Q716 156 716 172 L708 236 L640 272 L574 252 Z"/>')
    p.append('<path class="t7-l t7-fill" d="M640 272 L708 236 L742 250 L758 316 L700 338 L664 312 Z"/>')
    p.append('<path class="t7-thin" d="M590 214 L700 194 M668 290 L744 266"/>')
    # torre de navegación, carenado alto con faro de 4 LED y parabrisas
    p.append('<path class="t7-l t7-fill" d="M716 160 L744 104 L784 108 Q808 150 812 206 Q814 248 792 270 L766 274 Q746 238 734 200 Z"/>')
    p.append('<path class="t7-l t7-screen" d="M744 104 L762 34 L780 36 L784 108"/>')
    p.append('<path class="t7-thin" d="M730 130 L776 126"/>')
    for (x, y) in [(780, 176), (796, 176), (782, 208), (798, 208)]:
        p.append(f'<rect x="{x - 6}" y="{y - 11}" width="12" height="22" rx="6" class="t7-l t7-led"/>')
    # manubrio, cubrepuños y espejo
    p.append('<path class="t7-l" d="M708 132 L690 112 L670 108"/>')
    p.append('<path class="t7-l t7-fill" d="M652 98 Q684 88 704 110 Q682 126 654 120 Z"/>')
    p.append('<path class="t7-l" d="M712 126 L718 64 L740 58"/>')
    # estribo
    p.append('<path class="t7-l t7-fill" d="M444 394 L490 392 L492 404 L446 406 Z"/>')
    return ('<svg class="t7-svg" viewBox="40 10 1000 580" role="img" aria-labelledby="t7-title">'
            '<title id="t7-title">{title}</title>' + "".join(p) + '{hotspots}</svg>')


CSS = """.t7-l{fill:none;stroke:var(--carbon);stroke-width:3;stroke-linejoin:round;stroke-linecap:round}
.t7-fill{fill:var(--marfil)}.t7-seat{fill:var(--carbon)}.t7-skid{fill:var(--piedra,#d9d0bd)}.t7-led{fill:var(--cempasuchil)}.t7-tl{fill:var(--ocote)}
.t7-screen{fill:rgba(39,80,162,.12)}.t7-tire{fill:none;stroke:var(--carbon)}
.t7-thin{fill:none;stroke:var(--carbon);stroke-width:1.5}.t7-spoke{stroke:var(--carbon);stroke-width:1.2}.t7-knob{stroke:var(--marfil);stroke-width:3}
.t7-spring{fill:none;stroke:var(--ocote);stroke-width:7;stroke-dasharray:3 3}
.t7-disc{stroke-dasharray:4 4}.t7-ground{stroke:var(--carbon);stroke-width:2;stroke-dasharray:2 6}"""

if __name__ == "__main__":
    css = ("<style>:root{--carbon:#17171A;--marfil:#F4EAD7;--cempasuchil:#EDB544;--ocote:#E48233}"
           "body{margin:0;background:#F4EAD7}.t7-svg{width:1000px;display:block}" + CSS + "</style>")
    open("/tmp/t7.html", "w").write(css + svg().replace("{title}", "T7").replace("{hotspots}", ""))
