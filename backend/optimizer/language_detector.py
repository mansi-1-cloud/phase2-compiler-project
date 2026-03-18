"""
Simple Language Detector
"""

def detect_language(code):
    """Detect if code is C, C++ or Java"""
    
    code_lower = code.lower()
    
    # Check for Java FIRST
    if 'public class' in code_lower or 'system.out' in code_lower or 'import java' in code_lower:
        return 'java'
    
    # Check for C++
    if 'cout' in code_lower or 'cin' in code_lower or 'using namespace' in code_lower or 'std::' in code:
        return 'cpp'
    
    # Check for C (check stdio.h specifically)
    if '#include <stdio.h>' in code or 'printf(' in code or 'scanf(' in code:
        return 'c'
    
    # If nothing matched, return what user selected
    return 'c'