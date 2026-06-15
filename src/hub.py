from src.agents.gmail_agent import GmailAgent

class AgentHub:
    """
    Central hub to manage and access all Google ADK agents.
    This allows for a single entry point to instantiate and use multiple specialized agents.
    """
    def __init__(self):
        self._agents = {}

    def get_agent(self, agent_name):
        """
        Returns a singleton instance of the requested agent.
        If the agent hasn't been created yet, it will be instantiated.
        """
        if agent_name == 'gmail':
            if 'gmail' not in self._agents:
                print("Initializing Gmail Agent...")
                self._agents['gmail'] = GmailAgent()
            return self._agents['gmail']

        # Future agents can be added here
        # elif agent_name == 'calendar':
        #     if 'calendar' not in self._agents:
        #         self._agents['calendar'] = CalendarAgent()
        #     return self._agents['calendar']

        raise ValueError(f"Agent '{agent_name}' is not registered in the Hub.")

    def list_agents(self):
        """Returns a list of all available agents in the hub."""
        return list(self._agents.keys())

if __name__ == "__main__":
    # Example usage of the AgentHub
    hub = AgentHub()

    # Access the Gmail Agent
    gmail = hub.get_agent('gmail')

    # Use the Gmail agent's professional capabilities
    gmail.send_email(
        to=["test1@example.com", "test2@example.com"],
        subject="Hub Test",
        body="Hello from the AgentHub!",
        cc="boss@example.com",
        is_html=False
    )

    print(f"Active agents in hub: {hub.list_agents()}")
