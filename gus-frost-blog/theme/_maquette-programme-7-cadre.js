(() => {
const N = ' ', Q = '’';
const css = `
.gfp7A{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
.gfp7A>div{background:var(--cr);border-radius:18px;padding:22px;min-width:0}
.gfp7A h3{font-size:20px;margin:0 0 10px}
.gfp7A p{font-size:16px;line-height:1.55;margin:0 0 10px}
.gfp7A p:last-child{margin:0}
.gfp7-veto{font-weight:700;color:var(--ts)}
.gfp7B{max-width:1220px;margin:0 auto;background:var(--cr);border-left:6px solid var(--ts);border-radius:16px;padding:20px 24px;display:grid;grid-template-columns:auto minmax(0,1fr);gap:18px;align-items:start}
.gfp7B-ic{width:44px;height:44px;border-radius:50%;background:var(--ts);color:var(--cr);display:flex;align-items:center;justify-content:center;font:700 22px/1 Fraunces,serif}
.gfp7B h3{font-size:19px;margin:0 0 6px}
.gfp7B p{font-size:15px;line-height:1.55;margin:0 0 6px}
@media (max-width:749px){
 .gfp7A{grid-template-columns:minmax(0,1fr);gap:10px}
 .gfp7A>div{padding:16px 14px}
 .gfp7B{grid-template-columns:minmax(0,1fr);gap:10px;padding:16px 14px;border-left-width:4px}
 .gfp7B-ic{width:36px;height:36px;font-size:18px}
}`;
const veto1 = 'Le Programme est un accompagnement éducatif et comportemental. Il ne constitue ni un diagnostic, ni une prescription, ni un traitement, et il ne se substitue pas à une consultation vétérinaire' + N + ': certains troubles du comportement ont une origine médicale.';
const veto2 = 'Pour une anxiété sévère, voyez votre vétérinaire avant toute chose.';
const veto3 = 'Si votre questionnaire révèle une situation qui relève d' + Q + 'un vétérinaire, nous vous le dirons et vous orienterons vers lui. Votre commande vous est alors intégralement remboursée si aucun bilan ne vous a été remis.';
const moyens = 'L' + Q + 'évolution d' + Q + 'un chien dépend de la mise en œuvre effective des recommandations. Aucun résultat comportemental ne peut être garanti.';
const apres1 = 'Vous recevez par e-mail le lien vers votre questionnaire comportemental. Vous le remplissez à votre rythme, vous y joignez votre vidéo, et votre bilan suit. Le coffret part de son côté.';
const apres2 = 'Avant de payer, vous confirmez que l' + Q + 'accompagnement peut démarrer sans attendre le délai de rétractation de 14' + N + 'jours' + N + ': c' + Q + 'est ce qui permet de vous envoyer votre questionnaire tout de suite. Vous gardez la possibilité de vous rétracter, seule la part déjà fournie restant due, et la garantie de 30' + N + 'jours va plus loin.';
const A = `<div class="gfp-lbl" style="margin-top:34px" data-s7="A">Section 7, variante A : une capsule sauge, le cadre et l${Q}après-commande</div>
<div class="gfp-cap gfp-cap--sauge" data-s7="A"><h2>Le cadre, et ce qui se passe après votre commande</h2><div class="gfp7A">
<div><h3>Ce que le Programme n${Q}est pas</h3><p>${veto1}</p><p class="gfp7-veto">${veto2}</p><p>${veto3}</p><p>${moyens}</p></div>
<div><h3>Après votre commande</h3><p>${apres1}</p><p>${apres2}</p></div></div></div>`;
const B = `<div class="gfp-lbl" style="margin-top:34px" data-s7="B">Section 7, variante B : un encart sobre pour le cadre vétérinaire (l${Q}après-commande passe dans la FAQ)</div>
<div class="gfp7B" data-s7="B"><div class="gfp7B-ic">!</div><div><h3>Un accompagnement, pas un soin</h3><p>${veto1} <strong>${veto2}</strong></p><p>${veto3}</p><p>${moyens}</p></div></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
return document.documentElement.scrollWidth;
})()
