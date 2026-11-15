(() => {
const N = ' ', Q = '’';
const css = `
.gfp4-titre{text-align:center;margin:0 auto 6px}
.gfp4-sous{text-align:center;font-size:17px;line-height:1.5;margin:0 auto 22px;max-width:640px}
.gfp4-pied{text-align:center;font-size:14px;margin:14px 0 0}
/* A : deux cartes */
.gfp4A{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;max-width:900px;margin:0 auto;align-items:stretch}
.gfp4A-cab{background:#f2ece1;border-radius:20px;padding:24px;min-width:0}
.gfp4A-cab h3,.gfp4A-pro h3{font-size:15px;font-family:Figtree,sans-serif;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin:0 0 14px}
.gfp4A-cab h3{color:var(--ts)}
.gfp4A-l{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid #e0d7c6;font-size:16px}
.gfp4A-l b{white-space:nowrap}
.gfp4A-tot{display:flex;justify-content:space-between;gap:12px;padding:14px 0 0;font:600 22px/1.2 Fraunces,serif}
.gfp4A-sans{font-size:15px;line-height:1.45;margin:12px 0 0}
.gfp4A-pro{background:var(--ts);color:var(--cr);border-radius:20px;padding:24px;min-width:0}
.gfp4A-pro h3{color:var(--cr)}
.gfp4A-prix{font:600 46px/1 Fraunces,serif;margin:0 0 4px}
.gfp4A-prix small{font:500 16px/1 Figtree,sans-serif}
.gfp4A-pro ul{list-style:none;padding:0;margin:14px 0 18px}
.gfp4A-pro li{position:relative;padding:5px 0 5px 24px;font-size:16px;line-height:1.4}
.gfp4A-pro li:before{content:"";position:absolute;left:2px;top:11px;width:10px;height:6px;border-left:2px solid var(--cr);border-bottom:2px solid var(--cr);transform:rotate(-45deg)}
.gfp4A-pro .gfp-btn{width:100%}
/* B : tableau comparatif */
.gfp4B{max-width:900px;margin:0 auto;border-radius:20px;overflow:hidden;border:1px solid var(--tc)}
.gfp4B-r{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr);background:var(--cr)}
.gfp4B-r>div{padding:13px 16px;font-size:16px;line-height:1.4;border-top:1px solid #e0d7c6;min-width:0}
.gfp4B-r>div:first-child{font-weight:700}
.gfp4B-r>div:last-child{background:#f6eee6}
.gfp4B-h>div{border-top:0;font:700 14px/1.2 Figtree,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ts)}
.gfp4B-h>div:last-child{background:var(--ts);color:var(--cr)}
.gfp4B-p>div{font:600 22px/1.2 Fraunces,serif}
.gfp4B-p>div:first-child{font:700 16px/1.4 Figtree,sans-serif}
.gfp4B-cta{text-align:center;margin:20px 0 0}
@media (max-width:749px){
 .gfp4-sous{font-size:16px;margin-bottom:14px}
 .gfp4A{grid-template-columns:minmax(0,1fr);gap:10px}
 .gfp4A-cab,.gfp4A-pro{padding:16px 14px}
 .gfp4A-prix{font-size:38px}
 .gfp4B-r{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
 .gfp4B-r>div:first-child{grid-column:1/-1;padding:10px 12px 0;border-top:1px solid #e0d7c6;font-size:15px}
 .gfp4B-r>div{padding:6px 12px 10px;font-size:15px;border-top:0}
 .gfp4B-h>div:first-child{display:none}
 .gfp4B-h>div{padding:10px 12px}
 .gfp4B-cta .gfp-btn{width:100%}
}`;
const titre = 'Ce que le même parcours coûte en cabinet';
const sous = 'Un bilan d' + Q + 'une heure, puis deux séances de suivi. C' + Q + 'est le parcours habituel. Voici ce qu' + Q + 'il coûte, et ce qu' + Q + 'il ne comprend pas.';
const sans = 'Sans les outils, sans les recettes, et sans personne entre les rendez-vous.';
const pied = 'Prix TTC, payé une fois. Ce n' + Q + 'est pas un abonnement.';
const inclus = ['Votre bilan écrit, à son nom', 'L' + Q + 'analyse d' + Q + 'une vidéo', 'Vos questions par e-mail pendant 90' + N + 'jours', 'Le manuel, 30 recettes, la feuille de route et le carnet', 'Le coffret de trois accessoires'];
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s4="A">Section 4, variante A : deux cartes, le cabinet et le Programme</div>
<div class="gfp-cap gfp-cap--creme" data-s4="A"><h2 class="gfp4-titre">${titre}</h2><p class="gfp4-sous">${sous}</p>
<div class="gfp4A"><div class="gfp4A-cab"><h3>En cabinet</h3>
<div class="gfp4A-l"><span>Un bilan comportemental d${Q}une heure</span><b>environ 110${N}€</b></div>
<div class="gfp4A-l"><span>Deux séances de suivi</span><b>environ 145${N}€</b></div>
<div class="gfp4A-tot"><span>Total</span><span>environ 255${N}€</span></div><p class="gfp4A-sans">${sans}</p></div>
<div class="gfp4A-pro"><h3>Le Programme du Foyer Apaisé</h3><p class="gfp4A-prix">179${N}€ <small>· 90${N}jours</small></p>
<ul>${inclus.map(x => `<li>${x}</li>`).join('')}</ul><a class="gfp-btn" href="#">Être prévenu de l${Q}ouverture</a></div></div>
<p class="gfp4-pied">${pied}</p></div>`;
const R = [
 ['Le bilan', 'Une heure, à l' + Q + 'oral', 'Écrit, à son nom, à relire'],
 ['Entre les rendez-vous', 'Personne', 'Vos questions par e-mail, réponse sous 48' + N + 'h ouvrées'],
 ['Les outils', 'À acheter à part', 'Le coffret et la méthode écrite'],
];
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s4="B">Section 4, variante B : tableau comparatif ligne à ligne</div>
<div class="gfp-cap gfp-cap--creme" data-s4="B"><h2 class="gfp4-titre">${titre}</h2><p class="gfp4-sous">${sous}</p>
<div class="gfp4B"><div class="gfp4B-r gfp4B-h"><div>&nbsp;</div><div>En cabinet</div><div>Le Programme</div></div>
${R.map(r => `<div class="gfp4B-r"><div>${r[0]}</div><div>${r[1]}</div><div>${r[2]}</div></div>`).join('')}
<div class="gfp4B-r gfp4B-p"><div>Le prix</div><div>environ 255${N}€</div><div>179${N}€</div></div></div>
<div class="gfp4B-cta"><a class="gfp-btn" href="#">Être prévenu de l${Q}ouverture</a></div><p class="gfp4-pied">${pied}</p></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
localStorage.setItem('gfp-maquette', document.querySelector('#MainContent').innerHTML);
g.querySelectorAll('[data-s4="B"]').forEach(e => e.remove());
document.title = 'Section 4 : variante A';
g.querySelector('[data-s4="A"]').scrollIntoView();
return document.documentElement.scrollWidth;
})()
