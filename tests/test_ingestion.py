import sys
sys.path.append("..")

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from ingestion import read_urls_from_file, load_documents_from_urls, ingest_and_save_embeddings

class TestIngestionScript(unittest.TestCase):
    
    def test_read_urls_from_file(self):
        file_content = "https://google.com\nhttps://yahoo.com"
        expected_urls = ["https://google.com", "https://yahoo.com",]
        
        with patch('builtins.open', unittest.mock.mock_open(read_data=file_content)):
            urls = read_urls_from_file('testuris.txt')
            print("urls read")
            self.assertEqual(urls, expected_urls)
    
    @patch('ingestion.WebBaseLoader')
    @patch('ingestion.RecursiveCharacterTextSplitter')
    @patch('ingestion.logging')
    def test_load_documents_from_urls(self, mock_logging, mock_splitter, mock_loader):
        urls = ['https://google.com', 'https://yahoo.com']
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = "Sample document content"
        mock_loader.return_value = mock_loader_instance
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_documents.return_value = ["Chunk1", "Chunk2"]
        mock_splitter.return_value = mock_splitter_instance
        
        result = load_documents_from_urls(urls, mock_splitter_instance)
        
        self.assertEqual(result, ["Chunk1", "Chunk2", "Chunk1", "Chunk2"])
        self.assertEqual(mock_logging.info.call_count, 2)
        self.assertEqual(mock_logging.error.call_count, 0)
    
    @patch('ingestion.Path')
    @patch('ingestion.read_urls_from_file')
    @patch('ingestion.load_documents_from_urls')
    @patch('ingestion.HuggingFaceEmbeddings')
    @patch('ingestion.FAISS')
    @patch('ingestion.logging')
    def test_ingest_and_save_embeddings(self, mock_logging, mock_faiss, mock_embeddings, mock_load_docs, mock_read_urls, mock_path):
        mock_faiss_instance = MagicMock()
        mock_faiss.from_documents.return_value = mock_faiss_instance
        mock_faiss_instance.save_local.return_value = None
        
        ingest_and_save_embeddings('test_file.txt')
        
        self.assertTrue(mock_read_urls.called)
        self.assertTrue(mock_load_docs.called)
        self.assertTrue(mock_embeddings.called)
        self.assertTrue(mock_faiss_instance.save_local.called)
        self.assertTrue(mock_logging.info.called)
        self.assertFalse(mock_logging.error.called)

if __name__ == '__main__':
    unittest.main()
