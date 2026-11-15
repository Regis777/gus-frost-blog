(() => {
const N = ' ', Q = '’';
const IMG = 'https://cdn.shopify.com/s/files/1/0614/7119/5357/articles/hero-chien-dort.png?width=900';
const css = `
.gfp6-transp{background:var(--sg);border-radius:16px;padding:16px 18px;font-size:16px;line-height:1.5;margin:0 0 16px}
.gfp6-transp strong{display:block;font:600 18px/1.3 Fraunces,serif;margin:0 0 4px}
.gfp6-cit{font:italic 500 21px/1.45 Fraunces,serif;color:var(--vf);margin:0;padding:0 0 0 18px;border-left:3px solid var(--tc)}
.gfp6-gf{font-size:15px;line-height:1.5;margin:14px 0 0}
/* A : faits en cartes + citation */
.gfp6A{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;align-items:start}
.gfp6A-faits{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.gfp6A-faits div{background:#f2ece1;border-radius:14px;padding:14px;min-width:0}
.gfp6A-faits b{display:block;font:600 26px/1.1 Fraunces,serif;color:var(--ts);margin:0 0 4px}
.gfp6A-faits span{font-size:15px;line-height:1.4}
/* B : photo + texte */
.gfp6B{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:36px;align-items:center}
.gfp6B img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:18px;display:block}
.gfp6B p.gfp-p{margin:0 0 12px}
@media (max-width:749px){
 .gfp6A,.gfp6B{grid-template-columns:minmax(0,1fr);gap:16px}
 .gfp6A-faits b{font-size:22px}
 .gfp6-cit{font-size:18px;padding-left:14px}
 .gfp6B img{aspect-ratio:16/10;order:-1}
 .gfp6-transp{padding:14px}
}`;
const titre = 'Qui vous accompagne';
const transp = '<strong>Le métier n' + Q + 'est pas réglementé en France.</strong>N' + Q + 'importe qui peut se dire comportementaliste. C' + Q + 'est pour cela que nous vous disons exactement qui accompagne votre chien, et vous laissons juger.';
const qui = 'Un comportementaliste qui exerce depuis vingt ans, majoritairement en cabinet, au Canada, à recevoir des chiens et des chats. Ces dernières années, il s' + Q + 'est concentré sur un seul sujet' + N + ': la gestion du stress chez le chien. Il est titulaire de l' + Q + 'ACACED, l' + Q + 'attestation de connaissances pour les animaux de compagnie.';
const cit = '«' + N + 'En cabinet, je voyais le même mur revenir' + N + ': une heure de consultation, des consignes justes, et un foyer qui abandonne au bout de dix jours parce que personne n' + Q + 'est là entre les rendez-vous. Ce programme est ma réponse.' + N + '»';
const gf = 'Gus était un chien. Frost était un chat. C' + Q + 'est leur nom qui est sur cette boutique.';
const F = [['20' + N + 'ans', 'de pratique, surtout en cabinet, au Canada'], ['Chiens et chats', 'reçus en consultation'], ['Le stress', 'du chien, sa spécialité ces dernières années'], ['ACACED', 'attestation de connaissances obtenue']];
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s6="A">Section 6, variante A : les faits en quatre cartes, puis la citation</div>
<div class="gfp-cap gfp-cap--creme" data-s6="A"><div class="gfp6A"><div><h2>${titre}</h2><p class="gfp6-transp">${transp}</p>
<div class="gfp6A-faits">${F.map(f => `<div><b>${f[0]}</b><span>${f[1]}</span></div>`).join('')}</div></div>
<div><p class="gfp6-cit">${cit}</p><p class="gfp6-gf">${gf}</p></div></div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s6="B">Section 6, variante B : un texte suivi, une photo de la banque</div>
<div class="gfp-cap gfp-cap--creme" data-s6="B"><div class="gfp6B"><div><h2>${titre}</h2><p class="gfp6-transp">${transp}</p><p class="gfp-p">${qui}</p><p class="gfp6-cit">${cit}</p><p class="gfp6-gf">${gf}</p></div>
<img src="${IMG}" alt=""></div></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
localStorage.setItem('gfp-maquette', document.querySelector('#MainContent').innerHTML);
g.querySelectorAll('[data-s6="B"]').forEach(e => e.remove());
document.title = 'Section 6 : variante A';
g.querySelector('[data-s6="A"]').scrollIntoView();
return document.documentElement.scrollWidth;
})()
