/**
 * Accusé de réception automatique — formulaire « Nous contacter » (gusetfrost.fr)
 *
 * Où il tourne : Google Apps Script, dans le compte contact@gusetfrost.fr
 * (projet « Accusé de réception – formulaire contact »). Ce fichier en est la
 * copie versionnée : toute modification se fait ici PUIS se recolle là-bas.
 *
 * Pourquoi (13/09/2026) : le formulaire Shopify prévient la boutique mais
 * n'envoie RIEN au client, et aucun réglage ne l'active. Un accusé qui arrive
 * dans la minute permet au client de le chercher dans ses indésirables tout de
 * suite — et de savoir où trouver notre vraie réponse.
 *
 * Fonctionnement : toutes les minutes, `traiter()` cherche les e-mails
 * « formulaire de contact » envoyés par Shopify, lit l'adresse du client dans
 * la ligne « E-mail: », lui envoie l'accusé DEPUIS contact@ (adresse
 * authentifiée DKIM, meilleure délivrabilité que Shopify ou Klaviyo), puis pose
 * l'étiquette « Contact/Accusé envoyé » sur le fil pour ne jamais renvoyer.
 *
 * Garde-fous :
 *   - jamais d'envoi vers une adresse @gusetfrost.fr (pas de boucle) ;
 *   - un seul accusé par adresse sur 6 h (CacheService) : un robot qui passerait
 *     le captcha avec l'adresse d'un tiers ne peut pas le bombarder ;
 *   - `installer()` marque comme traités les messages DÉJÀ présents : la mise
 *     en route n'envoie rien à personne.
 *
 * Mise en route : exécuter `installer()` une fois (Google demande alors
 * l'autorisation d'envoyer des e-mails — à accepter par le titulaire du compte).
 */

var EXPEDITEUR_SHOPIFY = 'mailer@shopify.com';
var LIBELLE_FAIT = 'Contact/Accusé envoyé';
var NOM_EXPEDITEUR = 'Gus et Frost';
var ADRESSE_REPONSE = 'contact@gusetfrost.fr';
var REQUETE = 'from:' + EXPEDITEUR_SHOPIFY + ' "formulaire de contact" newer_than:2d';

// Étiquettes des champs telles que Shopify les écrit dans l'e-mail reçu (il met
// une majuscule à chaque mot : d'où les anciennes variantes, gardées au cas où).
var ETIQUETTES = ['Indicatif de pays', 'Motif', 'Commande', 'Numéro De Commande',
                  'Nom', 'E-mail', 'Téléphone', 'Message', 'Corps'];

// Valeur envoyée par le formulaire -> formulation reprise dans l'accusé (les
// mêmes mots que les cartes à cocher de la page).
var MOTIFS = {
  'Retour ou échange': 'un retour ou un échange',
  'Retour Ou Échange': 'un retour ou un échange',
  'Question sur une commande': 'une commande en cours',
  'Question Sur Une Commande': 'une commande en cours',
  'Autre question': 'une autre question',
  'Autre Question': 'une autre question'
};

var NBSP = '\u00a0';

/** Tâche planifiée : une passe toutes les minutes. */
function traiter() {
  var verrou = LockService.getScriptLock();
  if (!verrou.tryLock(20000)) return;
  try {
    var libelle = libelleFait_();
    var fils = GmailApp.search(REQUETE, 0, 50);
    fils.forEach(function (fil) {
      if (aLeLibelle_(fil, libelle)) return;
      var messages = fil.getMessages();
      var dernier = messages[messages.length - 1];
      var demande = lireDemande_(dernier.getPlainBody());
      if (demande.email) envoyerAccuse_(demande);
      // Libellé posé même sans adresse exploitable : on ne retente pas en boucle.
      fil.addLabel(libelle);
    });
  } finally {
    verrou.releaseLock();
  }
}

/** À lancer UNE fois : libellé, rattrapage silencieux, déclencheur. */
function installer() {
  var libelle = libelleFait_();
  GmailApp.search(REQUETE, 0, 100).forEach(function (fil) { fil.addLabel(libelle); });

  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'traiter') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('traiter').timeBased().everyMinutes(1).create();
  Logger.log('Installé : déclencheur chaque minute, messages existants marqués.');
}

/**
 * Test : renvoie l'accusé du DERNIER message du formulaire à l'adresse que ce
 * message contient (sans tenir compte du libellé ni du délai de 6 h).
 */
function testerDernierMessage() {
  var fils = GmailApp.search('from:' + EXPEDITEUR_SHOPIFY + ' "formulaire de contact"', 0, 1);
  if (!fils.length) { Logger.log('Aucun message du formulaire trouvé.'); return; }
  var messages = fils[0].getMessages();
  var corps = messages[messages.length - 1].getPlainBody();
  var demande = lireDemande_(corps);
  Logger.log(JSON.stringify(demande));
  if (!demande.email) { Logger.log('Pas d’adresse lisible. Corps :\n' + corps); return; }
  envoyerAccuse_(demande, true);
  Logger.log('Accusé de test envoyé à ' + demande.email);
}

// ---------------------------------------------------------------------------

function lireDemande_(corps) {
  var email = lireChamp_(corps, 'E-mail');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) email = '';
  return {
    email: email,
    nom: lireChamp_(corps, 'Nom'),
    motif: lireChamp_(corps, 'Motif'),
    commande: lireChamp_(corps, 'Commande') || lireChamp_(corps, 'Numéro De Commande')
  };
}

/** Valeur d'un champ, qu'elle soit sur la même ligne que l'étiquette ou la suivante. */
function lireChamp_(corps, etiquette) {
  var lignes = String(corps || '').split(/\r?\n/).map(function (l) { return l.trim(); });
  var debut = etiquette.toLowerCase() + ':';
  for (var i = 0; i < lignes.length; i++) {
    if (lignes[i].toLowerCase().indexOf(debut) !== 0) continue;
    var reste = lignes[i].slice(debut.length).trim();
    if (reste) return reste;
    for (var j = i + 1; j < lignes.length; j++) {
      if (!lignes[j]) continue;
      return estEtiquette_(lignes[j]) ? '' : lignes[j];
    }
    return '';
  }
  return '';
}

function estEtiquette_(ligne) {
  var bas = ligne.toLowerCase();
  return ETIQUETTES.some(function (e) { return bas.indexOf(e.toLowerCase() + ':') === 0; });
}

function envoyerAccuse_(demande, test) {
  var email = demande.email.toLowerCase();
  if (/@gusetfrost\.fr$/.test(email)) return;

  var cache = CacheService.getScriptCache();
  var cle = 'accuse:' + email;
  if (!test && cache.get(cle)) return;

  var motif = MOTIFS[demande.motif] || '';
  var commande = demande.commande ? ' (commande ' + demande.commande + ')' : '';

  var bonjour = demande.nom ? 'Bonjour ' + demande.nom + ',' : 'Bonjour,';
  var rappel = motif ? 'Pour rappel, votre demande concerne ' + motif + commande + '.' : '';

  var texte = [
    bonjour,
    '',
    'Merci pour votre message' + NBSP + ': il nous est bien parvenu. Nous vous répondons sous 48' + NBSP + 'h ouvrées.',
    rappel ? '\n' + rappel : '',
    '',
    'Si ce message est arrivé dans vos courriers indésirables, marquez-le comme «' + NBSP + 'non indésirable' + NBSP + '»' + NBSP + ': notre réponse arrivera ainsi dans votre boîte de réception.',
    '',
    'À très vite,',
    'L’équipe Gus et Frost'
  ].join('\n').replace(/\n{3,}/g, '\n\n');

  var p = 'margin:0 0 16px;';
  var html =
    '<div style="font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#314431;max-width:560px;">' +
      '<p style="' + p + '">' + echapper_(bonjour) + '</p>' +
      '<p style="' + p + '">Merci pour votre message&nbsp;: il nous est bien parvenu. Nous vous répondons sous 48&nbsp;h ouvrées.</p>' +
      (rappel ? '<p style="' + p + '">' + echapper_(rappel) + '</p>' : '') +
      '<p style="' + p + '">Si ce message est arrivé dans vos courriers indésirables, marquez-le comme «&nbsp;non indésirable&nbsp;»&nbsp;: notre réponse arrivera ainsi dans votre boîte de réception.</p>' +
      '<p style="margin:0;">À très vite,<br>L’équipe Gus et Frost</p>' +
    '</div>';

  GmailApp.sendEmail(demande.email, 'Nous avons bien reçu votre message', texte, {
    htmlBody: html,
    name: NOM_EXPEDITEUR,
    replyTo: ADRESSE_REPONSE
  });
  cache.put(cle, '1', 21600); // 6 h, le maximum de CacheService
}

function echapper_(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/\u00a0/g, '&nbsp;');
}

function libelleFait_() {
  return GmailApp.getUserLabelByName(LIBELLE_FAIT) || GmailApp.createLabel(LIBELLE_FAIT);
}

function aLeLibelle_(fil, libelle) {
  var nom = libelle.getName();
  return fil.getLabels().some(function (l) { return l.getName() === nom; });
}
