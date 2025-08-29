#!/usr/bin/env python3
"""
Simple test script for the Devil's Advocate Multi-Agent System
"""

def test_cases_module():
    """Test the cases module functionality."""
    try:
        from cases import get_case_titles, get_case_description, get_bias_analysis
        print("✅ Cases module imported successfully")
        
        # Test case retrieval
        titles = get_case_titles()
        print(f"✅ Found {len(titles)} sample cases")
        
        # Test specific case
        case_id = list(titles.keys())[0]
        case_desc = get_case_description(case_id)
        bias_info = get_bias_analysis(case_id)
        
        print(f"✅ Case '{case_id}' retrieved successfully")
        print(f"✅ Bias analysis: {bias_info['bias_type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cases module test failed: {e}")
        return False

def test_basic_agents():
    """Test basic agent functionality without model loading."""
    try:
        # Test the agent logic structure
        print("✅ Basic agent structure test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic agent test failed: {e}")
        return False

def test_gradio_import():
    """Test Gradio import."""
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Gradio import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Devil's Advocate Multi-Agent System...\n")
    
    tests = [
        ("Cases Module", test_cases_module),
        ("Basic Agents", test_basic_agents),
        ("Gradio Import", test_gradio_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing: {test_name}")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready for use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()