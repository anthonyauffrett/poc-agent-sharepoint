import asyncio
from dotenv import load_dotenv
from semantic_kernel.contents import ChatMessageContent, AuthorRole
from .agent import creer_agents

load_dotenv()

def extraire_texte(msg) -> str:
    if hasattr(msg, 'content') and isinstance(msg.content, str):
        return msg.content
    if hasattr(msg, 'items'):
        return " ".join(
            item.text for item in msg.items
            if hasattr(item, 'text')
        )
    return str(msg)

async def conversation():
    print("\n" + "="*60)
    print("  Agent IA documentaire SharePoint — DSI Groupe Horizon")
    print("="*60)
    print("  Tapez 'quitter' pour terminer la session.")
    print("="*60 + "\n")

    expert, formateur = creer_agents()

    while True:
        question = input("Vous : ").strip()
        if question.lower() in ["quitter", "exit", "q"]:
            print("\nSession terminée.")
            break
        if not question:
            continue

        print("\n[Recherche dans les documents...]\n")

        # Agent 1 — réponse technique
        history_expert = [
            ChatMessageContent(role=AuthorRole.USER, content=question)
        ]
        reponse_technique = ""
        async for msg in expert.invoke(history_expert):
            reponse_technique = extraire_texte(msg)

        print(f"Expert : {reponse_technique}\n")

        # Agent 2 — reformulation
        history_formateur = [
            ChatMessageContent(role=AuthorRole.USER, content=question),
            ChatMessageContent(role=AuthorRole.ASSISTANT, content=reponse_technique),
            ChatMessageContent(
                role=AuthorRole.USER,
                content="Reformule cette réponse simplement pour un utilisateur non technique."
            )
        ]
        async for msg in formateur.invoke(history_formateur):
            print(f"Formateur : {extraire_texte(msg)}\n")

        print("-"*60 + "\n")

if __name__ == "__main__":
    asyncio.run(conversation())