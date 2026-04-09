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
    
    # If nothing matched, return 'unknown'
    return 'unknown'


def validate_language(code, selected_language):
    """
    Validate if the code matches the selected language.
    Returns: {'valid': bool, 'detected': str, 'message': str}
    """
    
    detected = detect_language(code)
    
    # Map language names to their variations
    lang_map = {
        'c': ['c'],
        'cpp': ['cpp', 'c++'],
        'java': ['java']
    }
    
    selected_lang_normalized = selected_language.lower().replace('c++', 'cpp')
    
    # If user selected "Auto-detect", always valid
    if selected_lang_normalized in ['auto', 'auto-detect', 'autodetect']:
        if detected == 'unknown':
            return {
                'valid': False,
                'detected': detected,
                'message': 'Unable to detect language. Please ensure code contains language-specific keywords.'
            }
        return {
            'valid': True,
            'detected': detected,
            'message': f'Language auto-detected as {detected.upper()}'
        }
    
    # Check if detected language matches selected language
    if detected != 'unknown':
        if detected == selected_lang_normalized or detected == selected_language.lower():
            return {
                'valid': True,
                'detected': detected,
                'message': f'Language validated: {detected.upper()}'
            }
        else:
            return {
                'valid': False,
                'detected': detected,
                'message': f'LANGUAGE MISMATCH! You selected {selected_language.upper()} but the code appears to be {detected.upper()}. Please paste the correct language code.'
            }
    else:
        return {
            'valid': False,
            'detected': detected,
            'message': f'Cannot verify if code is {selected_language.upper()}. Please ensure code contains language-specific keywords (e.g., printf for C, cout for C++, System.out for Java).'
        }
