"""Integration tests for upgraded dependencies."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test all critical imports work."""
    from agents.agent_base import AgentBase
    from agents.conversation_agent import ConversationAgent
    from agents.scenario_agent import ScenarioAgent
    from agents.vocab_agent import VocabAgent
    from agents.session_history import get_session_history
    assert True

def test_session_history():
    """Test session history creation."""
    from agents.session_history import get_session_history
    history = get_session_history("test_session")
    assert history is not None
    assert len(history.messages) == 0

def test_conversation_agent_creation():
    """Test ConversationAgent can be instantiated."""
    from agents.conversation_agent import ConversationAgent
    agent = ConversationAgent(session_id="test_conv")
    assert agent.name == "conversation"
    assert agent.session_id == "test_conv"

if __name__ == "__main__":
    test_imports()
    print("✓ Import test passed")

    test_session_history()
    print("✓ Session history test passed")

    test_conversation_agent_creation()
    print("✓ Conversation agent test passed")

    print("\nAll integration tests passed!")
