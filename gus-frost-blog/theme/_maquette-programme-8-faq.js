(() => {
const N = ' ', Q = '’';
const css = `
.gfp8A{display:grid;gap:10px;max-width:900px;margin:0 auto}
.gfp8A details{background:#f2ece1;border-radius:14px;padding:0;border-left:3px solid transparent}
.gfp8A details[open]{background:var(--cr);border-left-color:var(--ts)}
.gfp8A summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:center;padding:14px 16px;font:600 17px/1.35 Figtree,sans-serif;color:var(--vf)}
.gfp8A summary::-webkit-details-marker{display:none}
.gfp8A summary:before{content:"?";display:flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;border:2px solid var(--tc);color:var(--tc);font:700 14px/1 Figtree,sans-serif}
.gfp8A summary:after{content:"";width:9px;height:9px;border-right:2px solid var(--tc);border-bottom:2px solid var(--tc);transform:rotate(45deg);margin:0 4px 4px 0}
.gfp8A details[open] summary:after{transform:rotate(-135deg);margin:4px 4px 0 0}
.gfp8A details p{margin:0;padding:0 16px 16px 54px;font-size:16px;line-height:1.55}
.gfp8B{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.gfp8B div{background:#f2ece1;border-radius:14px;padding:16px 18px;min-width:0}
.gfp8B h3{font:600 18px/1.3 Fraunces,serif;color:var(--vf);margin:0 0 6px}
.gfp8B p{font-size:15px;line-height:1.5;margin:0}
.gfp8 a{color:var(--ts);font-weight:600}
@media (max-width:749px){
 .gfp8A summary{padding:12px;font-size:16px;gap:10px}
 .gfp8A details p{padding:0 12px 14px 12px;font-size:15px}
 .gfp8B{grid-template-columns:minmax(0,1fr);gap:8px}
 .gfp8B div{padding:14px}
}`;
const F = [
 ['Est-ce un abonnement' + N + '?', 'Non. Le Programme dure 90' + N + 'jours, payés une fois.'],
 ['Mon chien est âgé, craintif ou adopté. Est-il concerné' + N + '?', 'C' + Q + 'est l' + Q + 'objet du bilan de départ' + N + ': il est écrit pour votre chien, pas pour un chien moyen. Si votre situation relève d' + Q + 'un vétérinaire, nous vous le dirons.'],
 ['Combien de temps cela prend-il par jour' + N + '?', 'Une dizaine de minutes. Le Programme est pensé pour des gens qui travaillent.'],
 ['Quand commencent les 90' + N + 'jours' + N + '?', 'À l' + Q + 'envoi de votre bilan. Vous avez six mois après votre commande pour renvoyer votre questionnaire.'],
 ['Quand le coffret arrive-t-il' + N + '?', 'Il est expédié selon notre <a href="/policies/shipping-policy">Politique d' + Q + 'expédition</a>. Votre bilan n' + Q + 'attend pas le colis' + N + ': vous commencez à sa lecture.'],
 ['Puis-je me rétracter' + N + '?', 'Oui. Avant de payer, vous acceptez que l' + Q + 'accompagnement démarre tout de suite. Si vous vous rétractez ensuite, seule la part déjà fournie reste due, et vous renvoyez le coffret. La garantie de 30' + N + 'jours va plus loin.'],
 ['Le Programme existe-t-il pour les chats' + N + '?', 'Pas encore. Il est conçu pour les chiens. Un programme pour les chats viendra plus tard.'],
 ['À quoi est-ce que je m' + Q + 'inscris, exactement' + N + '?', 'À une liste d' + Q + 'attente. Une fois votre adresse confirmée, vous recevez le guide «' + N + 'Les 5 erreurs qui aggravent le stress de votre chien' + N + '», puis un e-mail à l' + Q + 'ouverture. Vous décidez à ce moment-là.'],
 ['Allez-vous m' + Q + 'envoyer beaucoup d' + Q + 'e-mails' + N + '?', 'Non. Le guide, quelques e-mails courts, un par semaine au plus, et l' + Q + 'annonce de l' + Q + 'ouverture. Ensuite, c' + Q + 'est surtout vous qui nous écrirez, et nous vous répondrons. Désinscription en un clic.'],
];
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s8="A">Section 8, variante A : questions repliées, à ouvrir (comme sur l${Q}accueil)</div>
<div class="gfp-cap gfp-cap--creme gfp8" data-s8="A"><h2 style="text-align:center">Vos questions</h2><div class="gfp8A">${F.map((f, i) => `<details${i === 0 ? ' open' : ''}><summary>${f[0]}</summary><p>${f[1]}</p></details>`).join('')}</div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s8="B">Section 8, variante B : toutes les réponses visibles, en grille</div>
<div class="gfp-cap gfp-cap--creme gfp8" data-s8="B"><h2>Vos questions</h2><div class="gfp8B">${F.map(f => `<div><h3>${f[0]}</h3><p>${f[1]}</p></div>`).join('')}</div></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
return document.documentElement.scrollWidth;
})()
