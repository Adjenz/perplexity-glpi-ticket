# 🎫 Script d'Automatisation GLPI avec Reformulation IA

Un script Python professionnel pour automatiser la création et gestion de tickets GLPI 10.0.5 avec reformulation intelligente des textes via l'API Perplexity créé à l'aide de [Perplexity Labs](https://perplexity.ai).

## ✨ Fonctionnalités

### 🎯 **Collecte Interactive d'Informations**
- Interface CLI conviviale avec validation automatique
- Collecte complète : titre, appelant, téléphone, email, description, demandeur, type
- Support du numéro de série copieur (optionnel)
- Validation des formats (email français, téléphone français)
- Saisie multiligne avec double Entrée pour valider

### 🤖 **Reformulation IA via Perplexity**
- Reformulation professionnelle des descriptions et solutions
- Instructions personnalisables et testables
- Modèle `sonar` avec température optimisée (0.05)
- Gestion d'erreurs robuste avec fallback vers le texte original
- Préservation stricte du contexte et de l'intention originale

### 🎫 **Intégration GLPI Complète**
- Authentification sécurisée par tokens (app-token + user-token)
- Recherche intelligente d'utilisateurs et d'entités
- Création automatique de tickets avec tous les champs requis
- Support des sous-entités (CLIENTS_HORS_CONTRAT, CLIENTS_SOUS_CONTRAT, COPIEUR)
- Attribution de techniciens (ID 233 par défaut, personnalisable)
- Workflow complet : création → résolution → clôture
- Gestion complète des catégories ITIL

### ⚙️ **Configuration et Personnalisation**
- Configuration interactive des APIs (`--config`)
- Instructions de reformulation personnalisables (`--instructions`)
- Tests en temps réel des instructions
- Sauvegarde automatique des configurations
- Support multi-utilisateurs avec configurations séparées

## 📋 Prérequis

- **Python 3.7+**
- **GLPI 10.0.5** avec API REST activée
- **Compte Perplexity AI** avec clé API
- **Accès réseau** aux serveurs GLPI et Perplexity

## 🚀 Installation

### 1. Cloner le Repository
```bash
git clone https://github.com/Adjenz/perplexity-glpi-ticket
cd perplexity-glpi-ticket
```

### 2. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration Initiale
```bash
# Configuration interactive des APIs
python glpi_ticket_automation_v1.8.py --config
```

## ⚙️ Configuration

### Configuration GLPI

1. **Activer l'API REST dans GLPI :**
   - Aller dans `Configuration > Général > API`
   - Activer l'API REST
   - Noter l'URL : `https://votre-serveur-glpi.com/apirest.php`

2. **Créer un client API :**
   - `Configuration > Général > API > Clients API`
   - Créer un client avec votre plage IP
   - Noter le `App-Token` généré

3. **Obtenir le token utilisateur :**
   - Profil utilisateur > `Paramètres personnels`
   - Activer "Accès distant" et générer une clé
   - Noter le `User-Token`

### Configuration Perplexity

1. **Obtenir une clé API :**
   - Aller sur [Perplexity AI](https://www.perplexity.ai/)
   - Créer un compte et générer une clé API

2. **Lancer la configuration :**
```bash
python glpi_ticket_automation_v1.8.py --config
```

**Exemple d'interaction :**
```
⚙️  CONFIGURATION DU SCRIPT GLPI
======================================
🔧 CONFIGURATION GLPI
------------------------------
URL de l'API GLPI: https://glpi.monentreprise.com/apirest.php
App-Token GLPI: f7g3csp8mgatg5ebc5elnazakw20i9fyev1qopya7
User-Token GLPI: q56hqkniwot8wntb3z1qarka5atf365taaa2uyjrn

🤖 CONFIGURATION PERPLEXITY AI
------------------------------
Clé API Perplexity: pplx-1234567890abcdef1234567890abcdef

✅ Configuration sauvegardée dans .env
🧪 Test de la configuration...
   ✅ Connexion GLPI réussie
   ✅ Connexion Perplexity réussie
```

## 🎯 Utilisation

### Mode Normal - Création de Tickets
```bash
python glpi_ticket_automation_v1.8.py
```

### Configuration des Instructions IA
```bash
python glpi_ticket_automation_v1.8.py --instructions
```

### Aide Complète
```bash
python glpi_ticket_automation_v1.8.py --help
```

## 📝 Workflow Complet

### 1. Collecte des Informations
```
🎯 Titre du ticket: Problème imprimante bureau 205
👤 Nom de l'appelant: Sarah Martin
📱 Numéro de téléphone: 01 39 11 19 07
🖨️ Numéro de série du copieur: ABC123XYZ789
📧 Adresse email: sarah.martin@entreprise.com
📝 Description du problème/incident:
   L'imprimante ne répond plus depuis ce matin.
   Le voyant rouge clignote en permanence.
   
🏢 Nom du demandeur (utilisateur GLPI): TECHNIPLUS
🎫 Type de ticket: 1. Incident
```

### 2. Recherche et Validation
```
✅ Utilisateur trouvé: techniplus (ID: 157)
✅ Nom du client qui sera utilisé: TECHNIPLUS
✅ Entité trouvée dans COPIEUR: TECHNIPLUS (ID: 23)
📍 Chemin complet: VOTRE_ENTREPRISE > COPIEUR > TECHNIPLUS
```

### 3. Reformulation IA
```
📄 APERÇU DES DESCRIPTIONS:
------------------------------
📝 Description originale:
   L'imprimante ne répond plus depuis ce matin.
   Le voyant rouge clignote en permanence.

🤖 Description reformulée:
   Imprimante inaccessible depuis ce matin avec voyant rouge clignotant.

❓ Accepter la reformulation? (o/N): o
✅ Reformulation acceptée
```

### 4. Création et Gestion
```
📋 APERÇU DU TICKET FINAL:
👥 Nom du client : TECHNIPLUS
👤 Nom de l'appelant : Sarah Martin
📱 Numéro de téléphone : 01 39 11 19 07
🖨️ Numéro de série du copieur : ABC123XYZ789
📧 E-mail : sarah.martin@entreprise.com
📝 Description de l'incident :
Imprimante inaccessible depuis ce matin avec voyant rouge clignotant.

🎉 TICKET CRÉÉ AVEC SUCCÈS!
🆔 ID du ticket: 1245
```

## 🔧 Personnalisation des Instructions

Le script permet de personnaliser les instructions de reformulation pour adapter l'IA à vos besoins :

```bash
python glpi_ticket_automation_v1.8.py --instructions
```

### Menu de Configuration
```
📝 CONFIGURATION DES INSTRUCTIONS DE REFORMULATION
===================================================
🎯 Que souhaitez-vous faire ?
1. Modifier les instructions de reformulation de DESCRIPTION
2. Modifier les instructions de reformulation de SOLUTION  
3. Tester les instructions actuelles
4. Restaurer les instructions par défaut
5. Afficher les instructions actuelles
6. Retour au menu principal
```

### Test des Instructions
```
🧪 TEST DES INSTRUCTIONS DE REFORMULATION
--------------------------------------------------
📝 Test - Reformulation de DESCRIPTION:
Entrez un texte de description à tester: Le serveur est en panne depuis hier soir

📄 Résultat: Serveur inaccessible depuis hier soir

💡 Test - Reformulation de SOLUTION:
Entrez un texte de solution à tester: Redémarrage du serveur effectué

📄 Résultat: Redémarrage du serveur effectué avec succès
```

## 📁 Structure des Fichiers

```
glpi-ticket-automation/
├── glpi_ticket_automation_v1.8.py    # Script principal
├── requirements.txt                   # Dépendances Python
├── .env                              # Configuration APIs (généré automatiquement)
├── .env.example                      # Template de configuration
├── instructions_reformulation.json   # Instructions IA personnalisées
├── glpi_automation.log              # Logs d'exécution
├── test_connections.py              # Script de test des connexions
└── README.md                        # Cette documentation
```

## 🎨 Format de Ticket Généré

### Exemple de Ticket Créé
**Titre :** `Problème imprimante bureau 205`

**Contenu :**
```
👥 Nom du client : TECHNIPLUS
👤 Nom de l'appelant : Sarah Martin
📱 Numéro de téléphone : 01 39 11 19 07
🖨️ Numéro de série du copieur : ABC123XYZ789
📧 E-mail : sarah.martin@entreprise.com
📝 Description de l'incident :
Imprimante inaccessible depuis ce matin avec voyant rouge clignotant.
```

**Métadonnées GLPI :**
- **Demandeur :** TECHNIPLUS (ID: 157)
- **Entité :** VOTRE_ENTREPRISE > COPIEUR > TECHNIPLUS
- **Technicien assigné :** ID 233 (personnalisable)
- **Type :** Incident
- **Statut :** Nouveau (1)
- **Catégorie :** Sélectionnable parmi toutes les catégories ITIL

## 🛠️ Dépannage

### Erreurs Communes

#### Configuration Manquante
```
❌ Configuration manquante ! Utilisez: python glpi_ticket_automation.py --config
```
**Solution :** Exécuter `--config` pour configurer les APIs

#### Erreur d'Authentification GLPI
```
❌ Erreur d'authentification GLPI: 401 Unauthorized
```
**Solutions :**
- Vérifier l'URL de l'API GLPI
- Vérifier les tokens app-token et user-token
- Vérifier les droits de l'utilisateur dans GLPI
- Vérifier que l'API REST est activée

#### Erreur de Connexion Perplexity
```
❌ Erreur lors de la reformulation description: 401 Unauthorized
```
**Solutions :**
- Vérifier la clé API Perplexity
- Vérifier les quotas de l'API
- Vérifier la connexion internet

#### Utilisateur Non Trouvé
```
⚠️ Utilisateur 'test_user' non trouvé
```
**Solutions :**
- Vérifier que l'utilisateur existe dans GLPI
- Vérifier que l'utilisateur a le droit "Demandeur"
- Utiliser un terme de recherche plus précis

### Tests de Diagnostic

#### Test des Connexions APIs
```bash
python test_connections.py
```

#### Test des Instructions
```bash
python glpi_ticket_automation_v1.8.py --instructions
# Choisir option 3 : Tester les instructions actuelles
```

### Logs et Débogage

Les logs détaillés sont sauvegardés dans `glpi_automation.log` :
```
2025-09-08 10:30:15,123 - INFO - 🔐 Initialisation de la session GLPI...
2025-09-08 10:30:15,456 - INFO - ✅ Authentification GLPI réussie
2025-09-08 10:30:16,789 - INFO - 📋 14 entités chargées
2025-09-08 10:30:17,012 - INFO - 📂 10 catégories chargées
2025-09-08 10:30:20,345 - INFO - 🤖 Reformulation de la description via Perplexity...
2025-09-08 10:30:22,678 - INFO - ✅ Description reformulée avec succès
2025-09-08 10:30:25,901 - INFO - 🎫 Création du ticket dans GLPI...
2025-09-08 10:30:26,234 - INFO - ✅ Ticket créé avec l'ID: 1245
```

## 📊 Statuts de Tickets GLPI

Le script gère les statuts GLPI standard :
- **1** : Nouveau (défaut à la création)
- **2** : En cours (traitement)
- **4** : En attente
- **5** : Résolu (avec solution)
- **6** : Fermé (clôturé)

## 🔒 Sécurité

### Bonnes Pratiques
- ✅ Tokens stockés dans variables d'environnement
- ✅ Aucun token en dur dans le code
- ✅ Sessions GLPI fermées automatiquement
- ✅ Validation des entrées utilisateur
- ✅ Timeouts configurés pour toutes les requêtes API
- ✅ Logs détaillés pour audit

### Configuration Sécurisée
```bash
# Permissions restrictives sur le fichier .env
chmod 600 .env

# Ne pas committer le fichier .env
echo ".env" >> .gitignore
```

## 🚫 Limites Connues

- Support uniquement pour **GLPI 10.0.5**
- Format de téléphone **français uniquement**
- Validation email basique (RFC non complète)
- Une seule entité par ticket
- Pas de gestion des pièces jointes
- Reformulation en **français uniquement**
- Dépendance à la disponibilité des APIs externes

## 🔄 Workflow Multi-Utilisateurs

### Pour une Équipe
1. **Chaque utilisateur** exécute `--config` avec ses propres tokens
2. **Instructions partagées** : copier `instructions_reformulation.json`
3. **Configuration centralisée** : partager `.env.example` avec les URLs

### Exemple de Déploiement
```bash
# Utilisateur 1
python glpi_ticket_automation_v1.8.py --config
# → Crée .env avec ses tokens

# Utilisateur 2 (copie les instructions de l'utilisateur 1)
cp instructions_reformulation.json instructions_reformulation.json.backup
python glpi_ticket_automation_v1.8.py --config
# → Crée son .env
cp instructions_reformulation.json.backup instructions_reformulation.json
# → Récupère les instructions partagées
```

## 📚 Références API

### GLPI API 10.0.5
- [Documentation officielle](https://glpi-user-documentation.readthedocs.io/fr/latest/modules/configuration/general/api.html)
- **Endpoints utilisés :**
  - `POST /apirest.php/initSession` - Authentification
  - `GET /apirest.php/User` - Recherche utilisateurs
  - `GET /apirest.php/Entity` - Liste des entités  
  - `GET /apirest.php/ITILCategory` - Liste des catégories
  - `POST /apirest.php/Ticket` - Création de ticket
  - `POST /apirest.php/ITILSolution` - Ajout de solution
  - `PUT /apirest.php/Ticket/{id}` - Mise à jour
  - `GET /apirest.php/killSession` - Fermeture session

### Perplexity API
- [Documentation Perplexity](https://docs.perplexity.ai/)
- **Modèle utilisé :** `sonar`
- **Endpoint :** `https://api.perplexity.ai/chat/completions`
- **Température :** 0.05 (précision maximale)

## 🤝 Contribution

### Signaler un Bug
1. Vérifier les [issues existantes](https://github.com/votre-username/glpi-ticket-automation/issues)
2. Créer une nouvelle issue avec :
   - Description du problème
   - Version Python et OS
   - Logs d'erreur (`glpi_automation.log`)
   - Étapes pour reproduire

### Proposer une Amélioration
1. Fork le repository
2. Créer une branche feature : `git checkout -b feature/amelioration`
3. Commiter les changements : `git commit -m 'Ajout nouvelle fonctionnalité'`
4. Push vers la branche : `git push origin feature/amelioration`
5. Ouvrir une Pull Request

### Développement Local
```bash
# Cloner votre fork
git clone https://github.com/votre-username/glpi-ticket-automation.git

# Installer en mode développement
pip install -e .

# Lancer les tests
python test_connections.py
python glpi_ticket_automation_v1.8.py --instructions
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **GLPI Team** pour l'excellent système ITIL
- **Perplexity AI** pour l'API de reformulation intelligente
- **Communauté Python** pour les librairies utilisées
- **Contributeurs** du projet

## 📞 Support

- **Issues :** [GitHub Issues](https://github.com/votre-username/glpi-ticket-automation/issues)
- **Discussions :** [GitHub Discussions](https://github.com/votre-username/glpi-ticket-automation/discussions)
- **Wiki :** [Documentation avancée](https://github.com/votre-username/glpi-ticket-automation/wiki)

---

**Version :** 1.8  
**Auteur :** Votre Nom  
**Dernière mise à jour :** Septembre 2025

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**
