import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_text():
    """Sample research paper text for testing"""
    return """
    Abstract: This paper introduces the Transformer architecture for neural machine translation.
    The model relies entirely on attention mechanisms, dispensing with recurrence and convolutions.
    
    Introduction: Neural machine translation has made significant progress in recent years.
    However, existing models rely on complex recurrent or convolutional neural networks.
    
    Methodology: We propose a new simple network architecture, the Transformer, based solely on
    attention mechanisms. The model achieves state-of-the-art results on translation tasks.
    
    Results: Our model achieves a BLEU score of 28.4 on the WMT 2014 English-to-German translation task.
    
    Conclusion: The Transformer model demonstrates that attention mechanisms alone are sufficient
    for achieving excellent performance on sequence transduction tasks.
    """
