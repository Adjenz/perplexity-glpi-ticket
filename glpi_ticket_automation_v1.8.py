#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'automatisation pour la création et gestion de tickets GLPI 10.0.5
avec reformulation par l'API Perplexity.

Auteur: Assistant AI
Date: Septembre 2025
Version: 1.8 - Correction erreur import test instructions
"""

import requests
import json
import os
import sys
import re
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('glpi_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Gestionnaire de configuration interactive"""

    @staticmethod
    def configurer_environnement():
        """Configuration interactive du fichier .env"""
        print("\n" + "=" * 70)
        print("  ⚙️  CONFIGURATION DU SCRIPT GLPI")
        print("=" * 70)
        print("  📝 Configuration des variables d'environnement")
        print("=" * 70)

        config = {}

        # Configuration GLPI
        print("\n🔧 CONFIGURATION GLPI")
        print("-" * 30)

        while True:
            glpi_url = input("URL de l'API GLPI (ex: https://glpi.monentreprise.com/apirest.php): ").strip()
            if glpi_url:
                if not glpi_url.startswith('http'):
                    glpi_url = 'https://' + glpi_url
                if not glpi_url.endswith('/apirest.php'):
                    if glpi_url.endswith('/'):
                        glpi_url += 'apirest.php'
                    else:
                        glpi_url += '/apirest.php'
                config['GLPI_API_URL'] = glpi_url
                break
            print("❌ L'URL de l'API GLPI ne peut pas être vide")

        while True:
            app_token = input("App-Token GLPI: ").strip()
            if app_token:
                config['GLPI_APP_TOKEN'] = app_token
                break
            print("❌ L'App-Token ne peut pas être vide")

        while True:
            user_token = input("User-Token GLPI: ").strip()
            if user_token:
                config['GLPI_USER_TOKEN'] = user_token
                break
            print("❌ L'User-Token ne peut pas être vide")

        # Configuration Perplexity
        print("\n🤖 CONFIGURATION PERPLEXITY AI")
        print("-" * 30)

        while True:
            perplexity_key = input("Clé API Perplexity (ex: pplx-xxxxx): ").strip()
            if perplexity_key:
                if not perplexity_key.startswith('pplx-'):
                    print("⚠️  La clé devrait commencer par 'pplx-', continuez quand même? (o/N)")
                    if input().lower() not in ['o', 'oui', 'y', 'yes']:
                        continue
                config['PERPLEXITY_API_KEY'] = perplexity_key
                break
            print("❌ La clé API Perplexity ne peut pas être vide")

        # Sauvegarder dans .env
        env_content = f"""# Configuration des API - GLPI et Perplexity
# Généré automatiquement le {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Configuration GLPI
GLPI_API_URL={config['GLPI_API_URL']}
GLPI_APP_TOKEN={config['GLPI_APP_TOKEN']}
GLPI_USER_TOKEN={config['GLPI_USER_TOKEN']}

# Configuration Perplexity
PERPLEXITY_API_KEY={config['PERPLEXITY_API_KEY']}
"""

        try:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)

            print("\n✅ Configuration sauvegardée dans .env")
            print("\n🧪 Test de la configuration...")

            # Recharger les variables d'environnement
            load_dotenv(override=True)

            # Test rapide
            print("   🔍 Test de la connexion GLPI...")
            if ConfigManager.tester_glpi():
                print("   ✅ Connexion GLPI réussie")
            else:
                print("   ❌ Échec de la connexion GLPI")

            print("   🔍 Test de la connexion Perplexity...")
            if ConfigManager.tester_perplexity():
                print("   ✅ Connexion Perplexity réussie")
            else:
                print("   ❌ Échec de la connexion Perplexity")

            print("\n🎉 Configuration terminée ! Vous pouvez maintenant utiliser le script normalement.")

        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")

    @staticmethod
    def tester_glpi() -> bool:
        """Test rapide de la connexion GLPI"""
        try:
            api_url = os.getenv('GLPI_API_URL')
            app_token = os.getenv('GLPI_APP_TOKEN')
            user_token = os.getenv('GLPI_USER_TOKEN')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'user_token {user_token}',
                'App-Token': app_token
            }

            response = requests.get(f"{api_url}/initSession", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'session_token' in data:
                    # Fermer la session
                    requests.get(f"{api_url}/killSession", 
                               headers={'Session-Token': data['session_token'], 'App-Token': app_token})
                    return True
            return False
        except:
            return False

    @staticmethod
    def tester_perplexity() -> bool:
        """Test rapide de la connexion Perplexity"""
        try:
            api_key = os.getenv('PERPLEXITY_API_KEY')

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": "Test"}],
                "temperature": 0.1,
                "max_tokens": 10
            }

            response = requests.post("https://api.perplexity.ai/chat/completions", 
                                   headers=headers, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False


class GLPIConfig:
    """Configuration pour l'API GLPI"""
    def __init__(self):
        self.api_url = os.getenv('GLPI_API_URL', 'https://your-glpi-server.com/apirest.php')
        self.app_token = os.getenv('GLPI_APP_TOKEN', '')
        self.user_token = os.getenv('GLPI_USER_TOKEN', '')

        if not self.app_token or not self.user_token:
            logger.error("Variables d'environnement GLPI_APP_TOKEN et GLPI_USER_TOKEN requises")
            print("\n❌ Configuration manquante ! Utilisez: python glpi_ticket_automation.py --config")
            sys.exit(1)


class PerplexityConfig:
    """Configuration pour l'API Perplexity"""
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY', '')
        self.api_url = 'https://api.perplexity.ai/chat/completions'
        self.model = 'sonar-pro'

        if not self.api_key:
            logger.error("Variable d'environnement PERPLEXITY_API_KEY requise")
            print("\n❌ Configuration manquante ! Utilisez: python glpi_ticket_automation.py --config")
            sys.exit(1)


class PerplexityReformulator:
    """Classe pour la reformulation de texte via l'API Perplexity"""

    def __init__(self, config: PerplexityConfig):
        self.config = config
        self.instructions_manager = None  # Sera initialisé si nécessaire
        self.instructions = {}

    def charger_instructions_si_necessaire(self):
        """Charge les instructions si pas encore fait"""
        if not self.instructions:
            if not self.instructions_manager:
                self.instructions_manager = InstructionsManager()
            self.instructions = self.instructions_manager.instructions

    def reformuler_texte(self, texte: str, type_reformulation: str) -> str:
        """
        Reformule un texte via l'API Perplexity

        Args:
            texte: Le texte à reformuler
            type_reformulation: 'description' ou 'solution'

        Returns:
            Le texte reformulé
        """
        self.charger_instructions_si_necessaire()

        if type_reformulation not in self.instructions:
            raise ValueError(f"Type de reformulation invalide: {type_reformulation}")

        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": self.instructions[type_reformulation]},
                {"role": "user", "content": texte}
            ],
            "temperature": 0.05  # Température très basse pour minimiser la créativité
        }

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

        try:
            logger.info(f"🤖 Reformulation de la {type_reformulation} via Perplexity...")
            response = requests.post(self.config.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                texte_reformule = data['choices'][0]['message']['content'].strip()
                logger.info(f"✅ {type_reformulation.capitalize()} reformulée avec succès")
                return texte_reformule
            else:
                logger.error(f"❌ Réponse inattendue de l'API Perplexity: {data}")
                return texte

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur lors de la reformulation {type_reformulation}: {e}")
            return texte
        except Exception as e:
            logger.error(f"❌ Erreur inattendue lors de la reformulation: {e}")
            return texte


class InstructionsManager:
    """Gestionnaire des instructions de reformulation"""

    FICHIER_INSTRUCTIONS = 'instructions_reformulation.json'

    INSTRUCTIONS_PAR_DEFAUT = {
        'description': """Tu es un expert en support informatique. Reformule UNIQUEMENT le texte fourni de façon professionnelle.
RÈGLES STRICTES :
- Utilise SEULEMENT les informations présentes dans le texte original
- NE PAS inventer, ajouter ou imaginer d'informations supplémentaires
- NE PAS créer de détails techniques qui ne sont pas mentionnés
- NE PAS inclure les coordonnées du client (nom, téléphone, email, société)
- Garde EXACTEMENT le même niveau de détail que l'original
- Si le texte est court, la reformulation doit rester courte
- Si le texte est vague, la reformulation doit rester vague
- Style direct et professionnel
- Maximum 3 lignes
- Pas de formules de politesse
- Commence directement par le problème""",

        'solution': """Tu es un expert en support informatique. Reformule UNIQUEMENT cette solution de façon professionnelle.
RÈGLES ULTRA-STRICTES :
- Utilise SEULEMENT et EXCLUSIVEMENT les informations présentes dans le texte original
- NE PAS inventer, ajouter, imaginer ou déduire d'informations supplémentaires
- NE PAS créer de détails, étapes ou procédures qui ne sont pas explicitement mentionnés
- NE PAS suggérer de bonnes pratiques ou d'améliorations non mentionnées
- Si le texte dit "pas encore définie", reformule en gardant cette notion d'indéfini
- Si le texte est vague ou incomplet, la reformulation DOIT rester vague ou incomplète
- Garde EXACTEMENT le même niveau de détail et de précision que l'original
- Style direct et professionnel
- Maximum 2 lignes
- Pas de formules de politesse
- Commence directement par l'action ou l'état décrit"""
    }

    def __init__(self):
        self.instructions = self.charger_instructions()

    def charger_instructions(self) -> Dict[str, str]:
        """Charge les instructions depuis le fichier JSON ou utilise les valeurs par défaut"""
        try:
            if os.path.exists(self.FICHIER_INSTRUCTIONS):
                with open(self.FICHIER_INSTRUCTIONS, 'r', encoding='utf-8') as f:
                    instructions = json.load(f)
                    # Vérifier que toutes les clés nécessaires sont présentes
                    for key in self.INSTRUCTIONS_PAR_DEFAUT:
                        if key not in instructions:
                            instructions[key] = self.INSTRUCTIONS_PAR_DEFAUT[key]
                    return instructions
            else:
                return self.INSTRUCTIONS_PAR_DEFAUT.copy()
        except Exception as e:
            logger.warning(f"Erreur lors du chargement des instructions: {e}")
            return self.INSTRUCTIONS_PAR_DEFAUT.copy()

    def sauvegarder_instructions(self):
        """Sauvegarde les instructions dans le fichier JSON"""
        try:
            with open(self.FICHIER_INSTRUCTIONS, 'w', encoding='utf-8') as f:
                json.dump(self.instructions, f, ensure_ascii=False, indent=2)
            logger.info("Instructions sauvegardées")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des instructions: {e}")

    def configurer_instructions(self):
        """Configuration interactive des instructions de reformulation"""
        print("\n" + "=" * 70)
        print("  📝 CONFIGURATION DES INSTRUCTIONS DE REFORMULATION")
        print("=" * 70)

        while True:
            print("\n🎯 Que souhaitez-vous faire ?")
            print("1. Modifier les instructions de reformulation de DESCRIPTION")
            print("2. Modifier les instructions de reformulation de SOLUTION")
            print("3. Tester les instructions actuelles")
            print("4. Restaurer les instructions par défaut")
            print("5. Afficher les instructions actuelles")
            print("6. Retour au menu principal")

            choix = input("\n→ Votre choix (1-6): ").strip()

            if choix == '1':
                self.modifier_instruction('description')
            elif choix == '2':
                self.modifier_instruction('solution')
            elif choix == '3':
                self.tester_instructions()
            elif choix == '4':
                self.restaurer_defaut()
            elif choix == '5':
                self.afficher_instructions()
            elif choix == '6':
                break
            else:
                print("❌ Choix invalide")

    def modifier_instruction(self, type_instruction: str):
        """Modifie une instruction spécifique"""
        print(f"\n📝 MODIFICATION DE L'INSTRUCTION - {type_instruction.upper()}")
        print("-" * 50)

        print("\n📄 Instruction actuelle:")
        print(self.instructions[type_instruction])

        print("\n✏️  Saisissez la nouvelle instruction (appuyez deux fois sur Entrée pour valider):")
        print("   " + "-" * 50)

        lines = []
        consecutive_empty = 0

        while True:
            try:
                line = input("   ")
                if line == "":
                    consecutive_empty += 1
                    if consecutive_empty >= 2:
                        break
                    lines.append("")
                else:
                    consecutive_empty = 0
                    lines.append(line)
            except KeyboardInterrupt:
                print("\n⏹️  Modification annulée")
                return

        # Supprimer les lignes vides à la fin
        while lines and lines[-1] == "":
            lines.pop()

        nouvelle_instruction = "\n".join(lines)

        if nouvelle_instruction.strip():
            self.instructions[type_instruction] = nouvelle_instruction
            self.sauvegarder_instructions()
            print(f"\n✅ Instruction {type_instruction} mise à jour et sauvegardée")
        else:
            print("\n❌ Instruction vide, modification annulée")

    def tester_instructions(self):
        """Teste les instructions actuelles avec des exemples"""
        print("\n🧪 TEST DES INSTRUCTIONS DE REFORMULATION")
        print("-" * 50)

        # Vérifier que Perplexity est configuré
        if not os.getenv('PERPLEXITY_API_KEY'):
            print("❌ Clé API Perplexity non configurée. Utilisez --config d'abord.")
            return

        try:
            # Utiliser les classes déjà définies dans ce module (pas d'import nécessaire)
            perplexity_config = PerplexityConfig()
            reformulator = PerplexityReformulator(perplexity_config)
            reformulator.instructions = self.instructions

            # Test description
            print("\n📝 Test - Reformulation de DESCRIPTION:")
            texte_test_desc = input("Entrez un texte de description à tester: ").strip()
            if texte_test_desc:
                resultat_desc = reformulator.reformuler_texte(texte_test_desc, 'description')
                print(f"\n📄 Résultat: {resultat_desc}")

            # Test solution
            print("\n💡 Test - Reformulation de SOLUTION:")
            texte_test_sol = input("Entrez un texte de solution à tester: ").strip()
            if texte_test_sol:
                resultat_sol = reformulator.reformuler_texte(texte_test_sol, 'solution')
                print(f"\n📄 Résultat: {resultat_sol}")

        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")

    def restaurer_defaut(self):
        """Restaure les instructions par défaut"""
        confirmation = input("\n⚠️  Êtes-vous sûr de vouloir restaurer les instructions par défaut? (o/N): ")
        if confirmation.lower() in ['o', 'oui', 'y', 'yes']:
            self.instructions = self.INSTRUCTIONS_PAR_DEFAUT.copy()
            self.sauvegarder_instructions()
            print("✅ Instructions restaurées par défaut")
        else:
            print("⏹️  Restauration annulée")

    def afficher_instructions(self):
        """Affiche les instructions actuelles"""
        print("\n📄 INSTRUCTIONS ACTUELLES")
        print("=" * 50)

        for type_instr, instruction in self.instructions.items():
            print(f"\n🎯 {type_instr.upper()}:")
            print("-" * 30)
            print(instruction)


class GLPIManager:
    """Gestionnaire pour l'API GLPI"""

    def __init__(self, config: GLPIConfig):
        self.config = config
        self.session_token = None
        self.entities = {}
        self.categories = {}

    def authentification(self) -> bool:
        """
        Authentification auprès de l'API GLPI

        Returns:
            True si l'authentification réussit, False sinon
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'user_token {self.config.user_token}',
            'App-Token': self.config.app_token
        }

        try:
            logger.info("🔐 Initialisation de la session GLPI...")
            response = requests.get(f"{self.config.api_url}/initSession", headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            if 'session_token' in data:
                self.session_token = data['session_token']
                logger.info("✅ Authentification GLPI réussie")
                return True
            else:
                logger.error(f"❌ Token de session non trouvé: {data}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur d'authentification GLPI: {e}")
            return False

    def fermer_session(self):
        """Ferme la session GLPI"""
        if not self.session_token:
            return

        headers = {
            'Content-Type': 'application/json',
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        try:
            logger.info("🔒 Fermeture de la session GLPI...")
            response = requests.get(f"{self.config.api_url}/killSession", headers=headers, timeout=30)
            response.raise_for_status()
            logger.info("✅ Session GLPI fermée")
        except Exception as e:
            logger.warning(f"⚠️  Erreur lors de la fermeture de session: {e}")

    def rechercher_utilisateurs(self, search_term: str) -> List[Dict[str, Any]]:
        """Recherche des utilisateurs/demandeurs par terme de recherche"""
        headers = {
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        try:
            params = {
                'is_requester': True,
                'range': '0-1000'
            }

            response = requests.get(f"{self.config.api_url}/User", headers=headers, params=params, timeout=30)

            if response.status_code in [200, 206]:
                users = response.json()

                matching_users = []
                search_term_lower = search_term.lower()

                for user in users:
                    name = str(user.get('name', '')).lower()
                    realname = str(user.get('realname', '')).lower()
                    firstname = str(user.get('firstname', '')).lower()

                    if (search_term_lower in name or 
                        search_term_lower in realname or 
                        search_term_lower in firstname):
                        matching_users.append(user)

                if matching_users:
                    logger.info(f"✅ {len(matching_users)} utilisateur(s) trouvé(s) pour '{search_term}'")
                    return matching_users
                else:
                    logger.warning(f"⚠️  Aucun utilisateur ne correspond à '{search_term}'")
                    return []
            else:
                logger.error(f"❌ Erreur lors de la recherche d'utilisateurs. Code : {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"❌ Exception lors de la recherche d'utilisateurs : {str(e)}")
            return []

    def charger_toutes_entites(self) -> Dict[int, Dict[str, Any]]:
        """Charge toutes les entités avec leurs détails complets"""
        headers = {
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        toutes_entites = {}

        try:
            params = {
                'range': '0-1000'
            }

            response = requests.get(f"{self.config.api_url}/Entity", headers=headers, params=params, timeout=30)

            if response.status_code in [200, 206]:
                entities = response.json()

                for entity in entities:
                    if isinstance(entity, dict) and 'id' in entity:
                        toutes_entites[entity['id']] = entity

                logger.info(f"📋 {len(toutes_entites)} entités chargées")
                return toutes_entites
            else:
                logger.error(f"❌ Erreur lors du chargement des entités. Code : {response.status_code}")
                return {}

        except Exception as e:
            logger.error(f"❌ Exception lors du chargement des entités : {str(e)}")
            return {}

    def trouver_entite_utilisateur(self, user_id: int, nom_utilisateur: str) -> Optional[int]:
        """Trouve l'entité d'un utilisateur"""
        headers = {
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        try:
            response = requests.get(f"{self.config.api_url}/User/{user_id}", headers=headers, timeout=30)

            if response.status_code == 200:
                user_data = response.json()
                entity_id = user_data.get('entities_id')
                if entity_id:
                    logger.info(f"✅ Entité trouvée directement pour l'utilisateur {user_id}: {entity_id}")
                    return entity_id
        except Exception as e:
            logger.warning(f"⚠️  Erreur lors de la récupération directe de l'entité : {str(e)}")

        logger.info(f"🔍 Recherche de l'entité pour '{nom_utilisateur}' dans toutes les entités...")

        toutes_entites = self.charger_toutes_entites()
        nom_lower = nom_utilisateur.lower()

        entites_prioritaires = ['CLIENTS_HORS_CONTRAT', 'CLIENTS_SOUS_CONTRAT', 'COPIEUR']

        for entity_id, entity_data in toutes_entites.items():
            entity_name = str(entity_data.get('name', '')).lower()
            entity_completename = str(entity_data.get('completename', '')).lower()

            for prioritaire in entites_prioritaires:
                if prioritaire.lower() in entity_completename and nom_lower in entity_name:
                    logger.info(f"✅ Entité trouvée dans {prioritaire}: {entity_data['name']} (ID: {entity_id})")
                    logger.info(f"📍 Chemin complet: {entity_data.get('completename', '')}")
                    return entity_id

        for entity_id, entity_data in toutes_entites.items():
            entity_name = str(entity_data.get('name', '')).lower()

            if nom_lower in entity_name:
                logger.info(f"✅ Entité trouvée: {entity_data['name']} (ID: {entity_id})")
                logger.info(f"📍 Chemin complet: {entity_data.get('completename', '')}")
                return entity_id

        logger.warning(f"⚠️  Aucune entité trouvée pour '{nom_utilisateur}'")
        return None

    def charger_entites(self):
        """Charge la liste des entités"""
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        try:
            response = requests.get(f"{self.config.api_url}/Entity", headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            for entity in data:
                if isinstance(entity, dict) and 'id' in entity and 'name' in entity:
                    self.entities[entity['name']] = entity['id']

            logger.info(f"📋 {len(self.entities)} entités chargées")

        except Exception as e:
            logger.warning(f"⚠️  Erreur lors du chargement des entités: {e}")

    def charger_categories(self):
        """Charge la liste des catégories ITIL"""
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        try:
            response = requests.get(f"{self.config.api_url}/ITILCategory", headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            for category in data:
                if isinstance(category, dict) and 'id' in category and 'name' in category:
                    self.categories[category['name']] = category['id']

            logger.info(f"📂 {len(self.categories)} catégories chargées")

        except Exception as e:
            logger.warning(f"⚠️  Erreur lors du chargement des catégories: {e}")

    def creer_ticket(self, ticket_data: Dict[str, Any]) -> Optional[int]:
        """Crée un ticket dans GLPI"""
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        payload = {"input": ticket_data}

        try:
            logger.info("🎫 Création du ticket dans GLPI...")
            response = requests.post(f"{self.config.api_url}/Ticket", headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            if isinstance(data, dict) and 'id' in data:
                ticket_id = data['id']
                logger.info(f"✅ Ticket créé avec l'ID: {ticket_id}")
                return ticket_id
            elif isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                ticket_id = data[0]['id']
                logger.info(f"✅ Ticket créé avec l'ID: {ticket_id}")
                return ticket_id
            else:
                logger.error(f"❌ Réponse inattendue lors de la création: {data}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur lors de la création du ticket: {e}")
            return None

    def ajouter_solution(self, ticket_id: int, solution: str) -> bool:
        """Ajoute une solution à un ticket via ITILSolution"""
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        solution_data = {
            'itemtype': 'Ticket',
            'items_id': ticket_id,
            'content': solution,
            'solutiontype_id': 1
        }

        payload = {"input": solution_data}

        try:
            logger.info(f"💡 Ajout de solution au ticket {ticket_id}...")
            response = requests.post(f"{self.config.api_url}/ITILSolution", headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info("✅ Solution ajoutée avec succès")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur lors de l'ajout de solution: {e}")
            logger.error(f"Réponse: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            return False

    def mettre_a_jour_statut(self, ticket_id: int, statut: int) -> bool:
        """Met à jour le statut d'un ticket"""
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': self.session_token,
            'App-Token': self.config.app_token
        }

        payload = {"input": {"status": statut}}

        try:
            logger.info(f"📝 Mise à jour du statut du ticket {ticket_id} vers {statut}...")
            response = requests.put(f"{self.config.api_url}/Ticket/{ticket_id}", headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            logger.info("✅ Statut mis à jour avec succès")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur lors de la mise à jour du statut: {e}")
            return False


class TicketCollector:
    """Collecteur d'informations pour le ticket"""

    @staticmethod
    def afficher_banniere():
        """Affiche une bannière d'accueil"""
        print("\n" + "=" * 70)
        print("  🎫 SCRIPT D'AUTOMATISATION DE TICKETS GLPI 🎫")
        print("=" * 70)
        print("  📋 Création automatique avec reformulation IA")
        print("  🤖 Powered by Perplexity AI")
        print("=" * 70)

    @staticmethod
    def valider_email(email: str) -> bool:
        """Valide le format d'un email"""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def valider_telephone(telephone: str) -> bool:
        """Valide le format d'un numéro de téléphone français"""
        pattern = r'^0[1-9](\s?\d{2}){4}$'
        return re.match(pattern, telephone.replace(' ', '')) is not None

    @staticmethod
    def valider_numero_serie(numero_serie: str) -> bool:
        """Valide le format d'un numéro de série"""
        if not numero_serie:
            return True
        pattern = r'^[A-Za-z0-9_-]+$'
        return re.match(pattern, numero_serie) is not None

    @staticmethod
    def saisir_texte_multiligne(prompt: str) -> str:
        """Saisie de texte multiligne avec double Entrée pour valider"""
        print(f"\n📝 {prompt}")
        print("   💡 Astuce: Appuyez sur Entrée pour un saut de ligne")
        print("   ✅ Appuyez deux fois sur Entrée pour valider")
        print("   " + "-" * 50)

        lines = []
        consecutive_empty = 0

        while True:
            try:
                line = input("   ")
                if line == "":
                    consecutive_empty += 1
                    if consecutive_empty >= 2:
                        break
                    lines.append("")
                else:
                    consecutive_empty = 0
                    lines.append(line)
            except KeyboardInterrupt:
                print("\n⏹️  Saisie annulée")
                return ""

        while lines and lines[-1] == "":
            lines.pop()

        return "\n".join(lines)

    @staticmethod
    def collecter_informations() -> Dict[str, str]:
        """Collecte les informations du ticket via CLI interactif"""
        TicketCollector.afficher_banniere()

        informations = {}

        print("\n📋 COLLECTE DES INFORMATIONS DU TICKET")
        print("=" * 50)

        # Titre du ticket
        while True:
            print("\n🎯 Titre du ticket:")
            titre = input("   → ").strip()
            if titre:
                informations['titre'] = titre
                break
            print("   ❌ Le titre ne peut pas être vide")

        # Nom de l'appelant
        while True:
            print("\n👤 Nom de l'appelant:")
            nom_appelant = input("   → ").strip()
            if nom_appelant:
                informations['nom_appelant'] = nom_appelant
                break
            print("   ❌ Le nom de l'appelant ne peut pas être vide")

        # Numéro de téléphone
        while True:
            print("\n📱 Numéro de téléphone:")
            telephone = input("   → ").strip()
            if telephone:
                if TicketCollector.valider_telephone(telephone):
                    informations['telephone'] = telephone
                    break
                else:
                    print("   ❌ Format invalide (ex: 01 23 45 67 89)")
            else:
                print("   ❌ Le numéro de téléphone ne peut pas être vide")

        # Numéro de série du copieur
        while True:
            print("\n🖨️  Numéro de série du copieur (optionnel):")
            print("   💡 Laissez vide si l'incident ne concerne pas un copieur")
            numero_serie = input("   → ").strip()
            if TicketCollector.valider_numero_serie(numero_serie):
                if numero_serie:
                    informations['numero_serie'] = numero_serie
                break
            else:
                print("   ❌ Format invalide (lettres, chiffres, tirets et underscores uniquement)")

        # Adresse email
        while True:
            print("\n📧 Adresse email (optionnelle):")
            email = input("   → ").strip()
            if TicketCollector.valider_email(email):
                informations['email'] = email if email else "Non renseigné"
                break
            else:
                print("   ❌ Format d'email invalide")

        # Description du problème
        while True:
            description = TicketCollector.saisir_texte_multiligne("Description du problème/incident:")
            if description.strip():
                informations['description'] = description
                break
            print("   ❌ La description ne peut pas être vide")

        # Nom du demandeur
        while True:
            print("\n🏢 Nom du demandeur (utilisateur GLPI):")
            demandeur = input("   → ").strip()
            if demandeur:
                informations['demandeur'] = demandeur
                break
            print("   ❌ Le nom du demandeur ne peut pas être vide")

        # Type de ticket
        types_tickets = {
            '1': 'Incident',
            '2': 'Demande'
        }

        print("\n🎫 Type de ticket:")
        for key, value in types_tickets.items():
            print(f"   {key}. {value}")

        while True:
            type_ticket = input("   → Votre choix (1-2): ").strip()
            if type_ticket in types_tickets:
                informations['type_ticket'] = type_ticket
                informations['type_ticket_nom'] = types_tickets[type_ticket]
                break
            print("   ❌ Choix invalide")

        return informations

    @staticmethod
    def formater_ticket(informations: Dict[str, str], description_finale: str, nom_client_reel: str) -> str:
        """Formate les informations du ticket selon le template spécifié"""
        template = f"""👥 Nom du client : {nom_client_reel}
👤 Nom de l'appelant : {informations['nom_appelant']}
📱 Numéro de téléphone : {informations['telephone']}"""

        if 'numero_serie' in informations and informations['numero_serie']:
            template += f"\n🖨️ Numéro de série du copieur : {informations['numero_serie']}"

        template += f"""
📧 E-mail : {informations['email']}
\n \n📝 Description de l'incident :
{description_finale}"""

        return template


def afficher_aide():
    """Affiche l'aide du script"""
    print("""
🎫 SCRIPT D'AUTOMATISATION DE TICKETS GLPI
==========================================

UTILISATION:
  python glpi_ticket_automation.py [OPTIONS]

OPTIONS:
  --config         Configuration interactive des variables d'environnement
  --instructions   Configuration des instructions de reformulation IA
  --help, -h       Affiche cette aide

EXEMPLES:
  python glpi_ticket_automation.py --config
    └─ Configure les tokens GLPI et la clé Perplexity

  python glpi_ticket_automation.py --instructions  
    └─ Modifie les instructions de reformulation

  python glpi_ticket_automation.py
    └─ Lance le script normal de création de tickets

PRÉREQUIS:
  - Fichier .env configuré (utilisez --config)
  - Instructions de reformulation (utilisez --instructions si besoin)
""")


def main_creation_tickets():
    """Fonction principale de création de tickets"""
    try:
        # Configuration
        glpi_config = GLPIConfig()
        perplexity_config = PerplexityConfig()

        # Initialisation des managers
        glpi = GLPIManager(glpi_config)
        reformulator = PerplexityReformulator(perplexity_config)

        # Authentification GLPI
        if not glpi.authentification():
            logger.error("❌ Échec de l'authentification GLPI")
            sys.exit(1)

        # Chargement des données GLPI
        glpi.charger_entites()
        glpi.charger_categories()

        try:
            # Collecte des informations
            informations = TicketCollector.collecter_informations()

            print("\n" + "=" * 70)
            print("  📝 RÉSUMÉ DES INFORMATIONS COLLECTÉES")
            print("=" * 70)
            print(f"🎯 Titre: {informations['titre']}")
            print(f"👤 Appelant: {informations['nom_appelant']}")
            print(f"🏢 Demandeur recherché: {informations['demandeur']}")
            print(f"🎫 Type: {informations['type_ticket_nom']}")

            # Recherche de l'utilisateur/demandeur
            print("\n🔍 RECHERCHE DE L'UTILISATEUR DANS GLPI")
            print("=" * 50)

            users_found = glpi.rechercher_utilisateurs(informations['demandeur'])
            user_id = None
            entity_id = 1
            nom_client_reel = informations['demandeur']

            if users_found:
                if len(users_found) == 1:
                    user_id = users_found[0]['id']
                    user_name = users_found[0].get('name', 'Inconnu')
                    nom_client_reel = user_name.upper()
                    print(f"✅ Utilisateur trouvé: {user_name} (ID: {user_id})")
                    print(f"✅ Nom du client qui sera utilisé: {nom_client_reel}")

                    entity_id = glpi.trouver_entite_utilisateur(user_id, user_name)
                    if not entity_id:
                        entity_id = 1
                        print("⚠️  Utilisation de l'entité par défaut (ID: 1)")

                else:
                    print(f"🔍 Plusieurs utilisateurs trouvés ({len(users_found)}):")
                    for i, user in enumerate(users_found, 1):
                        user_info = []
                        if user.get('id'):
                            user_info.append(f"ID: {user['id']}")
                        if user.get('name'):
                            user_info.append(f"Nom: {user['name']}")
                        if user.get('firstname'):
                            user_info.append(f"Prénom: {user['firstname']}")
                        if user.get('realname'):
                            user_info.append(f"Nom complet: {user['realname']}")

                        print(f"   {i}. " + " - ".join(user_info))

                    while True:
                        try:
                            choix = input("\n→ Choisir un utilisateur (numéro) ou Entrée pour défaut: ").strip()
                            if not choix:
                                break
                            choix_idx = int(choix) - 1
                            if 0 <= choix_idx < len(users_found):
                                user_id = users_found[choix_idx]['id']
                                user_name = users_found[choix_idx].get('name', 'Inconnu')
                                nom_client_reel = user_name.upper()
                                print(f"✅ Utilisateur sélectionné: {user_name}")
                                print(f"✅ Nom du client qui sera utilisé: {nom_client_reel}")

                                entity_id = glpi.trouver_entite_utilisateur(user_id, user_name)
                                if not entity_id:
                                    entity_id = 1
                                    print("⚠️  Utilisation de l'entité par défaut (ID: 1)")
                                break
                        except (ValueError, IndexError):
                            print("❌ Choix invalide")
            else:
                print(f"⚠️  Utilisateur '{informations['demandeur']}' non trouvé")
                print(f"⚠️  Nom du client utilisé par défaut: {nom_client_reel}")
                print("⚠️  Utilisation de l'entité par défaut (ID: 1)")

            # Attribution à un technicien
            print("\n👨‍💻 ATTRIBUTION DU TECHNICIEN")
            print("=" * 50)
            print("💡 Technicien par défaut: ID 233")

            technicien_id = input("→ Entrez l'ID du technicien ou laissez vide pour le défaut (233): ").strip()
            if not technicien_id or not technicien_id.isdigit():
                technicien_id = 233
                print(f"✅ Utilisation du technicien par défaut: ID {technicien_id}")
            else:
                technicien_id = int(technicien_id)
                print(f"✅ Technicien sélectionné: ID {technicien_id}")

            # Reformulation de la description
            print("\n🤖 REFORMULATION IA DE LA DESCRIPTION")
            print("=" * 50)

            description_reformulee = reformulator.reformuler_texte(
                informations['description'], 
                'description'
            )

            print("\n📄 APERÇU DES DESCRIPTIONS:")
            print("-" * 30)
            print("📝 Description originale:")
            print(f"   {informations['description']}")
            print("\n🤖 Description reformulée:")
            print(f"   {description_reformulee}")

            validation = input("\n❓ Accepter la reformulation? (o/N): ").strip().lower()

            if validation in ['o', 'oui', 'y', 'yes']:
                print("✅ Reformulation acceptée")
                description_finale = description_reformulee
            else:
                print("⏹️  Utilisation de la description originale")
                description_finale = informations['description']

            # Création du contenu final du ticket avec le nom réel du client
            contenu_final_ticket = TicketCollector.formater_ticket(informations, description_finale, nom_client_reel)

            print("\n📋 APERÇU DU TICKET FINAL:")
            print("-" * 50)
            print(contenu_final_ticket)

            # Préparation des données du ticket
            ticket_data = {
                "name": informations['titre'],
                "content": contenu_final_ticket,
                "entities_id": entity_id,
                "type": int(informations['type_ticket']),
                "status": 1,
                "_users_id_assign": technicien_id
            }

            if user_id:
                ticket_data["_users_id_requester"] = user_id

            # Ajout de catégorie si disponible
            if glpi.categories:
                print("\n📂 SÉLECTION DE CATÉGORIE (OPTIONNEL)")
                print("=" * 50)
                categories_list = list(glpi.categories.items())

                # Afficher TOUTES les catégories sans limitation
                for i, (nom, cat_id) in enumerate(categories_list, 1):
                    print(f"   {i}. {nom}")

                # Validation avec gestion d'erreurs améliorée
                while True:
                    try:
                        choix_cat = input("\n→ Choisir une catégorie (numéro) ou Entrée pour ignorer: ").strip()
                        if not choix_cat:
                            print("⏩ Aucune catégorie sélectionnée")
                            break

                        if choix_cat.isdigit():
                            cat_index = int(choix_cat) - 1
                            if 0 <= cat_index < len(categories_list):
                                cat_nom, cat_id = categories_list[cat_index]
                                ticket_data["itilcategories_id"] = cat_id
                                print(f"✅ Catégorie sélectionnée: {cat_nom}")
                                break
                            else:
                                print(f"❌ Numéro invalide. Veuillez choisir entre 1 et {len(categories_list)}")
                        else:
                            print("❌ Veuillez entrer un numéro valide ou appuyer sur Entrée pour ignorer")
                    except (ValueError, IndexError):
                        print("❌ Erreur de saisie. Veuillez entrer un numéro valide")

            # Création du ticket
            print("\n🎫 CRÉATION DU TICKET DANS GLPI")
            print("=" * 50)

            ticket_id = glpi.creer_ticket(ticket_data)

            if not ticket_id:
                print("❌ Échec de la création du ticket")
                return

            print(f"\n🎉 TICKET CRÉÉ AVEC SUCCÈS!")
            print(f"🆔 ID du ticket: {ticket_id}")

            # Demande de résolution
            print("\n💡 AJOUT D'UNE SOLUTION (OPTIONNEL)")
            print("=" * 50)

            resolution = input("❓ Voulez-vous ajouter une solution à ce ticket? (o/N): ").strip().lower()

            if resolution in ['o', 'oui', 'y', 'yes']:
                solution_text = TicketCollector.saisir_texte_multiligne("Saisissez la solution:")

                if solution_text.strip():
                    print("\n🤖 Reformulation de la solution...")
                    solution_reformulee = reformulator.reformuler_texte(
                        solution_text, 
                        'solution'
                    )

                    print("\n📄 APERÇU DES SOLUTIONS:")
                    print("-" * 30)
                    print("📝 Solution originale:")
                    print(f"   {solution_text}")
                    print("\n🤖 Solution reformulée:")
                    print(f"   {solution_reformulee}")

                    validation_sol = input("\n❓ Accepter la reformulation? (o/N): ").strip().lower()

                    if validation_sol in ['o', 'oui', 'y', 'yes']:
                        print("✅ Reformulation acceptée")
                        solution_finale = solution_reformulee
                    else:
                        print("⏹️  Utilisation de la solution originale")
                        solution_finale = solution_text

                    # Ajout de la solution
                    if glpi.ajouter_solution(ticket_id, solution_finale):
                        print("✅ Solution ajoutée avec succès")

                        # Demande de clôture
                        cloture = input("\n❓ Voulez-vous clôturer ce ticket? (o/N): ").strip().lower()

                        if cloture in ['o', 'oui', 'y', 'yes']:
                            if glpi.mettre_a_jour_statut(ticket_id, 6):
                                print("✅ Ticket clôturé avec succès")
                            else:
                                print("❌ Échec de la clôture du ticket")
                    else:
                        print("❌ Échec de l'ajout de la solution")

            print("\n" + "=" * 70)
            print(f"  🎉 PROCESSUS TERMINÉ AVEC SUCCÈS!")
            print(f"  🆔 Ticket ID: {ticket_id}")
            print("=" * 70)

        finally:
            glpi.fermer_session()

    except KeyboardInterrupt:
        print("\n\n⏹️  Script interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        sys.exit(1)


def main():
    """Point d'entrée principal avec gestion des arguments"""
    parser = argparse.ArgumentParser(
        description="Script d'automatisation de tickets GLPI avec reformulation IA",
        add_help=False
    )
    parser.add_argument('--config', action='store_true', 
                       help='Configuration interactive des variables d\'environnement')
    parser.add_argument('--instructions', action='store_true',
                       help='Configuration des instructions de reformulation')
    parser.add_argument('--help', '-h', action='store_true',
                       help='Affiche cette aide')

    args = parser.parse_args()

    if args.help:
        afficher_aide()
        return

    if args.config:
        ConfigManager.configurer_environnement()
        return

    if args.instructions:
        instructions_manager = InstructionsManager()
        instructions_manager.configurer_instructions()
        return

    # Mode normal - création de tickets
    main_creation_tickets()


if __name__ == "__main__":
    main()
