/* gf-quiz-anxiete.js — Diagnostic scoré « anxiété de séparation »
   ---------------------------------------------------------------------------
   Équivalent maison des outils type ScoreApp / Involve.me, sans app ni abonnement.

   Ce que ça fait :
     1. Écran d'accueil (hook), puis les questions une par une (barre de progression).
     2. Chaque réponse pèse un nombre de points ; certaines réponses sont un
        « signal d'alerte » qui force la bande rouge (prudence vétérinaire).
     3. Mur e-mail JUSTE avant le résultat (levier de capture n°1).
     4. Résultat par bande (vert / orange / rouge) : texte de profil, reco produit,
        code promo, bouton vers la collection.
     5. Branchement Klaviyo par les endpoints CLIENT (clé publique uniquement) :
        inscription à la liste + propriétés `profil_anxiete`, `quiz_anxiete_score`…
        + un évènement pour déclencher les 3 séquences.

   Toute la configuration (questions, barèmes, textes, seuils, clé Klaviyo) est
   posée par la section Liquid dans un <script type="application/json">.
   Aucune donnée ne sort tant que l'utilisateur n'a pas donné son e-mail + consenti.
*/
(function () {
  'use strict';

  var KLAVIYO_REVISION = '2024-10-15';
  var STORE_KEY = 'gf_quiz_anxiete_v1';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function emailValide(s) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(s || '').trim());
  }

  /* ------------------------------------------------------------------ */
  /*  Un quiz par instance de section (au cas où il y en aurait plusieurs) */
  /* ------------------------------------------------------------------ */
  function initQuiz(racine) {
    var brut = $('[data-gfq-config]', racine);
    if (!brut) return;
    var cfg;
    try { cfg = JSON.parse(brut.textContent); }
    catch (e) { console.warn('[quiz] config illisible', e); return; }

    var questions = cfg.questions || [];
    if (!questions.length) return;

    var scene = $('[data-gfq-scene]', racine);
    var reponses = new Array(questions.length).fill(null); // index de la réponse choisie
    var idx = 0;

    /* ----- Klaviyo (facultatif : masqué si non configuré) ----- */
    var mailActif = !!(cfg.cle && cfg.liste);

    function klaviyoPost(chemin, corps) {
      return fetch('https://a.klaviyo.com/client/' + chemin + '/?company_id=' + encodeURIComponent(cfg.cle), {
        method: 'POST',
        headers: { 'content-type': 'application/json', revision: KLAVIYO_REVISION },
        body: JSON.stringify(corps)
      }).then(function (r) {
        if (r.ok || r.status === 202) return true;
        return r.text().then(function (t) { throw new Error('Klaviyo ' + r.status + ' ' + t.slice(0, 200)); });
      });
    }

    // Propriétés poussées sur le profil Klaviyo. Noms alignés sur le kit de
    // montage : ils pilotent le Conditional Split du flow « Bienvenue Quiz ».
    function proprietes(res, prenom) {
      var p = {
        quiz_profil: res.profil,                       // 'vert' | 'orange' | 'rouge'
        quiz_score: res.score,                         // 0 à 24
        signal_alerte: res.alertes > 0 ? 'oui' : 'non',// force la séquence Rouge
        source_lead: cfg.source || 'quiz_anxiete_separation',
        quiz_date: new Date().toISOString().slice(0, 10)
      };
      if (prenom) p.prenom = prenom;
      return p;
    }

    // Inscription à la liste (consentement + propriétés de profil + prénom).
    function klaviyoInscrit(email, res, prenom) {
      var attrs = { email: email, properties: proprietes(res, prenom) };
      if (prenom) attrs.first_name = prenom;
      return klaviyoPost('subscriptions', {
        data: {
          type: 'subscription',
          attributes: {
            profile: { data: { type: 'profile', attributes: attrs } }
          },
          relationships: { list: { data: { type: 'list', id: cfg.liste } } }
        }
      });
    }

    // Évènement : permet de déclencher le flow sur « Quiz terminé » puis
    // de brancher (conditional split) selon la propriété quiz_profil.
    function klaviyoEvenement(email, res, prenom) {
      if (!cfg.metric) return Promise.resolve(true);
      return klaviyoPost('events', {
        data: {
          type: 'event',
          attributes: {
            metric: { data: { type: 'metric', attributes: { name: cfg.metric } } },
            profile: { data: { type: 'profile', attributes: { email: email } } },
            properties: proprietes(res, prenom),
            value: res.score
          }
        }
      });
    }

    /* ----- Scoring ----- */
    function calcule() {
      var score = 0, alertes = 0, max = 0;
      questions.forEach(function (q, i) {
        var poidsMax = 0;
        q.reponses.forEach(function (r) { if (r.p > poidsMax) poidsMax = r.p; });
        max += poidsMax;
        var choix = reponses[i];
        if (choix == null) return;
        var r = q.reponses[choix];
        score += r.p || 0;
        if (q.alerte && (choix + 1) === q.alerte) alertes += 1;
      });
      var profil;
      if (alertes >= (cfg.alertes_pour_rouge || 1)) profil = 'rouge';
      else if (score <= cfg.seuil_vert) profil = 'vert';
      else if (score <= cfg.seuil_orange) profil = 'orange';
      else profil = 'rouge';
      return { score: score, max: max, alertes: alertes, profil: profil };
    }

    /* ----- Rendu des écrans ----- */
    function vide() { scene.innerHTML = ''; }

    function majProgression() {
      var barre = $('[data-gfq-jauge]', racine);
      var txt = $('[data-gfq-compteur]', racine);
      var pct = Math.round((idx) / questions.length * 100);
      if (barre) barre.style.width = pct + '%';
      if (txt) txt.textContent = 'Question ' + (idx + 1) + ' sur ' + questions.length;
      var wrap = $('[data-gfq-progress]', racine);
      if (wrap) wrap.hidden = false;
    }

    function ecranQuestion() {
      vide();
      majProgression();
      var q = questions[idx];
      var carte = el('div', 'gfq-q');
      carte.appendChild(el('h2', 'gfq-q-enonce', q.enonce));

      var liste = el('div', 'gfq-reponses', '');
      q.reponses.forEach(function (r, i) {
        var b = el('button', 'gfq-rep', '<span>' + r.t + '</span>');
        b.type = 'button';
        if (reponses[idx] === i) b.classList.add('is-actif');
        b.addEventListener('click', function () {
          reponses[idx] = i;
          // Petit délai pour laisser voir la sélection, puis on avance.
          Array.prototype.forEach.call(liste.children, function (c) { c.classList.remove('is-actif'); });
          b.classList.add('is-actif');
          setTimeout(avance, 220);
        });
        liste.appendChild(b);
      });
      carte.appendChild(liste);

      var nav = el('div', 'gfq-nav', '');
      if (idx > 0) {
        var prec = el('button', 'gfq-lien', '‹ Précédent');
        prec.type = 'button';
        prec.addEventListener('click', recule);
        nav.appendChild(prec);
      }
      carte.appendChild(nav);
      scene.appendChild(carte);
    }

    function avance() {
      if (reponses[idx] == null) return;
      if (idx < questions.length - 1) { idx += 1; ecranQuestion(); }
      else ecranMur();
    }
    function recule() {
      if (idx > 0) { idx -= 1; ecranQuestion(); }
    }

    function ecranMur() {
      vide();
      var barre = $('[data-gfq-jauge]', racine);
      if (barre) barre.style.width = '100%';
      var txt = $('[data-gfq-compteur]', racine);
      if (txt) txt.textContent = 'Dernière étape';

      var m = cfg.mur || {};
      var box = el('div', 'gfq-mur');
      box.appendChild(el('h2', 'gfq-mur-titre', m.titre || 'Votre résultat est prêt'));
      if (m.texte) box.appendChild(el('p', 'gfq-mur-texte', m.texte));

      var form = el('form', 'gfq-form', '');
      form.noValidate = true;

      var prenomChamp = el('input', 'gfq-input');
      prenomChamp.type = 'text';
      prenomChamp.placeholder = m.prenom_placeholder || 'Prénom (facultatif)';
      prenomChamp.autocomplete = 'given-name';
      form.appendChild(prenomChamp);

      var champ = el('input', 'gfq-input');
      champ.type = 'email';
      champ.placeholder = m.placeholder || 'votre@email.fr';
      champ.autocomplete = 'email';
      champ.required = true;
      form.appendChild(champ);

      var erreur = el('p', 'gfq-erreur', '');
      erreur.hidden = true;

      var consentTxt = m.consent || 'J’accepte de recevoir mon résultat et des conseils par e-mail. Désinscription en un clic.';
      var lab = el('label', 'gfq-consent',
        '<input type="checkbox" class="gfq-check"> <span>' + consentTxt + '</span>');
      form.appendChild(lab);

      var bouton = el('button', 'gfq-btn', m.bouton || 'Voir mon résultat');
      bouton.type = 'submit';
      form.appendChild(bouton);
      form.appendChild(erreur);

      if (m.note) box.appendChild(el('p', 'gfq-mur-note', m.note));

      form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var email = champ.value.trim();
        var prenom = prenomChamp.value.trim();
        var coche = $('.gfq-check', form).checked;
        erreur.hidden = true;
        if (!emailValide(email)) { erreur.textContent = 'Merci de saisir une adresse e-mail valide.'; erreur.hidden = false; return; }
        if (!coche) { erreur.textContent = 'Merci de cocher la case pour recevoir votre résultat.'; erreur.hidden = false; return; }

        var res = calcule();
        bouton.disabled = true;
        bouton.textContent = 'Un instant…';

        var envoi = mailActif
          ? klaviyoInscrit(email, res, prenom).then(function () { return klaviyoEvenement(email, res, prenom); })
          : Promise.resolve(true);

        envoi.catch(function (e) {
          // On n'empêche jamais l'utilisateur de voir son résultat pour un souci réseau.
          console.warn('[quiz] envoi Klaviyo impossible', e);
        }).then(function () {
          memorise(res, email);
          ecranResultat(res);
        });
      });

      box.insertBefore(form, box.querySelector('.gfq-mur-note') || null);
      // (form ajouté avant la note ; si pas de note, il est à la fin)
      if (!box.contains(form)) box.appendChild(form);

      var nav = el('div', 'gfq-nav', '');
      var prec = el('button', 'gfq-lien', '‹ Revenir aux questions');
      prec.type = 'button';
      prec.addEventListener('click', function () { idx = questions.length - 1; ecranQuestion(); });
      nav.appendChild(prec);
      box.appendChild(nav);

      scene.appendChild(box);
      champ.focus();
    }

    function ecranResultat(res) {
      vide();
      var wrap = $('[data-gfq-progress]', racine);
      if (wrap) wrap.hidden = true;

      var band = (cfg.bands && cfg.bands[res.profil]) || {};
      var box = el('div', 'gfq-res gfq-res--' + res.profil);

      box.appendChild(el('div', 'gfq-badge', band.badge || res.profil.toUpperCase()));
      box.appendChild(el('h2', 'gfq-res-titre', band.titre || 'Votre profil'));
      box.appendChild(el('p', 'gfq-res-score', 'Score : ' + res.score + ' / ' + res.max));
      if (band.html) box.appendChild(el('div', 'gfq-res-texte', band.html));

      if (band.promo) {
        var promo = el('div', 'gfq-promo', '');
        promo.appendChild(el('span', 'gfq-promo-lbl', band.promo_label || 'Votre code'));
        var code = el('button', 'gfq-promo-code', band.promo);
        code.type = 'button';
        code.title = 'Copier le code';
        code.addEventListener('click', function () {
          if (navigator.clipboard) navigator.clipboard.writeText(band.promo);
          code.classList.add('is-copie');
          var anc = code.textContent;
          code.textContent = 'Copié ✓';
          setTimeout(function () { code.textContent = anc; code.classList.remove('is-copie'); }, 1600);
        });
        promo.appendChild(code);
        box.appendChild(promo);
      }

      if (band.cta_url && band.cta_label) {
        var cta = el('a', 'gfq-btn gfq-btn--cta', band.cta_label);
        cta.href = band.cta_url;
        box.appendChild(cta);
      }

      var refaire = el('button', 'gfq-lien gfq-refaire', 'Refaire le test');
      refaire.type = 'button';
      refaire.addEventListener('click', function () {
        reponses = new Array(questions.length).fill(null);
        idx = 0;
        try { localStorage.removeItem(STORE_KEY); } catch (e) {}
        ecranQuestion();
      });
      box.appendChild(refaire);

      scene.appendChild(box);
      // On remonte en haut de la section pour que le résultat soit visible.
      racine.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /* ----- Persistance légère (pour re-montrer le résultat au retour) ----- */
    function memorise(res, email) {
      try {
        localStorage.setItem(STORE_KEY, JSON.stringify({
          score: res.score, max: res.max, profil: res.profil, email: email,
          date: new Date().toISOString()
        }));
      } catch (e) {}
    }

    /* ----- Démarrage ----- */
    var demarrer = $('[data-gfq-start]', racine);
    if (demarrer) {
      demarrer.addEventListener('click', function () {
        $('[data-gfq-intro]', racine).hidden = true;
        idx = 0;
        ecranQuestion();
      });
    }

    // Si l'utilisateur a déjà fait le test, on lui propose de revoir son résultat.
    try {
      var vu = JSON.parse(localStorage.getItem(STORE_KEY) || 'null');
      if (vu && vu.profil && cfg.bands && cfg.bands[vu.profil]) {
        var rappel = $('[data-gfq-rappel]', racine);
        if (rappel) {
          rappel.hidden = false;
          var lien = $('[data-gfq-revoir]', rappel);
          if (lien) lien.addEventListener('click', function (e) {
            e.preventDefault();
            $('[data-gfq-intro]', racine).hidden = true;
            ecranResultat({ score: vu.score, max: vu.max, alertes: 0, profil: vu.profil });
          });
        }
      }
    } catch (e) {}
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-gfq]'), initQuiz);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
