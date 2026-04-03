class Memory:
    """
    Stores the last N input/output pairs to provide conversational context
    to the LLM on subsequent calls.
    """

    def __init__(self, max_history: int = 5):
        self.history = []
        self.max_history = max_history

    def add(self, input_text: str, output: dict):
        """Add a new input/output pair to memory."""
        self.history.append({"input": input_text, "output": output})

    def get(self) -> list:
        """Return the most recent entries (up to max_history)."""
        return self.history[-self.max_history :]

    def clear(self):
        """Reset the memory history."""
        self.history = []


# Module-level instance shared across the application
memory = Memory()
