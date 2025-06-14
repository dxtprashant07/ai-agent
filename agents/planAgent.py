class PlanAgent:
    def __init__(self):
        self.tasks = []

    def analyze_query(self, query):
        tasks = []
        
        # Handle queries with numbers and currency
        if '₹' in query or 'Rs' in query.lower() or 'INR' in query.lower():
            # Keep the entire query as one task
            tasks.append(query.strip())
            return tasks
            
        # Split by commas and 'and'
        parts = [p.strip() for part in query.split(',') for p in part.split(' and ')]
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            tasks.append(part)
        
        return [t for t in tasks if t]  # Remove any empty tasks

    def generate_task_list(self):
        # Return the structured task list
        return self.tasks

    def refine_tasks(self, modifications):
        # Modify, delete, or add tasks based on feedback
        for modification in modifications:
            action, task = modification.get('action'), modification.get('task')
            if action == 'add':
                self.tasks.append(task)
            elif action == 'delete' and task in self.tasks:
                self.tasks.remove(task)
            elif action == 'modify' and task in self.tasks:
                index = self.tasks.index(task)
                self.tasks[index] = modification.get('new_task', task)
        return self.tasks

    def clear_tasks(self):
        # Clear the current task list
        self.tasks = []
        return self.tasks