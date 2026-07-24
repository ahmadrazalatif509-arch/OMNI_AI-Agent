from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 4) -> str:
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}")
        return "\n\n".join(results) if results else "No relevant search results found."
    except Exception as e:
        return f"Search error: {str(e)}"