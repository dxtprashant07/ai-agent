class PlanAgent:
    def __init__(self):
        self.tasks = []

    def analyze_query(self, query):
        # Analyze the user query and generate sub-tasks
        # This is a placeholder for actual analysis logic
        sub_tasks = query.split(",")  # Simple split for demonstration
        self.tasks = [task.strip() for task in sub_tasks]
        return self.tasks

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