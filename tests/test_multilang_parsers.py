"""
Test script for Multi-Language Parsers
Tests the newly implemented language parsers with sample queries
"""

from myriad.core.multilang.multilang_parser import get_multilang_parser
from myriad.core.multilang.language_detector import Language

def test_language_parsers():
    """Test all language parsers with sample queries"""
    
    parser = get_multilang_parser()
    
    # Test queries in different languages
    test_queries = {
        'English': "What is the historical impact of the lightbulb on industrial development?",
        'Spanish': "¿Cuál es el impacto histórico de la bombilla en el desarrollo industrial?",
        'French': "Quel est l'impact historique de l'ampoule sur le développement industriel?",
        'German': "Was ist die historische Auswirkung der Glühbirne auf die industrielle Entwicklung?",
        'Chinese': "灯泡对工业发展的历史影响是什么?",
        'Portuguese': "Qual é o impacto histórico da lâmpada no desenvolvimento industrial?",
        'Italian': "Qual è l'impatto storico della lampadina sullo sviluppo industriale?",
        'Russian': "Каково историческое влияние лампочки на промышленное развитие?"
    }
    
    print("=" * 80)
    print("Multi-Language Parser Testing")
    print("=" * 80)
    print()
    
    for language_name, query in test_queries.items():
        print(f"\n{'='*80}")
        print(f"Testing {language_name}")
        print(f"{'='*80}")
        print(f"Query: {query}")
        print()
        
        try:
            # Parse the query
            metadata, parsed = parser.parse_query(query)
            
            # Display results
            print(f"✅ Parsing Successful!")
            print(f"Detected Language: {metadata.detected_language.value}")
            print(f"Language Confidence: {metadata.language_confidence:.2f}")
            print(f"Primary Intent: {parsed.primary_intent}")
            print(f"Concepts: {', '.join(parsed.concepts[:5]) if parsed.concepts else 'None'}")
            print(f"Complexity Score: {parsed.complexity_score:.2f}")
            print(f"Estimated Agents: {parsed.estimated_agents_needed}")
            
            # Display language-specific data
            if parsed.language_specific_data:
                print(f"\nLanguage-Specific Features:")
                for key, value in parsed.language_specific_data.items():
                    print(f"  - {key}: {value}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("Testing Complete!")
    print(f"{'='*80}")


def test_intent_recognition():
    """Test intent recognition across languages"""
    
    parser = get_multilang_parser()
    
    print(f"\n{'='*80}")
    print("Intent Recognition Testing")
    print(f"{'='*80}")
    
    # Test different intents in different languages
    intent_tests = {
        'define': {
            'en': "What is a lightbulb?",
            'es': "¿Qué es una bombilla?",
            'fr': "Qu'est-ce qu'une ampoule?",
            'de': "Was ist eine Glühbirne?",
            'zh': "什么是灯泡?"
        },
        'explain_impact': {
            'en': "What was the impact of the lightbulb?",
            'es': "¿Cuál fue el impacto de la bombilla?",
            'fr': "Quel a été l'impact de l'ampoule?",
            'de': "Was war die Auswirkung der Glühbirne?",
            'zh': "灯泡的影响是什么?"
        },
        'compare': {
            'en': "Compare lightbulbs and candles",
            'es': "Comparar bombillas y velas",
            'fr': "Comparer les ampoules et les bougies",
            'de': "Vergleichen Sie Glühbirnen und Kerzen",
            'zh': "比较灯泡和蜡烛"
        }
    }
    
    for expected_intent, queries in intent_tests.items():
        print(f"\n\nTesting Intent: {expected_intent}")
        print("-" * 80)
        
        for lang, query in queries.items():
            try:
                metadata, parsed = parser.parse_query(query)
                status = "✅" if parsed.primary_intent == expected_intent else "❌"
                print(f"{status} [{lang}] {query}")
                print(f"   Detected Intent: {parsed.primary_intent}")
            except Exception as e:
                print(f"❌ [{lang}] Error: {str(e)}")


if __name__ == "__main__":
    print("\n🌍 Multi-Language Parser Test Suite 🌍\n")
    
    # Run basic parser tests
    test_language_parsers()
    
    # Run intent recognition tests
    test_intent_recognition()
    
    print("\n✨ All tests completed! ✨\n")
