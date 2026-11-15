(() => {
const N = ' ', Q = '’';
const IMG = 'https://cdn.shopify.com/s/files/1/0614/7119/5357/files/hero-tapis-lechage-apaiser-chien.png?width=900';
const css = `
.gfp9-form{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin:0}
.gfp9-form input{min-height:50px;border:2px solid var(--vf);border-radius:10px;padding:0 14px;font:16px Figtree,sans-serif;background:var(--cr);color:var(--vf);min-width:0}
.gfp9-rgpd{font-size:13px;line-height:1.45;margin:10px 0 0}
.gfp9-rgpd a{color:inherit;text-decoration:underline}
.gfp9-r{display:grid;gap:10px;margin:0 0 20px;padding:0;list-style:none}
.gfp9-r li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;align-items:start;font-size:16px;line-height:1.45}
.gfp9-r li b{display:block;font:600 18px/1.3 Fraunces,serif}
/* A : sauge, centré */
.gfp9A{max-width:720px;margin:0 auto}
.gfp9A h2{text-align:center}
.gfp9A .gfp9-intro{text-align:center;font-size:17px;line-height:1.5;margin:0 0 20px}
.gfp9A .gfp9-r li{background:var(--cr);border-radius:14px;padding:14px 16px}
/* B : bandeau terracotta + photo */
.gfp9B{max-width:1220px;margin:0 auto;background:var(--ts);color:var(--cr);border-radius:26px;overflow:hidden;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}
.gfp9B img{width:100%;height:100%;object-fit:cover;display:block;min-height:100%}
.gfp9B-t{padding:36px 40px;min-width:0}
.gfp9B h2{color:var(--cr)}
.gfp9B .gfp9-intro{font-size:17px;line-height:1.5;margin:0 0 18px}
.gfp9B .gfp9-r .gfp-num{background:var(--cr);color:var(--ts)}
.gfp9B .gfp9-form input{border-color:var(--cr)}
@media (max-width:749px){
 .gfp9-form{grid-template-columns:minmax(0,1fr)}
 .gfp9-form .gfp-btn{width:100%}
 .gfp9A .gfp9-intro,.gfp9B .gfp9-intro{font-size:16px;margin-bottom:14px}
 .gfp9A .gfp9-r li{padding:12px}
 .gfp9B{grid-template-columns:minmax(0,1fr);border-radius:20px}
 .gfp9B img{height:200px}
 .gfp9B-t{padding:20px 16px}
}`;
const titre = 'Être prévenu de l' + Q + 'ouverture';
const intro = 'Le Programme du Foyer Apaisé ouvre bientôt, à 179' + N + '€. Laissez votre adresse, vous serez parmi les premiers à le savoir.';
const R = [
 ['Le guide, tout de suite', 'Dès que vous confirmez votre adresse, vous recevez «' + N + 'Les 5 erreurs qui aggravent le stress de votre chien' + N + '». Il est à vous, quoi que vous décidiez ensuite.'],
 ['Avant l' + Q + 'ouverture publique', 'Vous êtes prévenu par e-mail avant tout le monde.'],
 ['Aucun paiement, aucun engagement', 'Vous décidez à l' + Q + 'ouverture, ou jamais.'],
];
const rgpd = 'Votre adresse sert uniquement à vous envoyer le guide et les nouvelles du Programme. Désinscription en un clic, à tout moment. <a href="/policies/privacy-policy">Politique de confidentialité</a>.';
const form = `<form class="gfp9-form" onsubmit="return false"><input type="email" placeholder="Votre adresse e-mail" aria-label="Votre adresse e-mail"><button class="gfp-btn" type="submit">Être prévenu</button></form><p class="gfp9-rgpd">${rgpd}</p>`;
const lis = R.map((r, i) => `<li><span class="gfp-num" style="margin:0">${i + 1}</span><span><b>${r[0]}</b>${r[1]}</span></li>`).join('');
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s9="A">Section 9, variante A : capsule sauge, trois raisons puis le formulaire</div>
<div class="gfp-cap gfp-cap--sauge" data-s9="A"><div class="gfp9A"><h2>${titre}</h2><p class="gfp9-intro">${intro}</p><ul class="gfp9-r">${lis}</ul>${form}</div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s9="B">Section 9, variante B : bandeau terracotta avec photo</div>
<div class="gfp9B" data-s9="B"><img src="${IMG}" alt=""><div class="gfp9B-t"><h2>${titre}</h2><p class="gfp9-intro">${intro}</p><ul class="gfp9-r">${lis}</ul>${form}</div></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
return document.documentElement.scrollWidth;
})()
