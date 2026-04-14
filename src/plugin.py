from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from semantic_kernel.functions import kernel_function
import os

class SharePointSearchPlugin:
    def __init__(self):
        self.client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )

    @kernel_function(
    name="rechercher_documents",
    description="Recherche des informations dans les documents SharePoint internes de la DSI"
)
    
    def rechercher(self, query: str) -> str:
        results = self.client.search(
            search_text=query,
            top=8,
            select=["chunk", "title"]
        )
        docs = []
        for r in results:
            chunk = r.get("chunk", "")
            if len(chunk) < 150:
                continue
            source = r.get("title", "inconnu")
            docs.append(f"[Source: {source}]\n{chunk[:600]}")

        return "\n\n---\n\n".join(docs) if docs else "Aucun document pertinent trouvé."