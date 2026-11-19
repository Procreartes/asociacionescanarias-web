#!/usr/bin/env python3
"""Genera la web de Asociaciones Canarias (asociacionescanarias.com).

Uso:  python3 scripts/generar.py
Datos editables (Gestor de webs del portal o a mano): data/packs.json, data/planes.json, data/consultas.json,
                  data/extras.json, data/encuentros.json, data/servicios.json
No edites los .html a mano: se sobrescriben.
"""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from web import RAIZ, Sitio, ICO, esc, datos, mailto, imagen, portada_foto, foto  # noqa: E402

CORREO = "hola@naroeconsulting.com"

S = Sitio(
    nombre="Asociaciones Canarias", nombre_corto="Asociaciones Canarias",
    dominio="https://asociacionescanarias.com",
    titular="Naroe Consulting S.L.", nif="B22534804",
    domicilio="Hoya de Parrado, 4 · 35017 Las Palmas de Gran Canaria",
    correo=CORREO, correo_datos="protecciondatos@naroeconsulting.com",
    objeto="Esta web informa sobre Asociaciones Canarias, el servicio de asesoría, gestión y formación para asociaciones de Naroe Consulting S.L., y sobre la forma de contactar.",
    color_tema="#1f5c50", color_fondo="#f7f1e6",
    precarga=["fraunces-latin-700-normal.woff2", "nunito-sans-latin-400-normal.woff2"],
    menu=[("/#servicios", "Servicios"), ("/#packs", "Packs"), ("/#planes", "Planes"), ("/#encuentros", "Encuentros gratis"),
          ("/#formacion", "Formación"), ("/#contacto", "Contacto")],
    marca='<span class="logo-islas" aria-hidden="true"><i></i><i></i><i></i></span><span>Asociaciones <em>Canarias</em></span>',
    pie_html='''<div class="pie-arriba">
      <div><p class="pie-titulo">Asociaciones <em>Canarias</em></p>
      <p>Asesoría, gestión y formación para asociaciones de todo tipo en Canarias.</p></div>
      <div><p class="pie-titulo-chico">Escríbannos</p><p><a href="mailto:hola@naroeconsulting.com">hola@naroeconsulting.com</a></p>
      <p class="pie-nota">Asociaciones Canarias es un servicio de Naroe Consulting S.L.</p></div>
    </div>''',
)

PACKS = datos("packs.json", [])
PLANES = datos("planes.json", [])
CONSULTAS = datos("consultas.json", [])
# Servicios sueltos: [{id, servicio, detalle, precio}]
EXTRAS = datos("extras.json", [])
# Encuentros gratuitos: [{id, titulo, modalidad, fecha, lugar, texto, enlace (inscripción, opcional)}]
ENCUENTROS = datos("encuentros.json", [])

TIPOS = ["Culturales", "Juveniles", "Sociales", "Vecinales", "Deportivas", "ONG y entidades sin ánimo de lucro"]

# Servicios: data/servicios.json [{id, titulo, texto, puntos (una línea por punto), imagen, imagen_alt}]
SERVICIOS = datos("servicios.json", [])

TALLERES = ["Obligaciones legales", "Gestión de asociaciones", "Contabilidad", "Subvenciones", "Contratación", "Facturación electrónica"]
AAPP = ["Ayuntamientos", "Cabildos", "Programas de participación ciudadana", "Concejalías de juventud", "Servicios sociales"]
POR_QUE = ["Asesoría especializada en asociaciones, en Canarias", "Conocemos el IGIC y las convocatorias de las islas", "Planes para todos los tamaños, también para las más pequeñas", "Experiencia en gestión de proyectos y subvenciones",
           "Apoyo en la actividad económica", "Acompañamiento profesional", "Formación práctica"]


def lista(items, clase="lista-check"):
    return f'<ul class="{clase}">' + "".join(f"<li>{ICO['check']}<span>{esc(i)}</span></li>" for i in items) + "</ul>"


def islas():
    """Ocho islas abstractas sobre una línea de mar (decorativo)."""
    formas = [(40, 88, 30, 18), (118, 74, 44, 26), (204, 92, 26, 15), (268, 70, 56, 34), (370, 86, 40, 22),
              (452, 66, 52, 32), (544, 90, 24, 14), (604, 80, 34, 20)]
    elipses = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in formas)
    return f'''<svg class="islas" viewBox="0 0 660 130" aria-hidden="true" focusable="false">
<path class="mar" d="M0 108 C 80 96, 160 120, 240 108 S 400 96, 480 108 S 600 120, 660 106"/>
<g class="tierra">{elipses}</g></svg>'''


def inicio():
    tipos = "".join(f"<li>{esc(t)}</li>" for t in TIPOS)
    areas = ""
    for i, s in enumerate(SERVICIOS, 1):
        img = imagen(s.get("imagen"), s.get("imagen_alt") or "", "(min-width: 1100px) 360px, (min-width: 700px) 45vw, 92vw", "area-foto")
        puntos = [x for x in str(s.get("puntos", "")).splitlines() if x.strip()]
        areas += f'''<article class="area aparece{" con-foto" if img else ""}">{img}
      <div class="area-txt"><span class="area-num" aria-hidden="true">{i:02d}</span>
      <h3>{esc(s.get("titulo"))}</h3><p>{esc(s.get("texto"))}</p>{lista(puntos) if puntos else ""}</div>
    </article>'''

    packs = "".join(f'''<article class="pack aparece{" pack-destacado" if i == 0 else ""}">
      {imagen(p.get("imagen"), p.get("imagen_alt") or "", "(min-width: 1100px) 360px, 92vw", "pack-foto")}<header><h3>{esc(p.get("nombre"))}</h3><p class="pack-lema">{esc(p.get("lema"))}</p></header>
      <p class="precio">{esc(p.get("precio"))}</p>
      <p>{esc(p.get("texto"))}</p>
      {lista([x for x in str(p.get("incluye", "")).splitlines() if x.strip()])}
      <a class="boton boton-linea" href="{mailto(CORREO, "Información sobre el " + p.get("nombre", "pack"))}">Pedir información {ICO["flecha"]}</a>
    </article>''' for i, p in enumerate(PACKS))

    planes = "".join(f'''<li class="plan aparece">
      <h3>{esc(p.get("nombre"))}</h3>
      <p class="plan-para">{esc(p.get("para"))}</p>
      <p class="plan-precio"><span>desde</span> <strong>{esc(p.get("precio"))} €</strong><span>/mes</span></p>
      {f'<p class="plan-nota">{ICO["check"]}{esc(p["nota"])}</p>' if p.get("nota") else ""}
      {lista([x for x in str(p.get("incluye", "")).splitlines() if x.strip()], "lista-check plan-incluye") if p.get("incluye") else ""}
    </li>''' for p in PLANES)

    extras = "".join(f'''<tr><th scope="row">{esc(c.get("servicio"))}{f'<span>{esc(c["detalle"])}</span>' if c.get("detalle") else ""}</th>
      <td>{esc(c.get("precio"))}</td></tr>''' for c in EXTRAS)

    encuentros = "".join(f'''<article class="encuentro aparece">
      <p class="encuentro-tipo">{esc(e.get("modalidad"))} · gratuito</p>
      <h3>{esc(e.get("titulo"))}</h3>
      <p class="encuentro-cuando">{ICO["cal"]}<span>{esc(e.get("fecha"))}</span></p>
      {f'<p class="encuentro-cuando">{ICO["pin"]}<span>{esc(e["lugar"])}</span></p>' if e.get("lugar") else ""}
      <p>{esc(e.get("texto"))}</p>
      <a class="boton boton-linea" href="{esc(e["enlace"]) if e.get("enlace") else mailto(CORREO, "Inscripción: " + e.get("titulo", "encuentro gratuito"))}">{"Inscribirse" if e.get("enlace") else "Avísenme de la fecha"} {ICO["flecha"]}</a>
    </article>''' for e in ENCUENTROS)
    minimo = min((int(p["precio"]) for p in PLANES if str(p.get("precio", "")).isdigit()), default=None)

    consultas = "".join(f'''<tr><th scope="row">{esc(c.get("servicio"))}{f'<span>{esc(c["detalle"])}</span>' if c.get("detalle") else ""}</th>
      <td>{esc(c.get("precio"))}</td></tr>''' for c in CONSULTAS)

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Asociaciones Canarias",
        "description": "Asesoría, gestión y formación para asociaciones en Canarias.",
        "url": S.dominio + "/", "email": CORREO, "areaServed": "Canarias",
        "parentOrganization": {"@type": "Organization", "name": "Naroe Consulting S.L.", "url": "https://naroeconsulting.com"},
    }, ensure_ascii=False)

    hero = portada_foto("manos", "Manos de varias personas unidas sobre una mesa de trabajo")
    reunion = foto("reunion", "Grupo de personas reunidas alrededor de una mesa", "(min-width: 860px) 45vw, 92vw", "tipos-foto")
    cuerpo = f'''<section class="portada">
  <div class="contenedor portada-grid">
    <div class="portada-texto">
      <p class="antetitulo">Asesoría, gestión y formación para asociaciones</p>
      <h1>Que su asociación se dedique a <em>lo que importa</em>.</h1>
      <p class="entradilla">Ayudamos a las asociaciones de Canarias a organizarse, cumplir con sus obligaciones y profesionalizar su actividad. Desde la constitución hasta las subvenciones, la facturación o la relación con las administraciones públicas.</p>
      <div class="botones">
        <a class="boton boton-principal" href="{mailto(CORREO, "Primera orientación gratuita")}">Primera orientación gratuita {ICO["flecha"]}</a>
        <a class="boton boton-linea" href="#planes">{f"Planes desde {minimo} €/mes" if minimo else "Ver planes y precios"}</a>
      </div>
    </div>
    <div class="portada-arte{" con-foto" if hero else ""}">{hero}
      {"" if hero else '<div aria-hidden="true">' + islas() + '</div>'}
      <ul class="flotantes" aria-hidden="true">
        <li>{ICO["check"]} Estatutos al día</li><li>{ICO["check"]} Subvención justificada</li><li>{ICO["check"]} Factura en FACe</li>
      </ul>
    </div>
  </div>
</section>

<section class="seccion seccion-tipos" aria-labelledby="t-tipos">
  <div class="contenedor tipos-grid">
    <div><p class="antetitulo">Con quién trabajamos</p><h2 id="t-tipos">Asociaciones de todo tipo, en todas las islas</h2>
    <p>Muchas asociaciones hacen un trabajo social, cultural o comunitario muy importante, pero las dificultades administrativas, fiscales o de gestión les restan tiempo y energía para sus proyectos. Nuestra misión es fortalecer el tejido asociativo con servicios profesionales que les permitan centrarse en su actividad y en su impacto social.</p></div>
    <div>{reunion}<ul class="tipos">{tipos}</ul></div>
  </div>
</section>

<section class="seccion" id="servicios" aria-labelledby="t-servicios">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Servicios</p><h2 id="t-servicios">Acompañamiento integral, en cinco áreas</h2></div>
    <div class="areas">{areas}</div>
  </div>
</section>

<section class="seccion seccion-arena" id="packs" aria-labelledby="t-packs">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Packs</p><h2 id="t-packs">Para empezar, reactivar o profesionalizar</h2>
    <p class="entradilla">Trabajos cerrados, con todo lo necesario para cada momento de la asociación.</p></div>
    <div class="packs">{packs}</div>
  </div>
</section>

<section class="seccion seccion-verde" id="planes" aria-labelledby="t-planes">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Planes de asesoramiento mensual</p><h2 id="t-planes">Una cuota al mes y la gestión al día</h2>
    <p class="entradilla">Elijan el plan que encaja con el tamaño y la actividad de su asociación.</p></div>
    <ul class="planes">{planes}</ul>
    <div class="extras">
      <div><h3>Servicios sueltos</h3><p>Para lo que no entra en su plan, con precio cerrado.</p></div>
      <table class="tabla-precios"><caption class="visualmente-oculto">Precios de los servicios sueltos</caption>
      <thead><tr><th scope="col">Servicio</th><th scope="col">Precio</th></tr></thead><tbody>{extras}</tbody></table>
    </div>
    <p class="nota-precios">El Plan Semilla se paga una vez al año. Precios orientativos. Antes de empezar les preparamos un presupuesto cerrado según las necesidades de su asociación.</p>
  </div>
</section>

<section class="seccion" id="consultas" aria-labelledby="t-consultas">
  <div class="contenedor consultas-grid">
    <div><p class="antetitulo">Consultas profesionales</p><h2 id="t-consultas">¿Una duda concreta?</h2>
    <p>Para resolver una cuestión puntual sin contratar un plan. La primera orientación es gratuita, y si contratan un plan en los 30 días siguientes, les descontamos la consulta.</p>
    <a class="boton boton-principal" href="{mailto(CORREO, "Consulta profesional")}">Pedir una consulta {ICO["flecha"]}</a></div>
    <table class="tabla-precios"><caption class="visualmente-oculto">Precios de las consultas</caption>
    <thead><tr><th scope="col">Servicio</th><th scope="col">Precio</th></tr></thead><tbody>{consultas}</tbody></table>
  </div>
</section>

<section class="seccion" id="encuentros" aria-labelledby="t-encuentros">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Encuentros gratuitos</p><h2 id="t-encuentros">Aprendan con nosotros, sin coste</h2>
    <p class="entradilla">Sesiones online cada mes y encuentros presenciales por las islas, abiertos a cualquier asociación. Con tiempo para sus preguntas.</p></div>
    <div class="encuentros">{encuentros}</div>
  </div>
</section>

<section class="seccion seccion-arena" id="formacion" aria-labelledby="t-formacion">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Formación</p><h2 id="t-formacion">Talleres prácticos para asociaciones y administraciones</h2></div>
    <div class="formacion-grid">
      <article class="aparece"><h3>Para asociaciones</h3><p>Talleres para juntas directivas, equipos técnicos y personas responsables de gestión sobre:</p>{lista(TALLERES)}</article>
      <article class="aparece"><h3>Para administraciones públicas</h3><p>Diseñamos programas formativos para fortalecer el tejido asociativo local en:</p>{lista(AAPP)}</article>
    </div>
  </div>
</section>

<section class="seccion" aria-labelledby="t-porque">
  <div class="contenedor porque">
    <h2 id="t-porque">Por qué trabajar con Asociaciones Canarias</h2>
    <ol>{"".join(f"<li>{esc(x)}</li>" for x in POR_QUE)}</ol>
  </div>
</section>

<section class="seccion contacto" id="contacto" aria-labelledby="t-contacto">
  <div class="contenedor contacto-caja aparece">
    <p class="antetitulo">Contacto</p>
    <h2 id="t-contacto">Cuéntennos qué necesita su asociación</h2>
    <p>La primera orientación es gratuita. Escríbannos y les respondemos con una propuesta.</p>
    <a class="boton boton-principal" href="{mailto(CORREO, "Asociaciones Canarias: primera orientación")}">{ICO["mail"]} {CORREO}</a>
  </div>
</section>'''
    return S.pagina("Asociaciones Canarias · Asesoría, gestión y formación para asociaciones",
                    "Asesoría, gestión y formación para asociaciones de Canarias: constitución, contabilidad, subvenciones, facturación y planes mensuales. Primera orientación gratuita.",
                    "/", cuerpo, actual="", ld=ld)


def main():
    css = (RAIZ / "css/base.css").read_text(encoding="utf-8") + "\n" + (RAIZ / "css/tema.css").read_text(encoding="utf-8")
    S.escribir("css/estilos.css", css)
    S.publicar({"index.html": inicio()})


if __name__ == "__main__":
    main()
