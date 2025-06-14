import requests
from datetime import datetime

class SearchTool:
    def __init__(self):
        self.search_url = "https://api.duckduckgo.com/"
    
    def search(self, query):
        # Check if query is about future
        current_year = datetime.now().year
        query_lower = query.lower()
        query_years = [int(word) for word in query_lower.split() if word.isdigit() and int(word) > current_year]
        
        # If query is about future predictions, don't use search
        if query_years:
            return "FUTURE_QUERY"
        
        try:
            # Remove year references for better current results
            search_query = ' '.join(word for word in query.split() if not word.isdigit())
            
            params = {
                'q': search_query,
                'format': 'json'
            }
            response = requests.get(self.search_url, params=params)
            data = response.json()
            
            if not data.get('RelatedTopics'):
                return "No results found."
            
            # Get top 3 results
            results = []
            for topic in data['RelatedTopics'][:3]:
                if 'Text' in topic:
                    results.append(topic['Text'])
            
            if not results:
                return "No relevant results found."
                
            return "\n\n".join([f"{i+1}. {result}" for i, result in enumerate(results)])
        except Exception as e:
            return f"Search error: {str(e)}"