import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ToolAgent:
    def __init__(self, tools=None):
        self.tools = tools or []

    def execute_task(self, task):
        task_lower = task.lower()
        if 'weather' in task_lower or 'temperature' in task_lower or 'hot' in task_lower:
            # Extract city names (handle multiple cities and different formats)
            import re
            cities = []
            # Check for cities after 'in'
            in_cities = re.findall(r'in ([a-zA-Z\s,]+)', task_lower)
            if in_cities:
                # Split multiple cities by 'and' or ','
                for city_group in in_cities:
                    cities.extend([c.strip() for c in re.split(r'(?:,|\sand\s)', city_group)])
            else:
                # Try to find city names at the end of the query
                city_match = re.search(r'(?:weather|temperature|hot)(?:\sin\s)?([a-zA-Z\s,]+)', task_lower)
                if city_match:
                    cities = [c.strip() for c in re.split(r'(?:,|\sand\s)', city_match.group(1))]

            if not cities:
                return "Could not identify city name in the query."

            api_key = os.getenv("OPENWEATHER_API_KEY")
            if not api_key:
                return "OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY in your .env file."

            results = []
            for city in cities:
                try:
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    response = requests.get(url)
                    data = response.json()
                    if data.get('cod') != 200:
                        results.append(f"Weather API error for {city}: {data.get('message', 'Unknown error')}")
                        continue
                    temp = data['main']['temp']
                    desc = data['weather'][0]['description']
                    results.append(f"The temperature in {city.title()} is {temp}°C with {desc}")
                except Exception as e:
                    results.append(f"Weather API error for {city}: {e}")
            
            return "\n".join(results)
        elif 'news' in task_lower:
            api_key = os.getenv("NEWS_API_KEY")
            if not api_key:
                return "NewsAPI key not found. Please set NEWS_API_KEY in your .env file."
            try:
                url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
                response = requests.get(url)
                data = response.json()
                if data.get('status') != 'ok':
                    return f"News API error: {data.get('message', 'Unknown error')}"
                articles = data.get('articles', [])
                if not articles:
                    return "No news articles found."
                # Get top 3 headlines
                summaries = [f"- {article['title']}" for article in articles[:3]]
                return "Today's top news:\n" + "\n".join(summaries)
            except Exception as e:
                return f"News API error: {e}"
        elif any(char.isdigit() for char in task_lower):
            import re
            # Extract the math expression from the task string
            match = re.search(r'([-+*/\d\s\.]+)', task_lower)
            if match:
                expr = match.group(1)
                try:
                    result = eval(expr)
                    return f"The result is {result}."
                except Exception:
                    return "Could not calculate the expression."
            else:
                return "Could not find a valid math expression."
        else:
            return f"Result for '{task}': [solution here]"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def modify_task(self, task_index, new_task):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index] = new_task
        else:
            raise IndexError("Task index out of range.")

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
        else:
            raise IndexError("Task index out of range.")

    def execute_tasks(self):
        results = []
        for task in self.tasks:
            result = self.execute_task(task)
            results.append(result)
        return results

    def execute_task(self, task):
        # Placeholder for task execution logic
        return f"Executed task: {task}"