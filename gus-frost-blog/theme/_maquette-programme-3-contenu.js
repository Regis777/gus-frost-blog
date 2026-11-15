(() => {
const N = ' ', Q = '’';
const CDN = 'https://cdn.shopify.com/s/files/1/0614/7119/5357/files/';
const IM = { lech: CDN + 'hero-tapis-lechage-apaiser-chien.png?width=700', fouil: CDN + 'hero-tapis-fouille-chien.png?width=700', carnet: CDN + 'hero-suivre-progres-chien-anxieux.png?width=700' };
const css = `
.gfp-cap--sauge .gfp-card{background:var(--cr)}
.gfp-card{border-radius:16px;padding:18px;min-width:0}
.gfp-card h3{font-size:20px;margin:0 0 8px}
.gfp-card p{font-size:16px;line-height:1.5;margin:0}
.gfp-num{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:var(--ts);color:var(--cr);font:600 16px/1 Fraunces,serif;margin:0 0 10px}
.gfp-duree{margin:18px 0 0;padding:16px 18px;border-radius:16px;background:var(--ts);color:var(--cr);font:500 17px/1.45 Figtree,sans-serif}
.gfp-duree strong{font-weight:700}
.gfp-intro{font-size:17px;line-height:1.5;margin:0 0 20px;max-width:760px}
/* A : grille de cinq cartes */
.gfp3A{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px}
.gfp3A .gfp-card{grid-column:span 2}
.gfp3A .gfp-card:nth-child(4),.gfp3A .gfp-card:nth-child(5){grid-column:span 3}
.gfp3A-photos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:12px 0 0}
.gfp3A-photos img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:12px;display:block}
/* B : deux colonnes, accompagnement / ce que vous recevez */
.gfp3B{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
.gfp3B-col{background:var(--cr);border-radius:20px;padding:22px;min-width:0}
.gfp3B-col h3.gfp-col-t{font-size:15px;font-family:Figtree,sans-serif;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ts);margin:0 0 14px}
.gfp3B-it{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;padding:14px 0;border-top:1px solid var(--tc)}
.gfp3B-it:first-of-type{border-top:0;padding-top:0}
.gfp3B-it .gfp-num{margin:0}
.gfp3B-it h4{font:600 19px/1.25 Fraunces,serif;color:var(--vf);margin:4px 0 6px}
.gfp3B-it p{font-size:16px;line-height:1.5;margin:0}
.gfp3B-it img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px;display:block;margin:10px 0 0}
@media (max-width:749px){
 .gfp3A{grid-template-columns:minmax(0,1fr);gap:10px}
 .gfp3A .gfp-card,.gfp3A .gfp-card:nth-child(4),.gfp3A .gfp-card:nth-child(5){grid-column:auto}
 .gfp-card{padding:14px}
 .gfp-card h3{font-size:18px}
 .gfp-intro{font-size:16px;margin-bottom:14px}
 .gfp-duree{font-size:16px;padding:14px}
 .gfp3B{grid-template-columns:minmax(0,1fr);gap:10px}
 .gfp3B-col{padding:16px 14px}
 .gfp3B-it{gap:12px}
}`;
const titre = 'Ce que comprend le Programme';
const intro = 'Tout part d' + Q + 'un bilan écrit pour votre chien, pas pour un chien moyen. Le reste sert à le tenir jusqu' + Q + 'au bout.';
const C = [
 ['Votre bilan écrit, à son nom', 'Après votre commande, vous recevez un questionnaire détaillé sur votre chien, votre foyer et les situations qui déclenchent le stress. Votre bilan écrit vous est adressé habituellement sous 72' + N + 'h, et au plus tard sous 7' + N + 'jours ouvrés à compter de la réception de votre questionnaire.'],
 ['L' + Q + 'analyse d' + Q + 'une vidéo de votre chien', 'Vous filmez deux minutes de la situation qui coince' + N + ': le départ, l' + Q + 'orage, le retour du soir. Je la regarde et je vous réponds par écrit.'],
 ['Vos questions par e-mail, pendant 90' + N + 'jours', 'Autant de questions qu' + Q + 'il vous en faut, réponse sous 48' + N + 'h ouvrées. C' + Q + 'est la partie qui empêche l' + Q + 'abandon.'],
 ['La méthode écrite', 'Le manuel du Foyer Apaisé, 30 recettes classées par besoin et par moment, la feuille de route jour par jour, et le carnet de bord qui vous fait tenir.'],
 ['Le coffret d' + Q + 'accessoires, expédié chez vous', 'Un tapis de léchage, l' + Q + 'outil du calme. Un tapis de fouille, celui de la dépense mentale. Un jouet de mastication. Son expédition suit notre Politique d' + Q + 'expédition, et le délai de votre bilan ne dépend pas de l' + Q + 'arrivée du colis.'],
];
const duree = '<strong>90' + N + 'jours à compter de l' + Q + 'envoi de votre bilan.</strong> Vous disposez de six mois après votre commande pour renvoyer votre questionnaire' + N + ': rien ne se périme si vous démarrez plus tard.';
const card = (c, i, extra = '') => `<div class="gfp-card"><span class="gfp-num">${i + 1}</span><h3>${c[0]}</h3><p>${c[1]}</p>${extra}</div>`;
const photos = `<div class="gfp3A-photos"><img src="${IM.lech}" alt=""><img src="${IM.fouil}" alt=""></div>`;
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s3="A">Section 3, variante A : cinq cartes sur fond sauge</div>
<div class="gfp-cap gfp-cap--sauge" data-s3="A"><h2>${titre}</h2><p class="gfp-intro">${intro}</p>
<div class="gfp3A">${C.map((c, i) => card(c, i, i === 4 ? photos : i === 3 ? `<div class="gfp3A-photos" style="grid-template-columns:minmax(0,1fr)"><img src="${IM.carnet}" alt="" style="aspect-ratio:16/7"></div>` : '')).join('')}</div><p class="gfp-duree">${duree}</p></div>`;
const it = (c, i, img = '') => `<div class="gfp3B-it"><span class="gfp-num">${i + 1}</span><div><h4>${c[0]}</h4><p>${c[1]}</p>${img}</div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s3="B">Section 3, variante B : deux colonnes, l${Q}accompagnement et ce que vous recevez</div>
<div class="gfp-cap gfp-cap--sauge" data-s3="B"><h2>${titre}</h2><p class="gfp-intro">${intro}</p>
<div class="gfp3B"><div class="gfp3B-col"><h3 class="gfp-col-t">L${Q}accompagnement</h3>${C.slice(0, 3).map((c, i) => it(c, i)).join('')}</div>
<div class="gfp3B-col"><h3 class="gfp-col-t">Ce que vous recevez</h3>${it(C[3], 3, `<img src="${IM.carnet}" alt="">`)}${it(C[4], 4, `<img src="${IM.lech}" alt="">`)}</div></div>
<p class="gfp-duree">${duree}</p></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
localStorage.setItem('gfp-maquette', document.querySelector('#MainContent').innerHTML);
g.querySelectorAll('[data-s3="B"]').forEach(e => e.remove());
document.title = 'Section 3 : variante A';
g.querySelector('[data-s3="A"]').scrollIntoView();
return document.documentElement.scrollWidth;
})()
