import sys
sys.path.append("..")

import unittest
from unittest.mock import MagicMock
from conversational_agent import ConversationalAgent

class TestConversationalAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ConversationalAgent()

    def test_fetch_model(self):
        # Mocking the return value of ChatOpenAI instance
        mock_llm = MagicMock()
        self.agent.fetch_model = MagicMock(return_value=mock_llm)

        llm = self.agent.fetch_model()

        self.assertEqual(llm, mock_llm)
        self.agent.fetch_model.assert_called_once()

    def test_get_retriever(self):
        retriever = self.agent.get_retriever()

        # Ensure retriever is not None
        self.assertIsNotNone(retriever)

    def test_get_crc(self):
        # Mocking the return value of fetch_model and get_retriever
        mock_llm = MagicMock()
        mock_retriever = MagicMock()
        self.agent.fetch_model = MagicMock(return_value=mock_llm)
        self.agent.get_retriever = MagicMock(return_value=mock_retriever)

        crc = self.agent.get_crc()

        # Ensure ConversationalRetrievalChain is returned
        self.agent.fetch_model.assert_called_once()
        self.agent.get_retriever.assert_called_once()


if __name__ == '__main__':
    unittest.main()
