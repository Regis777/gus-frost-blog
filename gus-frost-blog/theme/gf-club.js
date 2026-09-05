/* gf-club.js — formulaire d'adhésion au Club Gus et Frost
   --------------------------------------------------------------------------
   1. Valide le formulaire (e-mail + consentement obligatoires).
   2. Inscrit le profil dans Klaviyo par les endpoints CLIENT (clé PUBLIQUE
      uniquement, jamais de clé privée dans le thème) — mêmes appels que
      « Le Carnet » et le quiz anxiété.
   3. Affiche l'écran de confirmation, qui pousse vers la création du compte
      client Shopify (c'est le compte qui ouvre l'espace membre, pas l'e-mail).

   Clé ou liste absente du réglage de section = pas d'appel Klaviyo : le
   formulaire se contente d'envoyer vers la création de compte. La page reste
   donc fonctionnelle même mal configurée.

   Aucune donnée n'est stockée ici : le seul localStorage est un drapeau
   « déjà inscrit » qui sert à afficher un rappel au retour. */
(function () {
  'use strict';

  var KLAVIYO_REVISION = '2024-10-15';
  var CLE_LOCALE = 'gf_club_inscrit';

  function $(sel, racine) { return (racine || document).querySelector(sel); }

  function init(racine) {
    var noeudCfg = $('[data-gfc-config]', racine);
    if (!noeudCfg) return;

    var cfg;
    try { cfg = JSON.parse(noeudCfg.textContent); } catch (e) { return; }

    var form = $('[data-gfc-form]', racine);
    var panneauForm = $('[data-gfc-panneau-form]', racine);
    var panneauSucces = $('[data-gfc-panneau-succes]', racine);
    var zoneErreur = $('[data-gfc-erreur]', racine);
    var bouton = form ? $('[data-gfc-envoyer]', form) : null;
    var rappel = $('[data-gfc-rappel]', racine);

    // Rappel discret pour qui est déjà passé par le formulaire.
    try {
      if (rappel && window.localStorage.getItem(CLE_LOCALE)) rappel.hidden = false;
    } catch (e) { /* navigation privée : on ignore */ }

    if (!form) return;

    var mailActif = !!(cfg.cle && cfg.liste);

    /* ----- Klaviyo ----- */
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

    // Propriétés de profil : elles pilotent les segments et le flow d'accueil.
    function proprietes(donnees) {
      var p = {
        source_lead: cfg.source || 'club',
        club_membre: 'oui',
        club_date: new Date().toISOString().slice(0, 10)
      };
      if (donnees.prenom) p.prenom = donnees.prenom;
      if (donnees.animal) p.prenom_animal = donnees.animal;
      return p;
    }

    function klaviyoInscrit(donnees) {
      var attrs = { email: donnees.email, properties: proprietes(donnees) };
      if (donnees.prenom) attrs.first_name = donnees.prenom;
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

    function klaviyoEvenement(donnees) {
      if (!cfg.metric) return Promise.resolve(true);
      return klaviyoPost('events', {
        data: {
          type: 'event',
          attributes: {
            metric: { data: { type: 'metric', attributes: { name: cfg.metric } } },
            profile: { data: { type: 'profile', attributes: { email: donnees.email } } },
            properties: proprietes(donnees)
          }
        }
      });
    }

    /* ----- Affichage ----- */
    function erreur(message) {
      if (!zoneErreur) return;
      zoneErreur.textContent = message;
      zoneErreur.hidden = false;
    }

    function effaceErreur() {
      if (zoneErreur) zoneErreur.hidden = true;
    }

    function succes(donnees) {
      try { window.localStorage.setItem(CLE_LOCALE, '1'); } catch (e) { /* ignoré */ }

      // L'e-mail est pré-rempli dans le lien de création de compte quand le
      // thème le permet : une saisie de moins pour le futur membre.
      var lien = $('[data-gfc-compte]', panneauSucces);
      if (lien && cfg.compte_url) {
        var url = cfg.compte_url;
        if (donnees.email) {
          url += (url.indexOf('?') === -1 ? '?' : '&') + 'email=' + encodeURIComponent(donnees.email);
        }
        lien.setAttribute('href', url);
      }
      if (panneauForm) panneauForm.hidden = true;
      if (panneauSucces) {
        panneauSucces.hidden = false;
        panneauSucces.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }

    /* ----- Soumission ----- */
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      effaceErreur();

      var donnees = {
        email: (form.elements.email ? form.elements.email.value : '').trim(),
        prenom: (form.elements.prenom ? form.elements.prenom.value : '').trim(),
        animal: (form.elements.animal ? form.elements.animal.value : '').trim()
      };
      var consent = form.elements.consent;

      if (!donnees.email || donnees.email.indexOf('@') < 1 || donnees.email.indexOf('.') < 0) {
        erreur('Il manque une adresse e-mail valide pour vous envoyer vos accès.');
        return;
      }
      if (consent && !consent.checked) {
        erreur('Merci de cocher la case pour que nous puissions vous écrire.');
        return;
      }

      if (bouton) {
        bouton.disabled = true;
        bouton.dataset.libelle = bouton.textContent;
        bouton.textContent = 'Un instant…';
      }

      function termine() { succes(donnees); }

      function echoue(e) {
        console.warn('[club] inscription Klaviyo impossible', e);
        if (bouton) {
          bouton.disabled = false;
          if (bouton.dataset.libelle) bouton.textContent = bouton.dataset.libelle;
        }
        erreur('L’envoi n’a pas abouti. Vérifiez votre connexion et réessayez dans un instant.');
      }

      if (!mailActif) { termine(); return; }

      klaviyoInscrit(donnees)
        .then(function () { return klaviyoEvenement(donnees).catch(function () { return true; }); })
        .then(termine)
        .catch(echoue);
    });
  }

  function demarre() {
    var racines = document.querySelectorAll('[data-gfc]');
    for (var i = 0; i < racines.length; i++) init(racines[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', demarre);
  } else {
    demarre();
  }

  // L'éditeur de thème recharge la section sans recharger la page.
  document.addEventListener('shopify:section:load', function (ev) {
    var racine = ev.target.querySelector('[data-gfc]');
    if (racine) init(racine);
  });
})();
