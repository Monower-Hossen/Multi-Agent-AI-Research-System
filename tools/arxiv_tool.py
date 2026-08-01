import arxiv

def search_arxiv(query: str):
    try:
        client = arxiv.Client()
        search_query = arxiv.Search(
            query=query,
            max_results=3,
            sort_by=arxiv.SortCriterion.Relevance
        )
        # Safe iteration without calling .results directly if it's already an iterable
        results = []
        for paper in client.results(search_query):
            results.append({
                "title": paper.title,
                "summary": paper.summary,
                "pdf_url": paper.pdf_url
            })
        return results
    except Exception as e:
        return f"Arxiv error: {str(e)}"