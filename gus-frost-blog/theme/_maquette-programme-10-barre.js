(() => {
const N = ' ', Q = '’';
const css = `
.gfp10{display:none}
@media (max-width:749px){
 .gfp10{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:50;align-items:center;gap:10px;padding:8px 12px calc(8px + env(safe-area-inset-bottom));font-family:Figtree,sans-serif}
 .gfp10 .gfp-btn{min-height:44px;padding:8px 16px;font-size:16px;white-space:nowrap}
 .gfp10A{background:var(--cr);border-top:2px solid var(--tc);box-shadow:0 -4px 14px rgba(49,68,49,.12);color:var(--vf);justify-content:space-between}
 .gfp10A-t{min-width:0;line-height:1.2}
 .gfp10A-t b{display:block;font:600 18px/1.1 Fraunces,serif}
 .gfp10A-t span{font-size:13px}
 .gfp10B{background:var(--ts)}
 .gfp10B .gfp-btn{width:100%}
}`;
const A = `<div class="gfp10 gfp10A" data-s10="A"><div class="gfp10A-t"><b>179${N}€</b><span>Ouverture prochaine</span></div><a class="gfp-btn" href="#">Être prévenu</a></div>`;
const B = `<div class="gfp10 gfp10B" data-s10="B"><a class="gfp-btn" href="#">Être prévenu de l${Q}ouverture</a></div>`;
const g = document.querySelector('.gfp');
g.insertAdjacentHTML('beforeend', `<style>${css}</style>${A}${B}`);
return 'ok';
})()
