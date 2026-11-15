(() => {
const N = ' ';
const IMG_A = 'https://cdn.shopify.com/s/files/1/0614/7119/5357/articles/hero-maison-apaisante.png?width=1100';
const IMG_B = 'https://cdn.shopify.com/s/files/1/0614/7119/5357/articles/hero-maison-apaisante.png?width=1800';
const css = `
.gfp{--vf:#314431;--bg:#efe7da;--cr:#faf8f3;--tc:#c16b47;--ts:#a8522f;--sg:#b6bfa3;--cta:#c6efa3;background:var(--bg);padding:28px 16px;font-family:Figtree,sans-serif;color:var(--vf)}
.gfp *{box-sizing:border-box}
.gfp-lbl{max-width:1220px;margin:0 auto 10px;font:600 13px/1 Figtree,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--ts)}
.gfp-sur{display:inline-block;background:var(--ts);color:var(--cr);font:600 13px/1.2 Figtree,sans-serif;padding:7px 12px;border-radius:999px;margin:0 0 14px}
.gfp h1{font-family:Fraunces,serif;font-weight:600;color:var(--vf);font-size:clamp(28px,3.4vw,46px);line-height:1.12;margin:0 0 14px;letter-spacing:-.01em}
.gfp-sous{font-size:18px;line-height:1.5;margin:0 0 18px;opacity:1}
.gfp-prix{font:600 20px/1.2 Fraunces,serif;margin:0 0 16px}
.gfp-prix span{font:500 15px/1.2 Figtree,sans-serif;opacity:.9}
.gfp-btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:12px 22px;background:var(--cta);color:var(--vf);border:2px solid var(--vf);border-radius:10px;font:700 17px/1.2 Figtree,sans-serif;text-decoration:none;cursor:pointer}
.gfp-note{font-size:14px;line-height:1.45;margin:10px 0 0}
.gfp-reas{display:flex;flex-wrap:wrap;gap:8px 18px;margin:18px 0 0;padding:14px 0 0;border-top:1px solid var(--tc);font-size:14px}
.gfp-reas b{color:var(--ts)}
/* A */
.gfpA{max-width:1220px;margin:0 auto;background:var(--cr);border:1px solid var(--tc);border-radius:26px;overflow:hidden;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr)}
.gfpA-txt{padding:44px 44px 36px;min-width:0}
.gfpA-img{min-width:0;min-height:100%}
.gfpA-img img{width:100%;height:100%;object-fit:cover;display:block}
/* B */
.gfpB{max-width:1220px;margin:0 auto;position:relative;border-radius:26px;overflow:hidden;min-height:560px;display:flex;align-items:center}
.gfpB>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:70% 50%}
.gfpB-card{position:relative;margin:36px;max-width:560px;background:var(--cr);border:1px solid var(--tc);border-radius:20px;padding:30px 30px 26px;min-width:0}
.gfpB-form{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin:0}
.gfpB-form input{min-height:48px;border:2px solid var(--vf);border-radius:10px;padding:0 14px;font:16px Figtree,sans-serif;background:#fff8;color:var(--vf);min-width:0}
@media (max-width:749px){
 .gfp{padding:14px 12px}
 .gfpA{grid-template-columns:minmax(0,1fr)}
 .gfpA-img{order:-1;height:220px}
 .gfpA-txt{padding:20px 16px 18px}
 .gfp h1{font-size:27px}
 .gfp-sous{font-size:16px;margin-bottom:14px}
 .gfp-btn{width:100%}
 .gfpB{display:block;min-height:0;background:var(--cr);border:1px solid var(--tc)}
 .gfpB>img{position:static;height:220px}
 .gfpB-card{margin:0;border:0;border-radius:0;padding:20px 16px 18px;max-width:none}
 .gfpB-form{grid-template-columns:minmax(0,1fr)}
}`;
const sur = 'Accompagnement de 90' + N + 'jours · pour les chiens';
const h1 = 'Votre chien ne se calmera pas parce que vous avez acheté le bon objet.';
const sous = 'Il se calmera parce que quelqu’un vous aura suivi assez longtemps pour que ça tienne. Un bilan écrit à son nom, l’analyse d’une vidéo, et vos questions par e-mail pendant 90' + N + 'jours.';
const prix = '179' + N + '€ <span>· ouverture prochaine</span>';
const note = 'Inscription gratuite, sans engagement. Dès que vous confirmez votre adresse, vous recevez le guide «' + N + 'Les 5 erreurs qui aggravent le stress de votre chien' + N + '».';
const reas = '<div class="gfp-reas"><span><b>Bilan</b> sous 72' + N + 'h</span><span><b>Réponse</b> sous 48' + N + 'h ouvrées</span><span><b>Garantie</b> de remboursement</span></div>';
const A = `<div class="gfp-lbl">Variante A : photo à droite, bouton vers l’inscription</div>
<div class="gfpA"><div class="gfpA-txt"><span class="gfp-sur">${sur}</span><h1>${h1}</h1><p class="gfp-sous">${sous}</p><p class="gfp-prix">${prix}</p><a class="gfp-btn" href="#">Être prévenu de l’ouverture</a><p class="gfp-note">${note}</p>${reas}</div>
<div class="gfpA-img"><img src="${IMG_A}" alt=""></div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px">Variante B : grande photo, inscription directement dans l’ouverture</div>
<div class="gfpB"><img src="${IMG_B}" alt=""><div class="gfpB-card"><span class="gfp-sur">${sur}</span><h1>${h1}</h1><p class="gfp-sous">${sous}</p><p class="gfp-prix">${prix}</p><form class="gfpB-form" onsubmit="return false"><input type="email" placeholder="Votre adresse e-mail"><button class="gfp-btn" type="submit">Être prévenu</button></form><p class="gfp-note">${note}</p></div></div>`;
const main = document.querySelector('#MainContent');
main.innerHTML = `<style>${css}</style><div class="gfp">${A}${B}</div>`;
window.scrollTo(0,0);
return main.querySelectorAll('.gfp img').length;
})()
