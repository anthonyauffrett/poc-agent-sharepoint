from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from .plugin import SharePointSearchPlugin
import os

INSTRUCTIONS_EXPERT = """Tu es un assistant documentaire expert en gestion de projets SharePoint pour la DSI Groupe Horizon.
Tu réponds UNIQUEMENT en te basant sur les documents disponibles dans ta base de connaissances.
Tu utilises TOUJOURS l'outil rechercher_documents avant de répondre.
Si l'information n'est pas dans les documents, dis-le explicitement sans inventer.
Tu cites toujours le document source entre crochets à la fin de ta réponse.
Tu réponds toujours en français."""

INSTRUCTIONS_FORMATEUR = """Tu reçois une réponse technique sur SharePoint et tu la reformules
de façon claire et concise pour un utilisateur non technique.
Commence toujours par 'En résumé :'.
Conserve les informations chiffrées importantes (quotas, délais, nombres).
Tu réponds toujours en français."""

def creer_service():
    return AzureChatCompletion(
        deployment_name="gpt-4o",
        endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_KEY"),
        api_version="2024-02-01"
    )

def creer_agents():
    kernel = Kernel()
    service = creer_service()
    kernel.add_service(service)
    kernel.add_plugin(SharePointSearchPlugin(), plugin_name="SharePoint")

    expert = ChatCompletionAgent(
        service=creer_service(),
        kernel=kernel,
        name="ExpertSharePoint",
        instructions=INSTRUCTIONS_EXPERT
    )

    formateur = ChatCompletionAgent(
        service=creer_service(),
        name="Formateur",
        instructions=INSTRUCTIONS_FORMATEUR
    )

    return expert, formateur