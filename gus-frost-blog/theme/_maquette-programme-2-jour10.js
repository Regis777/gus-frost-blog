(() => {
const N = ' ';
const IMG = 'https://cdn.shopify.com/s/files/1/0614/7119/5357/files/hero-chien-anxieux-comprendre-apaiser.png?width=900';
const css = `
.gfp h2{font-family:Fraunces,serif;font-weight:600;color:var(--vf);font-size:clamp(24px,2.6vw,36px);line-height:1.15;margin:0 0 14px}
.gfp h3{font-family:Fraunces,serif;font-weight:600;color:var(--vf);font-size:22px;line-height:1.2;margin:0 0 10px}
.gfp p.gfp-p{font-size:17px;line-height:1.55;margin:0 0 12px}
.gfp-cap{max-width:1220px;margin:0 auto;border-radius:26px;padding:40px 44px}
.gfp-cap--sauge{background:var(--sg)}
.gfp-cap--creme{background:var(--cr);border:1px solid var(--tc)}
/* A : sauge, texte + 3 cartes jour */
.gfp2A{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:36px;align-items:start}
.gfp2A-jours{display:grid;gap:12px}
.gfp-jour{background:var(--cr);border-radius:16px;padding:16px 18px;display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;align-items:center}
.gfp-jour b{display:inline-flex;align-items:center;justify-content:center;min-width:76px;height:44px;border-radius:12px;background:var(--ts);color:var(--cr);font:600 16px/1 Fraunces,serif}
.gfp-jour span{font-size:16px;line-height:1.4}
.gfp-chute{margin:18px 0 0;padding:16px 18px;border-radius:16px;background:var(--ts);color:var(--cr);font:500 18px/1.45 Figtree,sans-serif}
/* B : creme, photo + texte, frise horizontale */
.gfp2B-haut{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:36px;align-items:center}
.gfp2B-haut img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:18px;display:block}
.gfp2B-frise{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin:30px 0 0;padding:26px 0 0}
.gfp2B-frise:before{content:"";position:absolute;left:0;right:0;top:0;border-top:2px solid var(--tc)}
.gfp2B-frise div{position:relative}
.gfp2B-frise div:before{content:"";position:absolute;top:-33px;left:0;width:12px;height:12px;border-radius:50%;background:var(--ts)}
.gfp2B-frise b{display:block;font:600 20px/1.2 Fraunces,serif;color:var(--ts);margin:0 0 6px}
.gfp2B-frise span{font-size:16px;line-height:1.45}
@media (max-width:749px){
 .gfp-cap{padding:20px 16px;border-radius:20px}
 .gfp h2{font-size:22px}
 .gfp h3{font-size:19px}
 .gfp p.gfp-p{font-size:16px;line-height:1.5}
 .gfp2A,.gfp2B-haut{grid-template-columns:minmax(0,1fr);gap:16px}
 .gfp-jour{padding:12px;gap:12px}
 .gfp-jour b{min-width:64px;height:40px;font-size:15px}
 .gfp-chute{font-size:16px;padding:14px}
 .gfp2B-haut img{aspect-ratio:16/10}
 .gfp2B-frise{grid-template-columns:minmax(0,1fr);gap:14px;margin-top:20px;padding:0 0 0 22px}
 .gfp2B-frise:before{top:4px;bottom:4px;left:5px;right:auto;border-top:0;border-left:2px solid var(--tc)}
 .gfp2B-frise div:before{top:5px;left:-22px}
}`;
const t1 = 'Ce n’est jamais l’objet qui échoue. C’est la suite.';
const p1 = 'Vous avez déjà essayé. Un tapis, un diffuseur, plus de balades, peut-être même une consultation. Pendant trois jours, ça allait mieux. Puis la semaine a repris, un soir vous avez sauté l’étape, le lendemain aussi, et au bout de dix jours l’objet était au fond du placard.';
const p2 = '<strong>Ce n’est pas un manque de volonté.</strong> C’est ce qui arrive à presque tout le monde quand personne ne vient voir où vous en êtes.';
const t2 = 'Une séance donne des consignes. Elle ne vous accompagne pas.';
const J = [['Jour 4', 'Votre chien régresse, et vous ne savez pas si c’est normal.'],
           ['Jour 9', 'Vous n’avez plus le temps, et personne ne le remarque.'],
           ['Jour 21', 'Ça marche, et vous ne savez pas quoi faire ensuite.']];
const chute = 'Le Programme est construit autour de ces moments' + N + ': non pas vous expliquer quoi faire, mais faire en sorte que vous le fassiez pendant 90' + N + 'jours.';
const A = `<div class="gfp-lbl" style="margin-top:34px">Section 2, variante A : capsule sauge, les trois jours en cartes</div>
<div class="gfp-cap gfp-cap--sauge"><div class="gfp2A"><div><h2>${t1}</h2><p class="gfp-p">${p1}</p><p class="gfp-p">${p2}</p></div>
<div><h3>${t2}</h3><div class="gfp2A-jours">${J.map(j => `<div class="gfp-jour"><b>${j[0].replace(' ', N)}</b><span>${j[1]}</span></div>`).join('')}</div><p class="gfp-chute">${chute}</p></div></div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px">Section 2, variante B : capsule crème, photo et frise</div>
<div class="gfp-cap gfp-cap--creme"><div class="gfp2B-haut"><img src="${IMG}" alt=""><div><h2>${t1}</h2><p class="gfp-p">${p1}</p><p class="gfp-p">${p2}</p></div></div>
<h3 style="margin-top:28px">${t2}</h3><div class="gfp2B-frise">${J.map(j => `<div><b>${j[0].replace(' ', N)}</b><span>${j[1]}</span></div>`).join('')}</div><p class="gfp-chute">${chute}</p></div>`;
document.getElementById('gfp-ov')?.remove();
const g = document.querySelector('.gfp');
g.querySelectorAll('.gfp-lbl')[0].remove(); g.querySelector('.gfpA').remove();
g.querySelector('.gfp-lbl').textContent = 'Section 1 retenue : ouverture B';
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
return g.children.length;
})()
