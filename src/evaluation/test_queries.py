import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.retrieval.chat_chain import ChatChain

def run_tests():
    print("🧪 Starting Evaluation Tests...\n")
    
    try:
        bot = ChatChain()
    except Exception as e:
        print(f"❌ Failed to init bot: {e}")
        return

    test_cases = [
        {
            "name": "Context Extraction (Refund)",
            "questions": ["How do I get a refund?"],
            "expected_keywords": ["refund", "policy", "days"] # Adjust based on actual text
        },
        {
            "name": "Follow-up Handling",
            "questions": ["What is the refund policy?", "What is the timeline for that?"],
            "expected_keywords": ["days", "process", "time"] 
        },
        {
            "name": "Hallucination Check (President)",
            "questions": ["Who is the President of the USA?"],
            "expected_exact": "I don’t have enough information in the provided documents to answer that."
        }
    ]

    for test in test_cases:
        print(f"running test: {test['name']}...")
        history = []
        last_response = ""
        
        for q in test['questions']:
            print(f"  Q: {q}")
            last_response = bot.ask(q, history)
            print(f"  A: {last_response}")
            history.append((q, last_response))
        
        # Validation
        passed = False
        if "expected_exact" in test:
            if test["expected_exact"] in last_response:
                passed = True
            else:
                print(f"  ❌ Expected exact match: '{test['expected_exact']}'")
        elif "expected_keywords" in test:
            if any(k.lower() in last_response.lower() for k in test["expected_keywords"]):
                passed = True
            else:
                print(f"  ❌ Expected keywords: {test['expected_keywords']}")
        
        if passed:
            print("  ✅ PASS\n")
        else:
            print("  ❌ FAIL\n")

if __name__ == "__main__":
    run_tests()
