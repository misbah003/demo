"""
Advanced Named Entity Recognition (NER) for Document Processing
Uses spaCy and Transformers for context-aware entity extraction
"""

import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re
from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict

class AdvancedNERExtractor:
    """
    Advanced NER system using multiple models:
    1. spaCy for general NER
    2. BERT-based FinBERT for financial entities
    3. Custom regex patterns as fallback
    """
    
    def __init__(self):
        print("🚀 Initializing Advanced NER System...")
        
        # Load spaCy model (English)
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded")
        except:
            print("⚠️ Downloading spaCy model...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Load FinBERT for financial NER
        try:
            print("🔄 Loading FinBERT for financial entity extraction...")
            self.fin_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            self.fin_model = AutoModelForTokenClassification.from_pretrained("ProsusAI/finbert")
            self.fin_ner = pipeline("ner", model=self.fin_model, tokenizer=self.fin_tokenizer, aggregation_strategy="simple")
            print("✅ FinBERT loaded")
        except Exception as e:
            print(f"⚠️ FinBERT not available: {e}")
            self.fin_ner = None
        
        # Enhanced regex patterns
        self.patterns = {
            'GST': [
                r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}[A-Z]{1}\d{1}\b',
                r'GSTIN\s*:?\s*(\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}[A-Z]{1}\d{1})',
                r'GST\s*(?:Number|No|#)?\s*:?\s*([\dA-Z]{15})',
            ],
            'PAN': [
                r'\b[A-Z]{5}\d{4}[A-Z]{1}\b',
                r'PAN\s*:?\s*([A-Z]{5}\d{4}[A-Z]{1})',
            ],
            'MONEY': [
                r'₹\s*[\d,]+(?:\.\d{1,2})?',
                r'INR\s*[\d,]+(?:\.\d{1,2})?',
                r'Rs\.?\s*[\d,]+(?:\.\d{1,2})?',
                r'\b[\d,]{1,}[\d]+\.\d{2}\b',
                r'\b[\d]{1,3}(?:,\d{3})*(?:\.\d{2})?\b',
            ],
            'DATE': [
                r'\b\d{1,2}[-\/]\d{1,2}[-\/]\d{4}\b',
                r'\b\d{4}[-\/]\d{1,2}[-\/]\d{1,2}\b',
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
            ],
            'INVOICE_NUMBER': [
                r'(?:Invoice|Bill|Receipt)\s*(?:No|Number|#)?\s*:?\s*([A-Z0-9\-\/]+)',
                r'\b(?:INV|BILL|REC)[-\/]?\d{4,}\b',
            ],
            'EMAIL': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            ],
            'PHONE': [
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\b\d{10}\b',
            ],
        }
        
        print("✅ Advanced NER System Ready!")
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract entities using multiple methods:
        1. spaCy NER
        2. FinBERT (if available)
        3. Regex patterns
        
        Returns structured entity dictionary with confidence scores
        """
        entities = defaultdict(list)
        
        # Method 1: spaCy NER
        spacy_entities = self._extract_with_spacy(text)
        for ent_type, ent_list in spacy_entities.items():
            entities[ent_type].extend(ent_list)
        
        # Method 2: FinBERT for financial entities
        if self.fin_ner:
            fin_entities = self._extract_with_finbert(text)
            for ent_type, ent_list in fin_entities.items():
                entities[ent_type].extend(ent_list)
        
        # Method 3: Regex patterns (high precision for specific formats)
        regex_entities = self._extract_with_regex(text)
        for ent_type, ent_list in regex_entities.items():
            entities[ent_type].extend(ent_list)
        
        # Deduplicate and rank by confidence
        entities = self._deduplicate_entities(entities)
        
        return dict(entities)
    
    def _extract_with_spacy(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities using spaCy"""
        entities = defaultdict(list)
        doc = self.nlp(text)
        
        for ent in doc.ents:
            entity_info = {
                'text': ent.text,
                'label': ent.label_,
                'confidence': 0.8,  # spaCy doesn't provide confidence, use default
                'start': ent.start_char,
                'end': ent.end_char,
                'method': 'spacy'
            }
            
            # Map spaCy labels to our categories
            if ent.label_ == 'MONEY':
                entities['MONEY'].append(entity_info)
            elif ent.label_ == 'DATE':
                entities['DATE'].append(entity_info)
            elif ent.label_ == 'ORG':
                entities['COMPANY'].append(entity_info)
            elif ent.label_ == 'PERSON':
                entities['PERSON'].append(entity_info)
            elif ent.label_ == 'GPE':
                entities['LOCATION'].append(entity_info)
        
        return entities
    
    def _extract_with_finbert(self, text: str) -> Dict[str, List[Dict]]:
        """Extract financial entities using FinBERT"""
        entities = defaultdict(list)
        
        try:
            # Split text into chunks (FinBERT has token limit)
            max_length = 512
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            
            for chunk in chunks:
                results = self.fin_ner(chunk)
                for result in results:
                    entity_info = {
                        'text': result['word'],
                        'label': result['entity_group'],
                        'confidence': result['score'],
                        'start': result['start'],
                        'end': result['end'],
                        'method': 'finbert'
                    }
                    entities[result['entity_group']].append(entity_info)
        except Exception as e:
            print(f"⚠️ FinBERT extraction error: {e}")
        
        return entities
    
    def _extract_with_regex(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities using regex patterns"""
        entities = defaultdict(list)
        
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_info = {
                        'text': match.group(0),
                        'label': entity_type,
                        'confidence': 0.95,  # Regex patterns are high precision
                        'start': match.start(),
                        'end': match.end(),
                        'method': 'regex'
                    }
                    entities[entity_type].append(entity_info)
        
        return entities
    
    def _deduplicate_entities(self, entities: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """
        Remove duplicate entities and keep highest confidence ones
        """
        deduplicated = defaultdict(list)
        
        for entity_type, entity_list in entities.items():
            # Group by text (case-insensitive)
            grouped = defaultdict(list)
            for entity in entity_list:
                key = entity['text'].lower().strip()
                grouped[key].append(entity)
            
            # Keep highest confidence for each unique text
            for key, group in grouped.items():
                best_entity = max(group, key=lambda x: x['confidence'])
                deduplicated[entity_type].append(best_entity)
        
        return deduplicated
    
    def extract_semantic_context(self, text: str, entity: Dict) -> Dict:
        """
        Extract semantic context around an entity using spaCy
        """
        doc = self.nlp(text)
        
        # Find the entity in the doc
        entity_start = entity['start']
        entity_end = entity['end']
        
        # Get surrounding sentences
        context_sentences = []
        for sent in doc.sents:
            if sent.start_char <= entity_start <= sent.end_char or \
               sent.start_char <= entity_end <= sent.end_char:
                context_sentences.append(sent.text)
        
        # Get dependency relations
        entity_tokens = [token for token in doc if entity_start <= token.idx < entity_end]
        dependencies = []
        for token in entity_tokens:
            dependencies.append({
                'text': token.text,
                'pos': token.pos_,
                'dep': token.dep_,
                'head': token.head.text
            })
        
        return {
            'context_sentences': context_sentences,
            'dependencies': dependencies,
            'entity': entity
        }
    
    def analyze_document_structure(self, text: str) -> Dict:
        """
        Analyze document structure and extract metadata
        """
        doc = self.nlp(text)
        
        analysis = {
            'num_sentences': len(list(doc.sents)),
            'num_tokens': len(doc),
            'num_entities': len(doc.ents),
            'language': doc.lang_,
            'has_financial_terms': self._detect_financial_terms(text),
            'document_type': self._classify_document_type(text),
            'key_phrases': self._extract_key_phrases(doc),
        }
        
        return analysis
    
    def _detect_financial_terms(self, text: str) -> bool:
        """Detect if document contains financial terms"""
        financial_keywords = [
            'invoice', 'bill', 'receipt', 'payment', 'tax', 'vat', 'gst',
            'amount', 'total', 'subtotal', 'refund', 'credit', 'debit'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in financial_keywords)
    
    def _classify_document_type(self, text: str) -> str:
        """Classify document type based on content"""
        text_lower = text.lower()
        
        if 'vat' in text_lower or 'gst' in text_lower:
            if 'invoice' in text_lower or 'bill' in text_lower:
                return 'VAT Invoice'
            elif 'return' in text_lower:
                return 'VAT Return'
            else:
                return 'VAT Document'
        elif 'invoice' in text_lower:
            return 'Tax Invoice'
        elif 'receipt' in text_lower:
            return 'Purchase Receipt'
        elif 'statement' in text_lower:
            return 'Financial Statement'
        else:
            return 'Document'
    
    def _extract_key_phrases(self, doc) -> List[str]:
        """Extract key noun phrases"""
        key_phrases = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) >= 2:  # Multi-word phrases
                key_phrases.append(chunk.text)
        return key_phrases[:10]  # Top 10


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("ADVANCED NER EXTRACTION SYSTEM TEST")
    print("=" * 60)
    
    # Initialize extractor
    extractor = AdvancedNERExtractor()
    
    # Test document
    test_text = """
    TAX INVOICE
    
    Invoice No: INV-2024-001
    Date: 15/10/2024
    
    From:
    ABC Trading Pvt Ltd
    GSTIN: 29ABCDE1234F1Z5
    PAN: ABCDE1234F
    
    To:
    XYZ Imports Ltd
    Email: contact@xyzimports.com
    Phone: +91-9876543210
    
    Items:
    Product A: ₹50,000.00
    Product B: ₹30,000.00
    Subtotal: ₹80,000.00
    GST (18%): ₹14,400.00
    Total Amount: ₹94,400.00
    
    Payment Terms: Net 30 days
    """
    
    print("\n📄 Test Document:")
    print(test_text)
    
    print("\n🔍 Extracting Entities...")
    entities = extractor.extract_entities(test_text)
    
    print("\n✅ Extracted Entities:")
    for entity_type, entity_list in entities.items():
        print(f"\n{entity_type}:")
        for entity in entity_list:
            print(f"  - {entity['text']} (confidence: {entity['confidence']:.2f}, method: {entity['method']})")
    
    print("\n📊 Document Analysis:")
    analysis = extractor.analyze_document_structure(test_text)
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("=" * 60)