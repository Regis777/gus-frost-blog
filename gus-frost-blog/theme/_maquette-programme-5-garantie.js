(() => {
const N = ' ', Q = '’';
const css = `
.gfp5-contrat{background:var(--cr);border-radius:16px;padding:18px 20px;font-size:16px;line-height:1.55;margin:0}
.gfp5-contrat a{color:var(--ts);font-weight:600}
.gfp5-pq{font-size:16px;line-height:1.5;margin:14px 0 0}
/* A : sceau + texte */
.gfp5A{display:grid;grid-template-columns:auto minmax(0,1fr);gap:36px;align-items:center}
.gfp5A-sceau{width:190px;height:190px;border-radius:50%;background:var(--ts);color:var(--cr);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 0 0 6px var(--sg),0 0 0 8px var(--ts)}
.gfp5A-sceau b{font:600 64px/1 Fraunces,serif}
.gfp5A-sceau span{font:600 14px/1.25 Figtree,sans-serif;letter-spacing:.05em;text-transform:uppercase;max-width:130px;margin-top:4px}
/* B : trois étapes */
.gfp5B-et{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0 0 14px}
.gfp5B-et div{background:var(--cr);border-radius:16px;padding:16px;min-width:0}
.gfp5B-et b{display:block;font:600 19px/1.25 Fraunces,serif;color:var(--vf);margin:8px 0 6px}
.gfp5B-et p{font-size:15px;line-height:1.45;margin:0}
.gfp5B details{background:var(--cr);border-radius:16px;padding:14px 18px}
.gfp5B summary{cursor:pointer;font-weight:700;color:var(--ts)}
.gfp5B details p{font-size:15px;line-height:1.55;margin:10px 0 0}
@media (max-width:749px){
 .gfp5A{grid-template-columns:minmax(0,1fr);gap:16px;justify-items:center}
 .gfp5A-sceau{width:140px;height:140px}
 .gfp5A-sceau b{font-size:46px}
 .gfp5A-sceau span{font-size:12px}
 .gfp5A>div:last-child{justify-self:stretch}
 .gfp5-contrat{padding:14px;font-size:15px}
 .gfp5B-et{grid-template-columns:minmax(0,1fr);gap:8px}
 .gfp5B-et div{padding:12px 14px}
}`;
const titre = 'Trente jours de carnet. Si rien ne bouge, vous êtes remboursé.';
const contrat = 'Si, après avoir suivi le Programme et rempli votre carnet de bord pendant trente (30) jours consécutifs, vous ne constatez aucune évolution, le prix vous est intégralement remboursé sur simple demande adressée à <a href="mailto:contact@gusetfrost.fr">contact@gusetfrost.fr</a>, accompagnée du carnet renseigné. Vous conservez alors le coffret et l' + Q + 'ensemble des supports remis. Cette garantie ne restreint ni votre droit de rétractation, ni les garanties légales.';
const pq = 'Pourquoi le carnet' + N + '? Parce qu' + Q + 'il montre ce qui a été fait, jour après jour. C' + Q + 'est aussi lui qui vous fait tenir les semaines où l' + Q + 'envie retombe.';
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s5="A">Section 5, variante A : un sceau « 30 jours » et le texte de la garantie</div>
<div class="gfp-cap gfp-cap--sauge" data-s5="A"><div class="gfp5A"><div class="gfp5A-sceau"><b>30</b><span>jours de carnet ou remboursé</span></div>
<div><h2>${titre}</h2><p class="gfp5-contrat">${contrat}</p><p class="gfp5-pq">${pq}</p></div></div></div>`;
const E = [
 ['Vous tenez votre carnet', 'Trente jours consécutifs, en suivant le Programme.'],
 ['Aucune évolution' + N + '?', 'Vous écrivez à contact@gusetfrost.fr, avec le carnet renseigné.'],
 ['Vous êtes remboursé', 'Intégralement. Vous conservez le coffret et tous les supports.'],
];
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s5="B">Section 5, variante B : la garantie en trois étapes, le texte complet à déplier</div>
<div class="gfp-cap gfp-cap--sauge gfp5B" data-s5="B"><h2>${titre}</h2>
<div class="gfp5B-et">${E.map((e, i) => `<div><span class="gfp-num" style="margin:0">${i + 1}</span><b>${e[0]}</b><p>${e[1]}</p></div>`).join('')}</div>
<details><summary>Le texte exact de la garantie</summary><p>${contrat}</p></details><p class="gfp5-pq">${pq}</p></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
localStorage.setItem('gfp-maquette', document.querySelector('#MainContent').innerHTML);
g.querySelectorAll('[data-s5="B"]').forEach(e => e.remove());
document.title = 'Section 5 : variante A';
g.querySelector('[data-s5="A"]').scrollIntoView();
return document.documentElement.scrollWidth;
})()
