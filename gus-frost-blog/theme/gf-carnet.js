/* gf-carnet.js — « Le Carnet » de Gus & Frost
   Carnet de santé, rappels, budget et souvenirs — 100 % dans le navigateur.
   Aucune donnée n'est envoyée : JSON dans localStorage, photos dans IndexedDB.
   Le seul point d'entrée est window.GFCarnet.init(racine). */
(function () {
  'use strict';

  var CLE = 'gf-carnet-v1';
  var IDB_NOM = 'gf-carnet';
  var IDB_STORE = 'photos';
  var MAX_PARTAGE = 6000; // caractères d'URL au-delà desquels on refuse le lien

  /* ================= Utilitaires ================= */

  function uid() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var ESPECES = ['Chien', 'Chat', 'Lapin', 'Cheval', 'Oiseau', 'Rongeur', 'Reptile', 'Autre'];
  var EMOJIS = {
    Chien: '🐕', Chat: '🐈', Lapin: '🐇', Cheval: '🐎',
    Oiseau: '🦜', Rongeur: '🐹', Reptile: '🦎', Autre: '🐾'
  };
  var CATEGORIES = ['Alimentation', 'Vétérinaire', 'Traitements', 'Toilettage',
    'Accessoires', 'Jouets', 'Assurance', 'Éducation', 'Garde', 'Autre'];

  function emoji(espece) { return EMOJIS[espece] || '🐾'; }

  function aujourdhui() {
    var d = new Date();
    d.setHours(0, 0, 0, 0);
    return d;
  }

  function isoJour(d) {
    // ISO local (pas toISOString, qui décale d'un jour selon le fuseau)
    var m = String(d.getMonth() + 1).padStart(2, '0');
    var j = String(d.getDate()).padStart(2, '0');
    return d.getFullYear() + '-' + m + '-' + j;
  }

  function parseIso(s) {
    if (!s) return null;
    var p = String(s).split('-');
    if (p.length !== 3) return null;
    var d = new Date(+p[0], +p[1] - 1, +p[2]);
    return isNaN(d.getTime()) ? null : d;
  }

  function dateFr(s) {
    var d = parseIso(s);
    if (!d) return '—';
    return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  function joursEntre(a, b) {
    return Math.round((b - a) / 86400000);
  }

  function ajouteJours(s, n) {
    var d = parseIso(s);
    if (!d) return '';
    d.setDate(d.getDate() + n);
    return isoJour(d);
  }

  var fmtEur = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });
  function euros(n) { return fmtEur.format(Number(n) || 0); }

  function age(naissance) {
    var d = parseIso(naissance);
    if (!d) return null;
    var maintenant = aujourdhui();
    if (d > maintenant) return null;
    var mois = (maintenant.getFullYear() - d.getFullYear()) * 12 + (maintenant.getMonth() - d.getMonth());
    if (maintenant.getDate() < d.getDate()) mois--;
    var ans = Math.floor(mois / 12);
    var reste = mois % 12;
    if (ans < 1) return reste + (reste > 1 ? '&nbsp;mois' : '&nbsp;mois');
    if (reste === 0) return ans + (ans > 1 ? '&nbsp;ans' : '&nbsp;an');
    return ans + (ans > 1 ? '&nbsp;ans' : '&nbsp;an') + '&nbsp;et&nbsp;' + reste + '&nbsp;mois';
  }

  /* ================= Stockage ================= */

  var etat = null;      // données structurées
  var photos = {};      // id -> dataURL (cache mémoire, source = IndexedDB)

  function etatVide() {
    return {
      v: 1, animaux: [], vaccins: [], traitements: [], poids: [],
      visites: [], rappels: [], depenses: [], souvenirs: []
    };
  }

  function charge() {
    try {
      var brut = localStorage.getItem(CLE);
      if (!brut) return etatVide();
      var d = JSON.parse(brut);
      var vide = etatVide();
      Object.keys(vide).forEach(function (k) {
        if (k !== 'v' && !Array.isArray(d[k])) d[k] = [];
      });
      return d;
    } catch (e) {
      console.warn('[carnet] données illisibles, on repart à vide', e);
      return etatVide();
    }
  }

  function sauve() {
    try {
      localStorage.setItem(CLE, JSON.stringify(etat));
      return true;
    } catch (e) {
      toast('Sauvegarde impossible&nbsp;: la mémoire du navigateur est pleine. Exportez puis allégez vos souvenirs.', 6000);
      return false;
    }
  }

  function ouvreIdb() {
    return new Promise(function (res, rej) {
      if (!window.indexedDB) return rej(new Error('IndexedDB indisponible'));
      var r = indexedDB.open(IDB_NOM, 1);
      r.onupgradeneeded = function () { r.result.createObjectStore(IDB_STORE); };
      r.onsuccess = function () { res(r.result); };
      r.onerror = function () { rej(r.error); };
    });
  }

  function idbTx(mode, fn) {
    return ouvreIdb().then(function (db) {
      return new Promise(function (res, rej) {
        var tx = db.transaction(IDB_STORE, mode);
        var req = fn(tx.objectStore(IDB_STORE));
        tx.oncomplete = function () { db.close(); res(req && req.result); };
        tx.onerror = function () { db.close(); rej(tx.error); };
      });
    });
  }

  function photoEcrit(id, dataUrl) {
    photos[id] = dataUrl;
    return idbTx('readwrite', function (s) { return s.put(dataUrl, id); })
      .catch(function (e) { console.warn('[carnet] photo non persistée', e); });
  }

  function photoSupprime(id) {
    if (!id) return Promise.resolve();
    delete photos[id];
    return idbTx('readwrite', function (s) { return s.delete(id); }).catch(function () {});
  }

  function photosCharge() {
    return ouvreIdb().then(function (db) {
      return new Promise(function (res) {
        var tx = db.transaction(IDB_STORE, 'readonly');
        var cur = tx.objectStore(IDB_STORE).openCursor();
        cur.onsuccess = function () {
          var c = cur.result;
          if (c) { photos[c.key] = c.value; c.continue(); }
        };
        tx.oncomplete = function () { db.close(); res(); };
        tx.onerror = function () { db.close(); res(); };
      });
    }).catch(function () {});
  }

  /* Redimensionne une image côté client : 900 px max, JPEG qualité 0,82. */
  function redimensionne(file) {
    return new Promise(function (res, rej) {
      if (!/^image\//.test(file.type)) return rej(new Error('Ce fichier n’est pas une image.'));
      var lecteur = new FileReader();
      lecteur.onerror = function () { rej(new Error('Lecture du fichier impossible.')); };
      lecteur.onload = function () {
        var img = new Image();
        img.onerror = function () { rej(new Error('Image illisible.')); };
        img.onload = function () {
          var max = 900;
          var ech = Math.min(1, max / Math.max(img.width, img.height));
          var c = document.createElement('canvas');
          c.width = Math.round(img.width * ech);
          c.height = Math.round(img.height * ech);
          c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
          res(c.toDataURL('image/jpeg', 0.82));
        };
        img.src = lecteur.result;
      };
      lecteur.readAsDataURL(file);
    });
  }

  /* ================= Sélecteurs ================= */

  var racine = null;
  var ongletActif = 'identite';
  var animalActif = null;
  var modeLecture = false; // fiche partagée : lecture seule

  function animal(id) {
    for (var i = 0; i < etat.animaux.length; i++) {
      if (etat.animaux[i].id === id) return etat.animaux[i];
    }
    return null;
  }

  function animalCourant() { return animal(animalActif) || etat.animaux[0] || null; }

  function nomAnimal(id) {
    var a = animal(id);
    return a ? a.nom : 'Animal supprimé';
  }

  function pourAnimal(liste, id) {
    return etat[liste].filter(function (x) { return x.petId === id; });
  }

  function parDate(cle, sens) {
    return function (a, b) {
      var x = a[cle] || '', y = b[cle] || '';
      return sens === 'asc' ? (x < y ? -1 : x > y ? 1 : 0) : (x > y ? -1 : x < y ? 1 : 0);
    };
  }

  /* Toutes les échéances, tous animaux confondus, triées par date. */
  function echeances() {
    var out = [];
    etat.vaccins.forEach(function (v) {
      if (v.rappel) out.push({ type: 'vaccin', src: v, petId: v.petId, date: v.rappel, titre: 'Rappel vaccin&nbsp;: ' + esc(v.nom) });
    });
    etat.traitements.forEach(function (t) {
      if (t.prochaine) out.push({ type: 'traitement', src: t, petId: t.petId, date: t.prochaine, titre: esc(t.nom) });
    });
    etat.rappels.forEach(function (r) {
      if (r.date && !r.fait) out.push({ type: 'rappel', src: r, petId: r.petId, date: r.date, titre: esc(r.titre) });
    });
    return out.sort(parDate('date', 'asc'));
  }

  function statut(dateIso) {
    var d = parseIso(dateIso);
    if (!d) return { cls: 'ok', texte: '—', j: 9999 };
    var j = joursEntre(aujourdhui(), d);
    if (j < 0) return { cls: 'late', texte: 'En retard de&nbsp;' + (-j) + '&nbsp;j', j: j };
    if (j === 0) return { cls: 'late', texte: "Aujourd'hui", j: j };
    if (j <= 30) return { cls: 'soon', texte: 'Dans&nbsp;' + j + '&nbsp;j', j: j };
    return { cls: 'ok', texte: 'Dans&nbsp;' + j + '&nbsp;j', j: j };
  }

  function nbUrgent() {
    return echeances().filter(function (e) { return statut(e.date).j <= 30; }).length;
  }

  /* ================= Rendu ================= */

  function $(sel) { return racine.querySelector(sel); }

  function rendu() {
    if (modeLecture) return;
    renduPetbar();
    renduOnglets();
    var hote = $('[data-gfc-panels]');
    var a = animalCourant();
    animalActif = a ? a.id : null;

    if (!etat.animaux.length) {
      hote.innerHTML = '<div class="gfc-empty">' +
        '<p><strong>Commencez par ajouter un animal.</strong></p>' +
        '<p>Tout reste sur cet appareil&nbsp;: rien n’est envoyé, aucun compte à créer.</p>' +
        '<p style="margin-top:14px"><button type="button" class="gfc-btn gfc-btn--primary" data-act="pet-new">+&nbsp;Ajouter mon animal</button></p>' +
        '</div>';
      return;
    }

    var vues = {
      identite: vueIdentite, sante: vueSante, rappels: vueRappels,
      budget: vueBudget, souvenirs: vueSouvenirs
    };
    hote.innerHTML = (vues[ongletActif] || vueIdentite)(a);
  }

  function renduPetbar() {
    var bar = $('[data-gfc-petbar]');
    var html = etat.animaux.map(function (a) {
      var sel = a.id === animalActif;
      var ava = a.photoId && photos[a.photoId]
        ? '<img class="gfc-pet-ava" src="' + photos[a.photoId] + '" alt="">'
        : '<span class="gfc-pet-ava">' + emoji(a.espece) + '</span>';
      return '<button type="button" class="gfc-pet" data-act="pet-pick" data-id="' + a.id + '" aria-pressed="' + sel + '">' +
        ava + '<span>' + esc(a.nom) + '</span></button>';
    }).join('');
    bar.innerHTML = html +
      '<button type="button" class="gfc-pet-add" data-act="pet-new">+&nbsp;Animal</button>';
  }

  function renduOnglets() {
    var urgent = nbUrgent();
    racine.querySelectorAll('[data-gfc-tab]').forEach(function (b) {
      var actif = b.getAttribute('data-gfc-tab') === ongletActif;
      b.setAttribute('aria-selected', actif ? 'true' : 'false');
      var pastille = b.querySelector('.gfc-tab-count');
      if (b.getAttribute('data-gfc-tab') === 'rappels') {
        if (urgent && !pastille) {
          b.insertAdjacentHTML('beforeend', '<span class="gfc-tab-count">' + urgent + '</span>');
        } else if (urgent && pastille) {
          pastille.textContent = urgent;
        } else if (!urgent && pastille) {
          pastille.remove();
        }
      }
    });
  }

  function ligne(o) {
    return '<div class="gfc-row' + (o.fait ? ' gfc-row--done' : '') + '">' +
      '<div class="gfc-row-main">' +
        '<div class="gfc-row-title">' + o.titre + '</div>' +
        (o.sous ? '<div class="gfc-row-sub">' + o.sous + '</div>' : '') +
      '</div>' +
      (o.badge || '') +
      (o.montant ? '<div class="gfc-row-amount">' + o.montant + '</div>' : '') +
      '<div class="gfc-row-act">' + (o.actions || '') + '</div>' +
    '</div>';
  }

  function boutonsEdit(type, id) {
    return '<button type="button" class="gfc-icon-btn" data-act="edit" data-type="' + type + '" data-id="' + id + '" title="Modifier" aria-label="Modifier">✏️</button>' +
      '<button type="button" class="gfc-icon-btn" data-act="del" data-type="' + type + '" data-id="' + id + '" title="Supprimer" aria-label="Supprimer">🗑️</button>';
  }

  function vide(texte) { return '<div class="gfc-empty">' + texte + '</div>'; }

  /* ---------- Onglet Identité ---------- */
  function vueIdentite(a) {
    var poids = pourAnimal('poids', a.id).sort(parDate('date', 'desc'));
    var dernier = poids[0];
    var ag = age(a.naissance);
    var photo = a.photoId && photos[a.photoId]
      ? '<img class="gfc-id-photo" src="' + photos[a.photoId] + '" alt="Photo de ' + esc(a.nom) + '">'
      : '<span class="gfc-id-photo">' + emoji(a.espece) + '</span>';

    var meta = [a.espece, a.race, a.sexe].filter(Boolean).join('&nbsp;· ');

    function fait(dt, dd) {
      return '<div class="gfc-fact"><dt>' + dt + '</dt><dd>' + dd + '</dd></div>';
    }

    return '<section class="gfc-sec">' +
      '<div class="gfc-card"><div class="gfc-id">' + photo +
        '<div class="gfc-id-body">' +
          '<h2>' + esc(a.nom) + '</h2>' +
          '<p class="gfc-id-meta">' + (meta || 'Fiche à compléter') + '</p>' +
          '<dl class="gfc-facts">' +
            fait('Âge', ag || '—') +
            fait('Naissance', a.naissance ? dateFr(a.naissance) : '—') +
            fait('Poids', dernier ? String(dernier.kg).replace('.', ',') + '&nbsp;kg' : '—') +
            fait('Stérilisé', a.sterilise || '—') +
          '</dl>' +
          '<p style="margin-top:14px"><button type="button" class="gfc-btn gfc-btn--sm" data-act="pet-edit">Modifier la fiche</button></p>' +
        '</div>' +
      '</div></div>' +

      '<div class="gfc-card">' +
        '<div class="gfc-sec-head"><h3>Identification &amp; vétérinaire</h3></div>' +
        '<dl class="gfc-facts">' +
          fait('Puce / tatouage', a.puce ? esc(a.puce) : '—') +
          fait('Vétérinaire', a.vetoNom ? esc(a.vetoNom) : '—') +
          fait('Téléphone', a.vetoTel ? '<a href="tel:' + esc(a.vetoTel).replace(/\s/g, '') + '">' + esc(a.vetoTel) + '</a>' : '—') +
        '</dl>' +
        (a.notes ? '<p style="margin-top:14px"><strong>Notes&nbsp;:</strong> ' + esc(a.notes) + '</p>' : '') +
      '</div>' +
    '</section>';
  }

  /* ---------- Onglet Santé ---------- */
  function vueSante(a) {
    var vaccins = pourAnimal('vaccins', a.id).sort(parDate('date', 'desc'));
    var traitements = pourAnimal('traitements', a.id).sort(parDate('prochaine', 'asc'));
    var visites = pourAnimal('visites', a.id).sort(parDate('date', 'desc'));
    var poids = pourAnimal('poids', a.id).sort(parDate('date', 'asc'));

    var htmlVaccins = vaccins.length ? '<div class="gfc-list">' + vaccins.map(function (v) {
      var st = v.rappel ? statut(v.rappel) : null;
      return ligne({
        titre: esc(v.nom),
        sous: 'Fait le&nbsp;' + dateFr(v.date) + (v.rappel ? '&nbsp;· rappel le&nbsp;' + dateFr(v.rappel) : ''),
        badge: st ? '<span class="gfc-badge gfc-badge--' + st.cls + '">' + st.texte + '</span>' : '',
        actions: boutonsEdit('vaccins', v.id)
      });
    }).join('') + '</div>' : vide('Aucun vaccin noté pour l’instant.');

    var htmlTraitements = traitements.length ? '<div class="gfc-list">' + traitements.map(function (t) {
      var st = t.prochaine ? statut(t.prochaine) : null;
      return ligne({
        titre: esc(t.nom),
        sous: 'Dernière prise&nbsp;: ' + dateFr(t.date) + (t.freq ? '&nbsp;· tous les&nbsp;' + t.freq + '&nbsp;jours' : ''),
        badge: st ? '<span class="gfc-badge gfc-badge--' + st.cls + '">' + st.texte + '</span>' : '',
        actions: '<button type="button" class="gfc-icon-btn" data-act="trait-fait" data-id="' + t.id + '" title="Marquer comme donné aujourd’hui" aria-label="Marquer comme donné aujourd’hui">✅</button>' +
          boutonsEdit('traitements', t.id)
      });
    }).join('') + '</div>' : vide('Antipuces, vermifuge, traitement en cours… notez-les ici pour ne plus les oublier.');

    var htmlVisites = visites.length ? '<div class="gfc-list">' + visites.map(function (v) {
      return ligne({
        titre: esc(v.motif),
        sous: dateFr(v.date) + (v.notes ? '&nbsp;· ' + esc(v.notes) : ''),
        actions: boutonsEdit('visites', v.id)
      });
    }).join('') + '</div>' : vide('Aucune visite enregistrée.');

    var htmlPoids = poids.length
      ? courbePoids(poids) + '<div class="gfc-list" style="margin-top:14px">' + poids.slice().reverse().map(function (p) {
          return ligne({
            titre: String(p.kg).replace('.', ',') + '&nbsp;kg',
            sous: dateFr(p.date),
            actions: boutonsEdit('poids', p.id)
          });
        }).join('') + '</div>'
      : vide('Pesez votre animal régulièrement&nbsp;: la courbe révèle les dérives avant l’œil nu.');

    function bloc(titre, type, contenu, libelle) {
      return '<div class="gfc-card">' +
        '<div class="gfc-sec-head"><h3>' + titre + '</h3>' +
        '<button type="button" class="gfc-btn gfc-btn--sm" data-act="new" data-type="' + type + '">+&nbsp;' + libelle + '</button></div>' +
        contenu + '</div>';
    }

    return '<section class="gfc-sec">' +
      bloc('Vaccins', 'vaccins', htmlVaccins, 'Vaccin') +
      bloc('Traitements &amp; antiparasitaires', 'traitements', htmlTraitements, 'Traitement') +
      bloc('Courbe de poids', 'poids', htmlPoids, 'Pesée') +
      bloc('Visites chez le vétérinaire', 'visites', htmlVisites, 'Visite') +
    '</section>';
  }

  /* Courbe de poids en SVG, sans aucune librairie. */
  function courbePoids(points) {
    if (points.length === 1) {
      return '<p class="gfc-hint">Une seule pesée pour l’instant&nbsp;: ' +
        String(points[0].kg).replace('.', ',') + '&nbsp;kg le&nbsp;' + dateFr(points[0].date) +
        '. Ajoutez-en une deuxième pour voir la courbe.</p>';
    }
    var L = 640, H = 210, mg = { h: 14, b: 30, g: 42, d: 12 };
    var xs = points.map(function (p) { return parseIso(p.date).getTime(); });
    var ys = points.map(function (p) { return Number(p.kg); });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
    var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var marge = (y1 - y0) * 0.15 || Math.max(y1 * 0.08, 0.5);
    y0 = Math.max(0, y0 - marge); y1 = y1 + marge;

    function px(t) { return mg.g + (x1 === x0 ? 0.5 : (t - x0) / (x1 - x0)) * (L - mg.g - mg.d); }
    function py(v) { return mg.h + (1 - (v - y0) / (y1 - y0 || 1)) * (H - mg.h - mg.b); }

    var d = points.map(function (p, i) {
      return (i ? 'L' : 'M') + px(xs[i]).toFixed(1) + ' ' + py(ys[i]).toFixed(1);
    }).join(' ');
    var aire = d + ' L' + px(x1).toFixed(1) + ' ' + (H - mg.b) + ' L' + px(x0).toFixed(1) + ' ' + (H - mg.b) + ' Z';

    var grille = '', etiq = '';
    for (var i = 0; i <= 3; i++) {
      var v = y0 + (y1 - y0) * i / 3, y = py(v);
      grille += '<line class="gfc-chart-grid" x1="' + mg.g + '" y1="' + y.toFixed(1) + '" x2="' + (L - mg.d) + '" y2="' + y.toFixed(1) + '"/>';
      etiq += '<text class="gfc-chart-txt" x="' + (mg.g - 7) + '" y="' + (y + 4).toFixed(1) + '" text-anchor="end">' + v.toFixed(1).replace('.', ',') + '</text>';
    }
    var pts = points.map(function (p, i) {
      return '<circle class="gfc-chart-dot" cx="' + px(xs[i]).toFixed(1) + '" cy="' + py(ys[i]).toFixed(1) + '" r="4"><title>' +
        String(p.kg).replace('.', ',') + ' kg — ' + dateFr(p.date).replace(/&nbsp;/g, ' ') + '</title></circle>';
    }).join('');

    var dg = '<text class="gfc-chart-txt" x="' + mg.g + '" y="' + (H - 9) + '">' + dateFr(points[0].date) + '</text>' +
      '<text class="gfc-chart-txt" x="' + (L - mg.d) + '" y="' + (H - 9) + '" text-anchor="end">' + dateFr(points[points.length - 1].date) + '</text>';

    return '<svg class="gfc-chart" viewBox="0 0 ' + L + ' ' + H + '" role="img" aria-label="Courbe de poids">' +
      grille + '<path class="gfc-chart-area" d="' + aire + '"/><path class="gfc-chart-line" d="' + d + '"/>' +
      pts + etiq + dg + '</svg>';
  }

  /* ---------- Onglet Rappels ---------- */
  function vueRappels() {
    var liste = echeances();
    var faits = etat.rappels.filter(function (r) { return r.fait; }).sort(parDate('date', 'desc'));

    var corps = liste.length ? '<div class="gfc-list">' + liste.map(function (e) {
      var st = statut(e.date);
      var actions = e.type === 'rappel'
        ? '<button type="button" class="gfc-icon-btn" data-act="rappel-fait" data-id="' + e.src.id + '" title="Marquer comme fait" aria-label="Marquer comme fait">✅</button>' + boutonsEdit('rappels', e.src.id)
        : '<button type="button" class="gfc-icon-btn" data-act="goto-sante" data-id="' + e.petId + '" title="Voir dans Santé" aria-label="Voir dans Santé">↗</button>';
      return ligne({
        titre: e.titre,
        sous: esc(nomAnimal(e.petId)) + '&nbsp;· ' + dateFr(e.date),
        badge: '<span class="gfc-badge gfc-badge--' + st.cls + '">' + st.texte + '</span>',
        actions: actions
      });
    }).join('') + '</div>' : vide('Rien à l’horizon. Les rappels de vaccins et de traitements apparaissent ici automatiquement.');

    var htmlFaits = faits.length ? '<div class="gfc-card"><div class="gfc-sec-head"><h3>Déjà fait</h3></div><div class="gfc-list">' +
      faits.slice(0, 12).map(function (r) {
        return ligne({
          titre: esc(r.titre), fait: true,
          sous: esc(nomAnimal(r.petId)) + '&nbsp;· ' + dateFr(r.date),
          badge: '<span class="gfc-badge gfc-badge--done">Fait</span>',
          actions: '<button type="button" class="gfc-icon-btn" data-act="rappel-refait" data-id="' + r.id + '" title="Rouvrir" aria-label="Rouvrir">↩️</button>' +
            '<button type="button" class="gfc-icon-btn" data-act="del" data-type="rappels" data-id="' + r.id + '" title="Supprimer" aria-label="Supprimer">🗑️</button>'
        });
      }).join('') + '</div></div>' : '';

    return '<section class="gfc-sec">' +
      '<div class="gfc-card">' +
        '<div class="gfc-sec-head"><h3>À venir — tous vos animaux</h3>' +
        '<button type="button" class="gfc-btn gfc-btn--sm" data-act="new" data-type="rappels">+&nbsp;Rappel</button></div>' +
        '<p class="gfc-hint">Votre navigateur ne peut pas sonner tout seul. Le bouton <strong>Agenda&nbsp;(.ics)</strong> en bas de page verse ces échéances dans le calendrier de votre téléphone&nbsp;: c’est lui qui vous préviendra, même app fermée.</p>' +
        corps +
      '</div>' + htmlFaits +
    '</section>';
  }

  /* ---------- Onglet Budget ---------- */
  function vueBudget() {
    var dep = etat.depenses.slice().sort(parDate('date', 'desc'));
    var maintenant = aujourdhui();
    var moisCourant = isoJour(maintenant).slice(0, 7);
    var an = maintenant.getFullYear();

    var totalMois = 0, totalAn = 0, total = 0, parCat = {}, parAnimal = {};
    dep.forEach(function (d) {
      var m = Number(d.montant) || 0;
      total += m;
      if ((d.date || '').slice(0, 7) === moisCourant) totalMois += m;
      if ((d.date || '').slice(0, 4) === String(an)) totalAn += m;
      parCat[d.cat] = (parCat[d.cat] || 0) + m;
      parAnimal[d.petId] = (parAnimal[d.petId] || 0) + m;
    });

    var totaux = '<div class="gfc-totals">' +
      '<div class="gfc-total"><span>Ce mois-ci</span><strong>' + euros(totalMois) + '</strong></div>' +
      '<div class="gfc-total gfc-total--soft"><span>Année ' + an + '</span><strong>' + euros(totalAn) + '</strong></div>' +
      '<div class="gfc-total gfc-total--soft"><span>Depuis le début</span><strong>' + euros(total) + '</strong></div>' +
    '</div>';

    var cats = Object.keys(parCat).sort(function (a, b) { return parCat[b] - parCat[a]; });
    var maxCat = cats.length ? parCat[cats[0]] : 0;
    var htmlCats = cats.length ? '<div class="gfc-bars">' + cats.map(function (c) {
      var pc = maxCat ? (parCat[c] / maxCat) * 100 : 0;
      return '<div class="gfc-bar-row"><span>' + esc(c) + '</span>' +
        '<span class="gfc-bar-track"><span class="gfc-bar-fill" style="width:' + pc.toFixed(1) + '%"></span></span>' +
        '<span class="gfc-bar-val">' + euros(parCat[c]) + '</span></div>';
    }).join('') + '</div>' : '';

    var animaux = Object.keys(parAnimal);
    var htmlAnimaux = (etat.animaux.length > 1 && animaux.length) ?
      '<div class="gfc-card"><div class="gfc-sec-head"><h3>Par animal</h3></div><div class="gfc-bars">' +
      animaux.sort(function (a, b) { return parAnimal[b] - parAnimal[a]; }).map(function (id) {
        var pc = total ? (parAnimal[id] / total) * 100 : 0;
        return '<div class="gfc-bar-row"><span>' + esc(nomAnimal(id)) + '</span>' +
          '<span class="gfc-bar-track"><span class="gfc-bar-fill" style="width:' + pc.toFixed(1) + '%"></span></span>' +
          '<span class="gfc-bar-val">' + euros(parAnimal[id]) + '</span></div>';
      }).join('') + '</div></div>' : '';

    var htmlListe = dep.length ? '<div class="gfc-list">' + dep.slice(0, 60).map(function (d) {
      return ligne({
        titre: esc(d.cat) + (d.note ? '&nbsp;— ' + esc(d.note) : ''),
        sous: esc(nomAnimal(d.petId)) + '&nbsp;· ' + dateFr(d.date),
        montant: euros(d.montant),
        actions: boutonsEdit('depenses', d.id)
      });
    }).join('') + '</div>' : vide('Croquettes, véto, jouets… notez une dépense et les totaux se calculent tout seuls.');

    return '<section class="gfc-sec">' + totaux +
      (htmlCats ? '<div class="gfc-card"><div class="gfc-sec-head"><h3>Par catégorie</h3></div>' + htmlCats + '</div>' : '') +
      htmlAnimaux +
      '<div class="gfc-card">' +
        '<div class="gfc-sec-head"><h3>Dépenses</h3>' +
        '<button type="button" class="gfc-btn gfc-btn--sm" data-act="new" data-type="depenses">+&nbsp;Dépense</button></div>' +
        htmlListe +
        (dep.length > 60 ? '<p class="gfc-hint" style="margin-top:12px">Les 60 dernières dépenses sont affichées&nbsp;; les totaux, eux, portent sur la totalité.</p>' : '') +
      '</div>' +
    '</section>';
  }

  /* ---------- Onglet Souvenirs ---------- */
  function vueSouvenirs(a) {
    var liste = pourAnimal('souvenirs', a.id).sort(parDate('date', 'desc'));
    var corps = liste.length ? '<div class="gfc-gallery">' + liste.map(function (s) {
      var img = s.photoId && photos[s.photoId]
        ? '<img src="' + photos[s.photoId] + '" alt="' + esc(s.titre) + '" loading="lazy">'
        : '<div style="aspect-ratio:1/1;display:grid;place-items:center;font-size:34px;background:var(--gfc-beige)">' + emoji(a.espece) + '</div>';
      return '<figure class="gfc-memo" style="margin:0">' + img +
        '<figcaption class="gfc-memo-body">' +
          '<div class="gfc-memo-title">' + esc(s.titre) + '</div>' +
          '<div class="gfc-memo-date">' + dateFr(s.date) + '</div>' +
          '<div class="gfc-row-act" style="margin-top:6px">' + boutonsEdit('souvenirs', s.id) + '</div>' +
        '</figcaption></figure>';
    }).join('') + '</div>' : vide('La première promenade, le jour de l’adoption, l’ordonnance du véto&nbsp;: gardez-les ici.');

    return '<section class="gfc-sec"><div class="gfc-card">' +
      '<div class="gfc-sec-head"><h3>Souvenirs de&nbsp;' + esc(a.nom) + '</h3>' +
      '<button type="button" class="gfc-btn gfc-btn--sm" data-act="new" data-type="souvenirs">+&nbsp;Souvenir</button></div>' +
      '<p class="gfc-hint">Les photos sont réduites puis rangées dans cet appareil. Pensez à exporter votre sauvegarde&nbsp;: vider les données du navigateur les effacerait.</p>' +
      corps + '</div></section>';
  }

  /* ================= Formulaires ================= */

  var photoEnCours = null; // dataURL choisie dans la modale ouverte

  var SCHEMAS = {
    animaux: {
      titre: 'Fiche de l’animal',
      champs: [
        { k: 'nom', l: 'Nom', t: 'text', requis: true },
        { k: 'espece', l: 'Espèce', t: 'select', options: ESPECES, moitie: true },
        { k: 'sexe', l: 'Sexe', t: 'select', options: ['', 'Mâle', 'Femelle'], moitie: true },
        { k: 'race', l: 'Race', t: 'text', moitie: true },
        { k: 'naissance', l: 'Date de naissance', t: 'date', moitie: true },
        { k: 'sterilise', l: 'Stérilisé', t: 'select', options: ['', 'Oui', 'Non'], moitie: true },
        { k: 'puce', l: 'N° de puce ou tatouage', t: 'text', moitie: true },
        { k: 'vetoNom', l: 'Vétérinaire', t: 'text', moitie: true },
        { k: 'vetoTel', l: 'Téléphone du vétérinaire', t: 'tel', moitie: true },
        { k: 'notes', l: 'Notes (allergies, caractère, régime…)', t: 'textarea' },
        { k: 'photo', l: 'Photo', t: 'photo' }
      ]
    },
    vaccins: {
      titre: 'Vaccin', animal: true,
      champs: [
        { k: 'nom', l: 'Vaccin', t: 'text', requis: true, note: 'Ex.&nbsp;: CHPPiL, rage, leucose…' },
        { k: 'date', l: 'Fait le', t: 'date', requis: true, moitie: true },
        { k: 'rappel', l: 'Prochain rappel', t: 'date', moitie: true }
      ]
    },
    traitements: {
      titre: 'Traitement / antiparasitaire', animal: true,
      champs: [
        { k: 'nom', l: 'Produit', t: 'text', requis: true, note: 'Ex.&nbsp;: pipette antipuces, vermifuge…' },
        { k: 'date', l: 'Dernière prise', t: 'date', requis: true, moitie: true },
        { k: 'freq', l: 'Tous les… (jours)', t: 'number', moitie: true, note: 'Mensuel&nbsp;= 30, trimestriel&nbsp;= 90.' },
        { k: 'prochaine', l: 'Prochaine prise', t: 'date', note: 'Laissez vide&nbsp;: elle sera calculée à partir de la fréquence.' }
      ]
    },
    poids: {
      titre: 'Pesée', animal: true,
      champs: [
        { k: 'date', l: 'Date', t: 'date', requis: true, moitie: true },
        { k: 'kg', l: 'Poids (kg)', t: 'number', requis: true, pas: '0.01', moitie: true }
      ]
    },
    visites: {
      titre: 'Visite vétérinaire', animal: true,
      champs: [
        { k: 'motif', l: 'Motif', t: 'text', requis: true },
        { k: 'date', l: 'Date', t: 'date', requis: true },
        { k: 'notes', l: 'Compte rendu, ordonnance…', t: 'textarea' }
      ]
    },
    rappels: {
      titre: 'Rappel', animal: true, choixAnimal: true,
      champs: [
        { k: 'titre', l: 'Intitulé', t: 'text', requis: true, note: 'Ex.&nbsp;: griffes à couper, rendez-vous toiletteur…' },
        { k: 'date', l: 'Date', t: 'date', requis: true }
      ]
    },
    depenses: {
      titre: 'Dépense', animal: true, choixAnimal: true,
      champs: [
        { k: 'cat', l: 'Catégorie', t: 'select', options: CATEGORIES, requis: true, moitie: true },
        { k: 'montant', l: 'Montant (€)', t: 'number', requis: true, pas: '0.01', moitie: true },
        { k: 'date', l: 'Date', t: 'date', requis: true },
        { k: 'note', l: 'Détail', t: 'text' }
      ]
    },
    souvenirs: {
      titre: 'Souvenir', animal: true,
      champs: [
        { k: 'titre', l: 'Titre', t: 'text', requis: true },
        { k: 'date', l: 'Date', t: 'date', requis: true },
        { k: 'photo', l: 'Photo ou document', t: 'photo' }
      ]
    }
  };

  function champHtml(c, val) {
    var id = 'gfc-f-' + c.k;
    var lab = '<label for="' + id + '">' + c.l + (c.requis ? '&nbsp;*' : '') + '</label>';
    var note = c.note ? '<div class="gfc-field-note">' + c.note + '</div>' : '';
    var corps;

    if (c.t === 'select') {
      corps = '<select id="' + id + '" name="' + c.k + '">' + c.options.map(function (o) {
        return '<option value="' + esc(o) + '"' + (String(val || '') === o ? ' selected' : '') + '>' +
          (o === '' ? '—' : esc(o)) + '</option>';
      }).join('') + '</select>';
    } else if (c.t === 'textarea') {
      corps = '<textarea id="' + id + '" name="' + c.k + '">' + esc(val || '') + '</textarea>';
    } else if (c.t === 'photo') {
      var apercu = photoEnCours || '';
      corps = '<div class="gfc-photo-pick">' +
        '<img class="gfc-photo-prev" data-gfc-prev alt="" src="' + (apercu || 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==') + '">' +
        '<div><input type="file" id="' + id + '" name="' + c.k + '" accept="image/*" data-gfc-photo>' +
        (apercu ? '<button type="button" class="gfc-btn gfc-btn--sm gfc-btn--danger" data-act="photo-clear" style="margin-top:8px">Retirer la photo</button>' : '') +
        '</div></div>';
    } else if (c.t === 'number') {
      // Volontairement type="text" : un input[type=number] renvoie une valeur VIDE
      // dès que l'on saisit « 62,90 ». Or c'est ce que tape un francophone.
      // inputmode="decimal" conserve le pavé numérique sur mobile, et on parse
      // la virgule comme le point à la validation.
      corps = '<input type="text" inputmode="decimal" id="' + id + '" name="' + c.k + '"' +
        ' value="' + esc(val == null ? '' : String(val).replace('.', ',')) + '">';
    } else {
      corps = '<input type="' + c.t + '" id="' + id + '" name="' + c.k + '"' +
        ' value="' + esc(val == null ? '' : val) + '">';
    }
    return '<div class="gfc-field' + (c.moitie ? ' gfc-field--half' : '') + '">' + lab + corps + note + '</div>';
  }

  /* Regroupe les champs « moitié » consécutifs deux par deux. */
  function champsHtml(champs, valeurs) {
    var out = '', i = 0;
    while (i < champs.length) {
      var c = champs[i];
      if (c.moitie && champs[i + 1] && champs[i + 1].moitie) {
        out += '<div class="gfc-field--row">' +
          champHtml(c, valeurs[c.k]) + champHtml(champs[i + 1], valeurs[champs[i + 1].k]) + '</div>';
        i += 2;
      } else {
        out += champHtml(c, valeurs[c.k]);
        i += 1;
      }
    }
    return out;
  }

  function ouvreForm(type, id) {
    var sch = SCHEMAS[type];
    if (!sch) return;
    var liste = type === 'animaux' ? etat.animaux : etat[type];
    var obj = id ? liste.filter(function (x) { return x.id === id; })[0] : null;
    var val = obj ? JSON.parse(JSON.stringify(obj)) : {};

    if (!obj) {
      if (SCHEMAS[type].champs.some(function (c) { return c.k === 'date'; })) val.date = isoJour(aujourdhui());
      if (type === 'animaux') val.espece = 'Chien';
      if (type === 'depenses') val.cat = 'Alimentation';
    }
    photoEnCours = obj && obj.photoId ? (photos[obj.photoId] || null) : null;

    var choix = '';
    if (sch.choixAnimal && etat.animaux.length > 1) {
      var courant = val.petId || animalActif;
      choix = '<div class="gfc-field"><label for="gfc-f-petId">Animal concerné</label>' +
        '<select id="gfc-f-petId" name="petId">' + etat.animaux.map(function (a) {
          return '<option value="' + a.id + '"' + (a.id === courant ? ' selected' : '') + '>' + esc(a.nom) + '</option>';
        }).join('') + '</select></div>';
    }

    var html = '<div class="gfc-modal-box" role="dialog" aria-modal="true" aria-labelledby="gfc-modal-t">' +
      '<h2 id="gfc-modal-t">' + (obj ? 'Modifier' : 'Ajouter') + '&nbsp;— ' + sch.titre + '</h2>' +
      '<form data-gfc-form data-type="' + type + '" data-id="' + (id || '') + '" novalidate>' +
        choix + champsHtml(sch.champs, val) +
        '<div class="gfc-field-err" data-gfc-err hidden></div>' +
        '<div class="gfc-modal-foot">' +
          (obj ? '<button type="button" class="gfc-btn gfc-btn--sm gfc-btn--danger" data-act="del" data-type="' + type + '" data-id="' + id + '">Supprimer</button>' : '') +
          '<button type="button" class="gfc-btn gfc-btn--sm" data-act="modal-close">Annuler</button>' +
          '<button type="submit" class="gfc-btn gfc-btn--sm gfc-btn--primary">Enregistrer</button>' +
        '</div>' +
      '</form></div>';

    var m = $('[data-gfc-modal]');
    m.innerHTML = html;
    m.hidden = false;
    var premier = m.querySelector('input, select, textarea');
    if (premier) premier.focus();
  }

  function fermeModal() {
    var m = $('[data-gfc-modal]');
    m.hidden = true;
    m.innerHTML = '';
    photoEnCours = null;
  }

  var enregistrementEnCours = false;

  function soumetForm(form) {
    if (enregistrementEnCours) return; // double-clic sur « Enregistrer »
    var type = form.getAttribute('data-type');
    var id = form.getAttribute('data-id');
    var sch = SCHEMAS[type];
    var err = form.querySelector('[data-gfc-err]');
    var donnees = {};

    for (var i = 0; i < sch.champs.length; i++) {
      var c = sch.champs[i];
      if (c.t === 'photo') continue;
      var el = form.querySelector('[name="' + c.k + '"]');
      var v = el ? String(el.value).trim() : '';
      if (c.requis && !v) {
        err.innerHTML = 'Le champ «&nbsp;' + c.l + '&nbsp;» est obligatoire.';
        err.hidden = false;
        if (el) el.focus();
        return;
      }
      if (c.t === 'number' && v) {
        // « 62,90 », « 62.90 », « 62,90 € », « 1 250 » : tout doit passer.
        v = v.replace(/[\s €]/g, '').replace(',', '.');
        if (v === '' || isNaN(Number(v)) || Number(v) < 0) {
          err.innerHTML = 'Le champ «&nbsp;' + c.l + '&nbsp;» attend un nombre positif.';
          err.hidden = false;
          if (el) el.focus();
          return;
        }
        v = Number(v);
      }
      donnees[c.k] = v;
    }

    var selAnimal = form.querySelector('[name="petId"]');
    if (type !== 'animaux') {
      donnees.petId = selAnimal ? selAnimal.value : (id ? (etat[type].filter(function (x) { return x.id === id; })[0] || {}).petId : animalActif);
      if (!donnees.petId) donnees.petId = animalActif;
    }

    // Prochaine prise calculée si on ne l'a pas saisie
    if (type === 'traitements' && !donnees.prochaine && donnees.freq) {
      donnees.prochaine = ajouteJours(donnees.date, Number(donnees.freq));
    }

    var cible = type === 'animaux' ? etat.animaux : etat[type];
    var obj = id ? cible.filter(function (x) { return x.id === id; })[0] : null;

    var aPhoto = sch.champs.some(function (c) { return c.t === 'photo'; });
    var tachePhoto = Promise.resolve();

    if (obj) {
      Object.keys(donnees).forEach(function (k) { obj[k] = donnees[k]; });
    } else {
      obj = donnees;
      obj.id = uid();
      cible.push(obj);
    }

    if (aPhoto) {
      if (photoEnCours) {
        var pid = obj.photoId || uid();
        obj.photoId = pid;
        tachePhoto = photoEcrit(pid, photoEnCours);
      } else if (obj.photoId) {
        tachePhoto = photoSupprime(obj.photoId);
        delete obj.photoId;
      }
    }

    if (type === 'animaux' && !animalActif) animalActif = obj.id;
    if (type === 'animaux') animalActif = obj.id;

    enregistrementEnCours = true;
    var valider = form.querySelector('button[type="submit"]');
    if (valider) valider.disabled = true;

    tachePhoto.then(function () {
      sauve();
      fermeModal();
      rendu();
      toast('Enregistré.');
    })['catch'](function (e) {
      console.warn('[carnet] enregistrement incomplet', e);
      toast('L’enregistrement a échoué. Réessayez.', 5000);
    }).then(function () { enregistrementEnCours = false; });
  }

  function supprime(type, id) {
    var cible = type === 'animaux' ? etat.animaux : etat[type];
    var obj = cible.filter(function (x) { return x.id === id; })[0];
    if (!obj) return;

    var question = type === 'animaux'
      ? 'Supprimer ' + obj.nom + ' et TOUT son carnet (santé, dépenses, souvenirs) ? Cette action est définitive.'
      : 'Supprimer cet élément ? Cette action est définitive.';
    if (!window.confirm(question)) return;

    var aSupprimer = [];
    if (obj.photoId) aSupprimer.push(obj.photoId);

    if (type === 'animaux') {
      ['vaccins', 'traitements', 'poids', 'visites', 'rappels', 'depenses', 'souvenirs'].forEach(function (k) {
        etat[k] = etat[k].filter(function (x) {
          if (x.petId === id) { if (x.photoId) aSupprimer.push(x.photoId); return false; }
          return true;
        });
      });
      etat.animaux = etat.animaux.filter(function (x) { return x.id !== id; });
      if (animalActif === id) animalActif = etat.animaux.length ? etat.animaux[0].id : null;
    } else {
      etat[type] = etat[type].filter(function (x) { return x.id !== id; });
    }

    Promise.all(aSupprimer.map(photoSupprime)).then(function () {
      sauve();
      fermeModal();
      rendu();
      toast('Supprimé.');
    });
  }

  /* ================= Outils : sauvegarde, agenda, PDF, partage ================= */

  function telecharge(nom, contenu, mime) {
    var blob = new Blob([contenu], { type: mime || 'application/octet-stream' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = nom;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }

  function exporte() {
    var paquet = JSON.parse(JSON.stringify(etat));
    paquet.photos = photos;
    paquet.exportLe = new Date().toISOString();
    telecharge('carnet-gus-et-frost-' + isoJour(aujourdhui()) + '.json',
      JSON.stringify(paquet), 'application/json');
    toast('Sauvegarde téléchargée. Rangez-la ailleurs que sur le téléphone.', 5000);
  }

  function importe(file) {
    var fr = new FileReader();
    fr.onload = function () {
      var d;
      try { d = JSON.parse(fr.result); } catch (e) {
        return toast('Ce fichier n’est pas une sauvegarde valide.', 5000);
      }
      if (!d || !Array.isArray(d.animaux)) {
        return toast('Ce fichier n’est pas une sauvegarde du Carnet.', 5000);
      }
      if (!window.confirm('Remplacer le carnet actuel par cette sauvegarde ? Le contenu présent sur cet appareil sera écrasé.')) return;

      var lot = d.photos || {};
      var vide2 = etatVide();
      Object.keys(vide2).forEach(function (k) {
        if (k !== 'v') etat[k] = Array.isArray(d[k]) ? d[k] : [];
      });
      animalActif = etat.animaux.length ? etat.animaux[0].id : null;

      Promise.all(Object.keys(lot).map(function (id) { return photoEcrit(id, lot[id]); }))
        .then(function () {
          sauve();
          rendu();
          toast('Sauvegarde restaurée.');
        });
    };
    fr.readAsText(file);
  }

  function echapIcs(s) {
    return String(s).replace(/&nbsp;/g, ' ').replace(/\\/g, '\\\\')
      .replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');
  }

  /* RFC 5545 : une ligne ne dépasse pas 75 octets ; au-delà on replie avec
     un retour + une espace. On compte en octets (UTF-8), pas en caractères,
     sinon les accents font sauter la limite chez les clients stricts. */
  function plieIcs(ligne) {
    var enc = new TextEncoder();
    if (enc.encode(ligne).length <= 75) return ligne;
    var out = '', courant = '', limite = 74; // 1 octet gardé pour l'espace de continuation
    for (var i = 0; i < ligne.length; i++) {
      var c = ligne[i];
      if (enc.encode(courant + c).length > limite) {
        out += (out ? '\r\n ' : '') + courant;
        courant = '';
        limite = 73;
      }
      courant += c;
    }
    return out + (out ? '\r\n ' : '') + courant;
  }

  function exporteIcs() {
    var liste = echeances();
    if (!liste.length) return toast('Aucune échéance à exporter pour l’instant.');

    var l = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Gus et Frost//Le Carnet//FR', 'CALSCALE:GREGORIAN'];
    var horodatage = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

    liste.forEach(function (e) {
      var d = parseIso(e.date);
      if (!d) return;
      var debut = isoJour(d).replace(/-/g, '');
      var fin = ajouteJours(e.date, 1).replace(/-/g, '');
      var titre = echapIcs(e.titre.replace(/<[^>]+>/g, '')) + ' — ' + echapIcs(nomAnimal(e.petId));
      l.push('BEGIN:VEVENT',
        'UID:' + (e.src.id || uid()) + '@gus-et-frost',
        'DTSTAMP:' + horodatage,
        'DTSTART;VALUE=DATE:' + debut,
        'DTEND;VALUE=DATE:' + fin,
        'SUMMARY:' + titre,
        'DESCRIPTION:' + echapIcs('Échéance notée dans Le Carnet de Gus & Frost.'),
        'BEGIN:VALARM', 'TRIGGER:-P1D', 'ACTION:DISPLAY',
        'DESCRIPTION:' + titre, 'END:VALARM',
        'END:VEVENT');
    });
    l.push('END:VCALENDAR');

    telecharge('rappels-carnet-' + isoJour(aujourdhui()) + '.ics',
      l.map(plieIcs).join('\r\n'), 'text/calendar');
    toast('Fichier agenda téléchargé&nbsp;: ouvrez-le pour l’ajouter à votre calendrier.', 6000);
  }

  function tableau(entetes, lignes) {
    if (!lignes.length) return '<p>—</p>';
    return '<table><thead><tr>' + entetes.map(function (h) { return '<th>' + h + '</th>'; }).join('') +
      '</tr></thead><tbody>' + lignes.map(function (r) {
        return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody></table>';
  }

  function imprime() {
    if (!etat.animaux.length) return toast('Ajoutez d’abord un animal.');

    var html = etat.animaux.map(function (a) {
      var vaccins = pourAnimal('vaccins', a.id).sort(parDate('date', 'desc'));
      var traitements = pourAnimal('traitements', a.id).sort(parDate('date', 'desc'));
      var visites = pourAnimal('visites', a.id).sort(parDate('date', 'desc'));
      var poids = pourAnimal('poids', a.id).sort(parDate('date', 'desc'));
      var ag = age(a.naissance);

      return '<div class="gfc-print-pet">' +
        '<h1>' + esc(a.nom) + '</h1>' +
        '<p class="gfc-print-sub">' +
          [a.espece, a.race, a.sexe].filter(Boolean).map(esc).join(' · ') +
          (ag ? ' · ' + ag.replace(/&nbsp;/g, ' ') : '') +
          (a.naissance ? ' · né(e) le ' + dateFr(a.naissance).replace(/&nbsp;/g, ' ') : '') +
        '</p>' +

        '<h2>Identité</h2>' +
        tableau(['Rubrique', 'Valeur'], [
          ['Stérilisé', esc(a.sterilise || '—')],
          ['Puce / tatouage', esc(a.puce || '—')],
          ['Vétérinaire', esc(a.vetoNom || '—') + (a.vetoTel ? ' — ' + esc(a.vetoTel) : '')],
          ['Poids le plus récent', poids[0] ? String(poids[0].kg).replace('.', ',') + ' kg (' + dateFr(poids[0].date).replace(/&nbsp;/g, ' ') + ')' : '—'],
          ['Notes', esc(a.notes || '—')]
        ]) +

        '<h2>Vaccins</h2>' +
        tableau(['Vaccin', 'Fait le', 'Rappel prévu'], vaccins.map(function (v) {
          return [esc(v.nom), dateFr(v.date).replace(/&nbsp;/g, ' '), v.rappel ? dateFr(v.rappel).replace(/&nbsp;/g, ' ') : '—'];
        })) +

        '<h2>Traitements &amp; antiparasitaires</h2>' +
        tableau(['Produit', 'Dernière prise', 'Fréquence', 'Prochaine'], traitements.map(function (t) {
          return [esc(t.nom), dateFr(t.date).replace(/&nbsp;/g, ' '),
            t.freq ? t.freq + ' j' : '—', t.prochaine ? dateFr(t.prochaine).replace(/&nbsp;/g, ' ') : '—'];
        })) +

        '<h2>Suivi du poids</h2>' +
        tableau(['Date', 'Poids'], poids.slice(0, 20).map(function (p) {
          return [dateFr(p.date).replace(/&nbsp;/g, ' '), String(p.kg).replace('.', ',') + ' kg'];
        })) +

        '<h2>Visites vétérinaires</h2>' +
        tableau(['Date', 'Motif', 'Notes'], visites.map(function (v) {
          return [dateFr(v.date).replace(/&nbsp;/g, ' '), esc(v.motif), esc(v.notes || '—')];
        })) +

        '<p class="gfc-print-foot">Carnet établi le ' +
          new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' }) +
          ' avec Le Carnet de Gus &amp; Frost. Document tenu par le propriétaire, sans valeur vétérinaire officielle.</p>' +
      '</div>';
    }).join('');

    var hote = document.createElement('div');
    hote.className = 'gfc-print-host';
    hote.innerHTML = '<div class="gfc-print">' + html + '</div>';
    document.body.appendChild(hote);

    var nettoie = function () {
      hote.remove();
      window.removeEventListener('afterprint', nettoie);
    };
    window.addEventListener('afterprint', nettoie);
    window.print();
    setTimeout(nettoie, 60000); // filet de sécurité si afterprint ne se déclenche pas
  }

  /* --- Partage : la fiche santé compressée dans l'URL, sans serveur --- */

  function b64Encode(str) {
    var octets = new TextEncoder().encode(str);
    var bin = '';
    octets.forEach(function (o) { bin += String.fromCharCode(o); });
    return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }

  function b64Decode(s) {
    var b = s.replace(/-/g, '+').replace(/_/g, '/');
    while (b.length % 4) b += '=';
    var bin = atob(b);
    var octets = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) octets[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(octets);
  }

  function partage() {
    var a = animalCourant();
    if (!a) return toast('Ajoutez d’abord un animal.');

    var paquet = {
      a: { nom: a.nom, espece: a.espece, race: a.race, sexe: a.sexe, naissance: a.naissance,
           sterilise: a.sterilise, puce: a.puce, vetoNom: a.vetoNom, vetoTel: a.vetoTel, notes: a.notes },
      v: pourAnimal('vaccins', a.id).map(function (v) { return [v.nom, v.date, v.rappel || '']; }),
      t: pourAnimal('traitements', a.id).map(function (t) { return [t.nom, t.date, t.freq || '', t.prochaine || '']; }),
      p: pourAnimal('poids', a.id).sort(parDate('date', 'asc')).map(function (p) { return [p.date, p.kg]; }),
      s: pourAnimal('visites', a.id).map(function (v) { return [v.date, v.motif, v.notes || '']; })
    };

    var lien = location.origin + location.pathname + '#fiche=' + b64Encode(JSON.stringify(paquet));
    if (lien.length > MAX_PARTAGE) {
      return toast('La fiche est trop fournie pour tenir dans un lien. Utilisez plutôt <strong>Carnet&nbsp;PDF</strong>&nbsp;: il s’envoie par mail sans limite.', 8000);
    }

    if (navigator.share) {
      navigator.share({ title: 'Carnet de ' + a.nom, text: 'La fiche santé de ' + a.nom, url: lien })
        .catch(function () {});
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(lien).then(function () {
        toast('Lien copié&nbsp;! Collez-le dans un message&nbsp;: la fiche s’ouvre sans compte.', 6000);
      }).catch(function () { window.prompt('Copiez ce lien :', lien); });
      return;
    }
    window.prompt('Copiez ce lien :', lien);
  }

  function vueFichePartagee(p) {
    var a = p.a || {};
    var ag = age(a.naissance);
    function bloc(titre, contenu) {
      return '<div class="gfc-card"><div class="gfc-sec-head"><h3>' + titre + '</h3></div>' + contenu + '</div>';
    }
    function liste(items) {
      return items.length ? '<div class="gfc-list">' + items.join('') + '</div>' : vide('Rien de noté.');
    }

    var vaccins = liste((p.v || []).map(function (v) {
      return ligne({ titre: esc(v[0]), sous: 'Fait le&nbsp;' + dateFr(v[1]) + (v[2] ? '&nbsp;· rappel le&nbsp;' + dateFr(v[2]) : '') });
    }));
    var traitements = liste((p.t || []).map(function (t) {
      return ligne({ titre: esc(t[0]), sous: 'Dernière prise&nbsp;: ' + dateFr(t[1]) + (t[3] ? '&nbsp;· prochaine le&nbsp;' + dateFr(t[3]) : '') });
    }));
    var visites = liste((p.s || []).map(function (v) {
      return ligne({ titre: esc(v[1]), sous: dateFr(v[0]) + (v[2] ? '&nbsp;· ' + esc(v[2]) : '') });
    }));
    var poids = (p.p || []).map(function (x) { return { date: x[0], kg: x[1] }; });

    return '<div class="gfc-shared-note">Vous consultez la fiche de <strong>' + esc(a.nom || 'cet animal') +
      '</strong>, partagée en lecture seule. Rien n’a été enregistré sur un serveur&nbsp;: tout est contenu dans le lien lui-même.</div>' +
      '<div class="gfc-card"><div class="gfc-id">' +
        '<span class="gfc-id-photo">' + emoji(a.espece) + '</span>' +
        '<div class="gfc-id-body"><h2>' + esc(a.nom || '—') + '</h2>' +
        '<p class="gfc-id-meta">' + [a.espece, a.race, a.sexe].filter(Boolean).map(esc).join('&nbsp;· ') + '</p>' +
        '<dl class="gfc-facts">' +
          '<div class="gfc-fact"><dt>Âge</dt><dd>' + (ag || '—') + '</dd></div>' +
          '<div class="gfc-fact"><dt>Puce</dt><dd>' + esc(a.puce || '—') + '</dd></div>' +
          '<div class="gfc-fact"><dt>Vétérinaire</dt><dd>' + esc(a.vetoNom || '—') + '</dd></div>' +
        '</dl>' + (a.notes ? '<p style="margin-top:12px"><strong>Notes&nbsp;:</strong> ' + esc(a.notes) + '</p>' : '') +
      '</div></div></div>' +
      bloc('Vaccins', vaccins) +
      bloc('Traitements', traitements) +
      bloc('Poids', poids.length ? courbePoids(poids) : vide('Aucune pesée.')) +
      bloc('Visites vétérinaires', visites) +
      '<p style="text-align:center;margin-top:24px">' +
        '<a class="gfc-btn gfc-btn--primary" href="' + esc(location.pathname) + '">Créer mon propre carnet, gratuitement</a></p>';
  }

  function raz() {
    if (!window.confirm('Effacer tout le carnet de cet appareil ? Exportez d’abord votre sauvegarde si vous voulez la garder.')) return;
    if (!window.confirm('Dernière confirmation : tout sera perdu définitivement.')) return;
    var ids = Object.keys(photos);
    Promise.all(ids.map(photoSupprime)).then(function () {
      etat = etatVide();
      animalActif = null;
      ongletActif = 'identite';
      localStorage.removeItem(CLE);
      rendu();
      toast('Carnet effacé.');
    });
  }

  /* ================= Message flottant ================= */

  var minuteurToast = null;
  function toast(html, duree) {
    var t = $('[data-gfc-toast]');
    if (!t) return;
    t.innerHTML = html;
    t.hidden = false;
    clearTimeout(minuteurToast);
    minuteurToast = setTimeout(function () { t.hidden = true; }, duree || 3200);
  }

  /* ================= Événements ================= */

  function branche() {
    racine.addEventListener('click', function (ev) {
      var el = ev.target.closest('[data-act], [data-gfc-tab]');
      if (!el || !racine.contains(el)) return;

      var tab = el.getAttribute('data-gfc-tab');
      if (tab) {
        ongletActif = tab;
        rendu();
        return;
      }

      var act = el.getAttribute('data-act');
      var type = el.getAttribute('data-type');
      var id = el.getAttribute('data-id');

      switch (act) {
        case 'pet-pick': animalActif = id; rendu(); break;
        case 'pet-new': ouvreForm('animaux', null); break;
        case 'pet-edit': ouvreForm('animaux', animalActif); break;
        case 'new': ouvreForm(type, null); break;
        case 'edit': ouvreForm(type, id); break;
        case 'del': supprime(type, id); break;
        case 'modal-close': fermeModal(); break;
        case 'photo-clear':
          photoEnCours = null;
          var prev = racine.querySelector('[data-gfc-prev]');
          if (prev) prev.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
          el.remove();
          break;
        case 'goto-sante': animalActif = id; ongletActif = 'sante'; rendu(); break;
        case 'rappel-fait': basculeRappel(id, true); break;
        case 'rappel-refait': basculeRappel(id, false); break;
        case 'trait-fait': traitementFait(id); break;
        case 'export': exporte(); break;
        case 'import': $('[data-gfc-import]').click(); break;
        case 'ics': exporteIcs(); break;
        case 'print': imprime(); break;
        case 'share': partage(); break;
        case 'raz': raz(); break;
      }
    });

    racine.addEventListener('submit', function (ev) {
      var f = ev.target.closest('[data-gfc-form]');
      if (!f) return;
      ev.preventDefault();
      soumetForm(f);
    });

    racine.addEventListener('change', function (ev) {
      if (ev.target.matches('[data-gfc-photo]')) {
        var file = ev.target.files && ev.target.files[0];
        if (!file) return;
        redimensionne(file).then(function (dataUrl) {
          photoEnCours = dataUrl;
          var prev = racine.querySelector('[data-gfc-prev]');
          if (prev) prev.src = dataUrl;
        }).catch(function (e) { toast(esc(e.message)); });
      }
      if (ev.target.matches('[data-gfc-import]')) {
        var f2 = ev.target.files && ev.target.files[0];
        if (f2) importe(f2);
        ev.target.value = '';
      }
    });

    // Clic sur le voile de la modale + touche Échap
    racine.addEventListener('mousedown', function (ev) {
      if (ev.target.matches('[data-gfc-modal]')) fermeModal();
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') {
        var m = $('[data-gfc-modal]');
        if (m && !m.hidden) fermeModal();
      }
    });
  }

  function basculeRappel(id, fait) {
    var r = etat.rappels.filter(function (x) { return x.id === id; })[0];
    if (!r) return;
    r.fait = !!fait;
    sauve();
    rendu();
  }

  function traitementFait(id) {
    var t = etat.traitements.filter(function (x) { return x.id === id; })[0];
    if (!t) return;
    t.date = isoJour(aujourdhui());
    t.prochaine = t.freq ? ajouteJours(t.date, Number(t.freq)) : '';
    sauve();
    rendu();
    toast(t.prochaine
      ? 'Noté. Prochaine prise le&nbsp;' + dateFr(t.prochaine) + '.'
      : 'Noté pour aujourd’hui.');
  }

  /* ================= Démarrage ================= */

  function affiche(sel, visible) {
    var el = $(sel);
    if (el) el.hidden = !visible;
  }

  /* Décide quoi montrer selon l'URL : fiche partagée (lecture seule) ou carnet.
     Appelée au démarrage ET à chaque changement de hash — un lien de partage
     ouvert alors que la page est déjà affichée ne recharge pas le document. */
  function appliqueRoute() {
    var m = /[#&]fiche=([^&]+)/.exec(location.hash);
    if (m) {
      try {
        var p = JSON.parse(b64Decode(m[1]));
        modeLecture = true;
        affiche('[data-gfc-petbar]', false);
        affiche('[data-gfc-tablist]', false);
        affiche('[data-gfc-tools]', false);
        $('[data-gfc-panels]').innerHTML = vueFichePartagee(p);
        return;
      } catch (e) {
        toast('Ce lien de partage est illisible ou incomplet.', 5000);
      }
    }
    modeLecture = false;
    affiche('[data-gfc-petbar]', true);
    affiche('[data-gfc-tablist]', true);
    affiche('[data-gfc-tools]', true);
    rendu();
  }

  var routeBranchee = false;

  function init(el) {
    racine = el;
    etat = charge();
    animalActif = etat.animaux.length ? etat.animaux[0].id : null;

    if (!el.getAttribute('data-gfc-pret')) {
      branche();
      el.setAttribute('data-gfc-pret', '1');
    }
    if (!routeBranchee) {
      window.addEventListener('hashchange', appliqueRoute);
      routeBranchee = true;
    }

    appliqueRoute();                 // affichage immédiat, sans attendre les photos
    photosCharge().then(function () { // puis on repasse avec les images
      if (!modeLecture) rendu();
    });
  }

  window.GFCarnet = { init: init };
})();
