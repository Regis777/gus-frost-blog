# -*- coding: utf-8 -*-
"""Genere theme/gf-question-blog.liquid.

Les espaces insecables (U+00A0) sont ecrits en   pour rester visibles
dans le source : regle absolue G&F (avant : ; ! ? » et apres «).
"""
import io
import os
import sys

NB = u" "   # espace insecable
AP = u"’"   # apostrophe typographique

T = u"""{%- comment -%}
  Section <<Votre question>> - bas de la page de resultats de recherche.

  But : recuperer de la matiere editoriale. Quand un visiteur cherche quelque
  chose qu@il ne trouve pas (ou dont les resultats ne lui conviennent pas), on
  lui demande sa question. Le terme exact qu@il a tape part avec le message :
  c@est lui qui sert a choisir les prochains articles.

  Deux canaux, volontairement redondants :
    1. Formulaire CONTACT natif Shopify -> e-mail vers l@adresse de la boutique.
       Aucune cle d@API dans la page, anti-spam natif, marche sans JavaScript.
    2. Klaviyo (endpoints CLIENT, cle PUBLIQUE) -> evenement <<Question blog>>
       avec la question et le terme cherche en proprietes. L@inscription a la
       liste marketing n@a lieu QUE si la case facultative est cochee (RGPD).

  Le JavaScript ne bloque jamais l@envoi : au bout de 2 s le formulaire part de
  toute facon. Cle Klaviyo vide = seul l@e-mail fonctionne, sans erreur.

  Rappel Dawn : 1rem = 10 px (racine a 62,5 %).
{%- endcomment -%}
{%- if search.performed -%}
  {%- liquid
    assign terme = search.terms | escape
    assign vide = false
    if search.results_count == 0
      assign vide = true
    endif
  -%}
  <div class="gf-question page-width" id="gf-question">
    <div class="gf-question__box">
      <h2 class="gf-question__titre">
        {%- if vide -%}
          {{ section.settings.titre_vide | replace: '[terme]', terme }}
        {%- else -%}
          {{ section.settings.titre }}
        {%- endif -%}
      </h2>
      <p class="gf-question__intro">{{ section.settings.intro }}</p>

      {%- form 'contact', id: 'GfQuestionBlog', class: 'gf-question__form' -%}
        {%- if form.posted_successfully? -%}
          <p class="gf-question__ok" role="status" tabindex="-1" autofocus>{{ section.settings.merci }}</p>
        {%- else -%}
          {%- if form.errors -%}
            <p class="gf-question__erreur" role="alert">{{ form.errors | default_errors }}</p>
          {%- endif -%}

          {%- comment -%} Contexte de la recherche : repris tel quel dans l@e-mail recu. {%- endcomment -%}
          <input type="hidden" name="contact[Recherche]" value="{{ terme }}">
          <input type="hidden" name="contact[Resultats trouves]" value="{{ search.results_count }}">
          <input type="hidden" name="contact[Origine]" value="Page de resultats de recherche">

          <div class="gf-question__champ">
            <label for="GfQuestionBody">{{ section.settings.label_question }} <span aria-hidden="true">*</span></label>
            <textarea id="GfQuestionBody" name="contact[body]" rows="4" required placeholder="{{ section.settings.exemple | escape }}">{{ form.body }}</textarea>
          </div>

          <div class="gf-question__champ">
            <label for="GfQuestionEmail">{{ section.settings.label_email }} <span aria-hidden="true">*</span></label>
            <input type="email" id="GfQuestionEmail" name="contact[email]" value="{{ form.email }}" autocomplete="email" autocorrect="off" autocapitalize="off" required placeholder="vous@@exemple.fr">
          </div>

          <div class="gf-question__optin">
            <input type="checkbox" id="GfQuestionOptin" name="contact[Inscription newsletter]" value="oui">
            <label for="GfQuestionOptin">{{ section.settings.optin }}</label>
          </div>

          <p class="gf-question__rgpd">
            {{ section.settings.rgpd }}
            {%- if shop.privacy_policy -%}
              <a href="{{ shop.privacy_policy.url }}">{{ shop.privacy_policy.title }}</a>.
            {%- endif -%}
          </p>

          <button type="submit" class="gf-question__bouton">{{ section.settings.bouton }}</button>
        {%- endif -%}
      {%- endform -%}
    </div>

    {%- comment -%} ---------- Configuration passee au JS (Klaviyo) ---------- {%- endcomment -%}
    <script type="application/json" data-gfq-question-config>
      {
        "cle": {{ section.settings.klaviyo_cle | default: '' | json }},
        "liste": {{ section.settings.klaviyo_liste | default: '' | json }},
        "metric": {{ section.settings.klaviyo_metric | default: 'Question blog' | json }},
        "source": {{ section.settings.source | default: 'recherche_blog' | json }},
        "terme": {{ search.terms | json }},
        "resultats": {{ search.results_count | default: 0 }}
      }
    </script>
  </div>

  <style>
    .gf-question{margin:4rem auto 5rem;}
    .gf-question__box{max-width:64rem;margin:0 auto;padding:2.8rem 3rem;border:1px solid rgba(var(--color-foreground),.14);border-radius:1.2rem;background:rgba(var(--color-foreground),.03);}
    .gf-question__titre{margin:0 0 .8rem;font-size:2.2rem;line-height:1.25;}
    .gf-question__intro{margin:0 0 2rem;font-size:1.6rem;line-height:1.45;color:rgba(var(--color-foreground),.85);}
    .gf-question__champ{margin:0 0 1.4rem;}
    .gf-question__champ label{display:block;margin:0 0 .5rem;font-size:1.5rem;font-weight:600;}
    .gf-question__champ textarea,
    .gf-question__champ input[type=email]{width:100%;box-sizing:border-box;padding:1.1rem 1.4rem;font-family:inherit;font-size:1.6rem;line-height:1.4;border:1px solid rgba(var(--color-foreground),.25);border-radius:.8rem;background:rgb(var(--color-background));color:rgb(var(--color-foreground));}
    .gf-question__champ textarea{resize:vertical;min-height:9rem;}
    .gf-question__champ textarea::placeholder,
    .gf-question__champ input[type=email]::placeholder{color:rgba(var(--color-foreground),.5);}
    .gf-question__champ textarea:focus,
    .gf-question__champ input[type=email]:focus{outline:2px solid rgba(var(--color-foreground),.5);outline-offset:1px;}
    .gf-question__optin{display:flex;align-items:flex-start;gap:.8rem;margin:0 0 1.2rem;}
    .gf-question__optin input{margin-top:.35rem;flex:0 0 auto;width:1.6rem;height:1.6rem;}
    .gf-question__optin label{font-size:1.4rem;line-height:1.4;color:rgba(var(--color-foreground),.85);}
    .gf-question__rgpd{margin:0 0 1.8rem;font-size:1.3rem;line-height:1.4;color:rgba(var(--color-foreground),.65);}
    .gf-question__rgpd a{color:inherit;}
    .gf-question__bouton{padding:1.2rem 2.6rem;font-family:inherit;font-size:1.5rem;font-weight:600;letter-spacing:.03em;border:0;border-radius:999px;cursor:pointer;background:rgb(var(--color-foreground));color:rgb(var(--color-background));}
    .gf-question__bouton:hover{opacity:.9;}
    .gf-question__ok{margin:0;padding:1.4rem 1.6rem;font-size:1.6rem;line-height:1.45;border-radius:.8rem;background:rgba(var(--color-foreground),.07);}
    .gf-question__erreur{margin:0 0 1.4rem;font-size:1.5rem;line-height:1.4;color:#b3261e;}
    @media screen and (max-width: 749px){
      .gf-question{margin:3rem auto 4rem;}
      .gf-question__box{padding:2rem 1.8rem;border-radius:1rem;}
      .gf-question__titre{font-size:1.9rem;}
      .gf-question__bouton{width:100%;}
    }
  </style>

  <script>
    /* Klaviyo en second canal.

       ON NE TOUCHE PAS A L'ENVOI DU FORMULAIRE. Shopify protege les
       formulaires de contact par un CAPTCHA dont le jeton est injecte
       PENDANT l'evenement submit. Intercepter cet evenement puis appeler
       form.submit() -- qui, lui, ne redeclenche aucun evenement -- fait
       sauter cette injection : Shopify repond 400 <<Missing CAPTCHA token>>
       et l'e-mail ne part jamais. Mesure faite en direct le 06/09/2026.

       Donc : pas de preventDefault. Les appels Klaviyo partent en
       `keepalive`, ce qui les fait survivre au changement de page. */
    (function () {
      var box = document.getElementById('gf-question');
      if (!box) return;
      var form = box.querySelector('form');
      var brut = box.querySelector('[data-gfq-question-config]');
      if (!form || !brut) return;

      var cfg = {};
      try { cfg = JSON.parse(brut.textContent); } catch (e) { return; }
      if (!cfg.cle) return;                    /* cle vide : e-mail seul */

      var REVISION = '2024-10-15';

      function post(chemin, corps) {
        try {
          fetch('https://a.klaviyo.com/client/' + chemin + '/?company_id=' + encodeURIComponent(cfg.cle), {
            method: 'POST',
            headers: { 'content-type': 'application/json', revision: REVISION },
            body: JSON.stringify(corps),
            keepalive: true
          }).catch(function (err) { console.warn('[question blog] Klaviyo indisponible', err); });
        } catch (e) {
          console.warn('[question blog] Klaviyo indisponible', e);
        }
      }

      /* Evenement : question + terme cherche deviennent des proprietes
         consultables dans Klaviyo (Analytics > Metrics > Question blog). */
      function evenement(email, question) {
        post('events', {
          data: {
            type: 'event',
            attributes: {
              metric: { data: { type: 'metric', attributes: { name: cfg.metric } } },
              profile: { data: { type: 'profile', attributes: { email: email } } },
              properties: {
                question: question,
                recherche: cfg.terme,
                resultats: cfg.resultats,
                source_lead: cfg.source,
                date: new Date().toISOString().slice(0, 10)
              }
            }
          }
        });
      }

      /* Inscription marketing : UNIQUEMENT si la case facultative est cochee. */
      function inscrit(email) {
        if (!cfg.liste) return;
        post('subscriptions', {
          data: {
            type: 'subscription',
            attributes: {
              profile: {
                data: {
                  type: 'profile',
                  attributes: { email: email, properties: { source_lead: cfg.source } }
                }
              }
            },
            relationships: { list: { data: { type: 'list', id: cfg.liste } } }
          }
        });
      }

      /* Aucun preventDefault ici : l'envoi Shopify (et son jeton CAPTCHA)
         suit son cours normal, les appels Klaviyo partent en parallele. */
      form.addEventListener('submit', function () {
        var champEmail = form.querySelector('[name="contact[email]"]');
        var champTexte = form.querySelector('[name="contact[body]"]');
        if (!champEmail || !champTexte || !champEmail.value || !champTexte.value) return;

        evenement(champEmail.value, champTexte.value);

        var optin = form.querySelector('[name="contact[Inscription newsletter]"]');
        if (optin && optin.checked) inscrit(champEmail.value);
      });
    })();
  </script>
{%- endif -%}

{% schema %}
{
  "name": "Question du visiteur",
  "settings": [
    {
      "type": "paragraph",
      "content": "S@affiche sous les resultats de recherche. Les reponses arrivent par e-mail (formulaire de contact Shopify) avec le terme cherche, et dans Klaviyo si la cle est renseignee."
    },
    {
      "type": "text",
      "id": "titre",
      "label": "Titre (quand il y a des resultats)",
      "default": "Vous n@avez pas trouve votre reponse~?"
    },
    {
      "type": "text",
      "id": "titre_vide",
      "label": "Titre (quand il n@y a aucun resultat)",
      "info": "[terme] est remplace par ce que le visiteur a tape.",
      "default": "Aucun resultat pour <<~[terme]~>>~: posez-nous votre question."
    },
    {
      "type": "textarea",
      "id": "intro",
      "label": "Texte d@introduction",
      "default": "Dites-nous ce que vous cherchiez~: nous lisons chaque question et nous vous repondons par e-mail. Les sujets qui reviennent le plus souvent deviennent nos prochains articles."
    },
    {
      "type": "text",
      "id": "label_question",
      "label": "Libelle du champ question",
      "default": "Votre question"
    },
    {
      "type": "textarea",
      "id": "exemple",
      "label": "Exemple affiche dans le champ",
      "default": "Ex.~: mon chiot de 4~mois hurle des que je pars travailler, par ou commencer~?"
    },
    {
      "type": "text",
      "id": "label_email",
      "label": "Libelle du champ e-mail",
      "default": "Votre e-mail"
    },
    {
      "type": "textarea",
      "id": "optin",
      "label": "Case facultative (inscription marketing)",
      "default": "Je souhaite aussi recevoir les conseils de Gus~&~Frost par e-mail. Sans cette case, votre adresse ne sert qu@a vous repondre."
    },
    {
      "type": "textarea",
      "id": "rgpd",
      "label": "Mention de confidentialite",
      "default": "Votre adresse nous sert a vous repondre~; elle n@est ni revendue ni cedee. Vous pouvez demander sa suppression a tout moment~:"
    },
    {
      "type": "text",
      "id": "bouton",
      "label": "Libelle du bouton",
      "default": "Envoyer ma question"
    },
    {
      "type": "textarea",
      "id": "merci",
      "label": "Message de confirmation",
      "default": "Merci~! Votre question est bien arrivee. Nous vous repondons par e-mail, et si le sujet manque au blog, il rejoint notre liste d@articles a ecrire."
    },
    {
      "type": "header",
      "content": "Branchement Klaviyo (facultatif)"
    },
    {
      "type": "paragraph",
      "content": "Cle vide = seul l@e-mail fonctionne. Cle PUBLIQUE (Site ID) dans Klaviyo > Settings > API keys. L@id de liste ne sert QUE si le visiteur coche la case facultative."
    },
    { "type": "text", "id": "klaviyo_cle", "label": "Cle publique Klaviyo (Site ID)" },
    { "type": "text", "id": "klaviyo_liste", "label": "ID de la liste Klaviyo" },
    { "type": "text", "id": "klaviyo_metric", "label": "Nom de l@evenement", "default": "Question blog" },
    { "type": "text", "id": "source", "label": "Source du lead", "default": "recherche_blog" }
  ],
  "presets": [{ "name": "Question du visiteur" }]
}
{% endschema %}
"""

# ---- Substitutions : caracteres typographiques francais ----------------------
# @  -> apostrophe typographique          ~  -> espace insecable
# <<  >> -> guillemets francais
# @@ -> arobase litterale (adresse e-mail d'exemple)
T = T.replace(u"@@", u"\x00")        # arobase litterale (adresse d'exemple)
T = T.replace(u"@media", u"\x01")    # at-rule CSS : ne pas toucher
T = T.replace(u"@", AP)
T = T.replace(u"\x00", u"@").replace(u"\x01", u"@media")
T = T.replace(u"~", NB)
T = T.replace(u"<<", u"«").replace(u">>", u"»")

# Accents des textes visibles (le code et les commentaires restent en ASCII).
ACCENTS = [
    (u"S’affiche sous les resultats", u"S’affiche sous les résultats"),
    (u"cherche, et dans Klaviyo si la cle est renseignee.",
     u"cherché, et dans Klaviyo si la clé est renseignée."),
    (u"le terme cherche, et", u"le terme cherché, et"),
    (u"Titre (quand il y a des resultats)", u"Titre (quand il y a des résultats)"),
    (u"Vous n’avez pas trouve votre reponse", u"Vous n’avez pas trouvé votre réponse"),
    (u"Titre (quand il n’y a aucun resultat)", u"Titre (quand il n’y a aucun résultat)"),
    (u"est remplace par ce que le visiteur a tape.",
     u"est remplacé par ce que le visiteur a tapé."),
    (u"Aucun resultat pour", u"Aucun résultat pour"),
    (u"nous vous repondons par e-mail", u"nous vous répondons par e-mail"),
    (u"Texte d’introduction", u"Texte d’introduction"),
    (u"Libelle du champ question", u"Libellé du champ question"),
    (u"Exemple affiche dans le champ", u"Exemple affiché dans le champ"),
    (u"hurle des que je pars travailler, par ou commencer",
     u"hurle dès que je pars travailler, par où commencer"),
    (u"Libelle du champ e-mail", u"Libellé du champ e-mail"),
    (u"ne sert qu’a vous repondre.", u"ne sert qu’à vous répondre."),
    (u"Mention de confidentialite", u"Mention de confidentialité"),
    (u"Votre adresse nous sert a vous repondre", u"Votre adresse nous sert à vous répondre"),
    (u"elle n’est ni revendue ni cedee. Vous pouvez demander sa suppression a tout moment",
     u"elle n’est ni revendue ni cédée. Vous pouvez demander sa suppression à tout moment"),
    (u"Libelle du bouton", u"Libellé du bouton"),
    (u"Votre question est bien arrivee.", u"Votre question est bien arrivée."),
    (u"il rejoint notre liste d’articles a ecrire.",
     u"il rejoint notre liste d’articles à écrire."),
    (u"Cle vide = seul l’e-mail fonctionne.", u"Clé vide = seul l’e-mail fonctionne."),
    (u"Cle PUBLIQUE (Site ID)", u"Clé PUBLIQUE (Site ID)"),
    (u"Cle publique Klaviyo (Site ID)", u"Clé publique Klaviyo (Site ID)"),
    (u"Nom de l’evenement", u"Nom de l’événement"),
    (u"Section «Votre question» - bas", u"Section « Votre question » — bas"),
    (u"Les reponses arrivent", u"Les réponses arrivent"),
    # Libelles repris tels quels dans l'e-mail recu par Regis.
    (u"contact[Resultats trouves]", u"contact[Résultats trouvés]"),
    (u"Page de resultats de recherche", u"Page de résultats de recherche"),
    (u"recherche : repris tel quel dans", u"recherche : repris tel quel dans"),
    (u"Nous vous repondons par e-mail", u"Nous vous répondons par e-mail"),
]
for a, b in ACCENTS:
    T = T.replace(a, b)

dest = sys.argv[1]
io.open(dest, "w", encoding="utf-8", newline="\n").write(T)
print("ecrit : %s (%d octets, %d insecables)"
      % (os.path.basename(dest), len(T.encode("utf-8")), T.count(NB)))
