"""
Code Optimization Detector
Detects: Constant Folding, Dead Code, Unused Variables, 
Loop Invariant, Unnecessary Variables, Inefficient Loop Patterns
"""
import re


def optimize(code):
    """
    Analyze code for optimization opportunities
    Returns: (code, stats_dict)
    """
    stats = {
        'constant_folding': 0,
        'dead_code': 0,
        'unused_variables': 0,
        'loop_invariant': 0,
        'unnecessary_variables': 0,
        'inefficient_loops': 0
    }
    
    lines = code.split('\n')
    
    print("\n" + "="*70)
    print("OPTIMIZATION ANALYSIS")
    print("="*70)
    
    # ===== 1. CONSTANT FOLDING =====
    print("\n[1] CONSTANT FOLDING - Fold constant expressions (e.g., 2+3→5)")
    const_fold_count = 0
    for i, line in enumerate(lines, 1):
        if re.search(r'=\s*(\d+)\s*([+\-*/])\s*(\d+)\s*[;:]', line):
            const_fold_count += 1
            match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', line)
            if match:
                print(f"  → Line {i}: '{match.group(0)}' can be folded")
    
    stats['constant_folding'] = const_fold_count
    print(f"  Total: {const_fold_count} opportunities")
    
    # ===== 2. DEAD CODE =====
    print("\n[2] DEAD CODE - Remove unreachable code after return/break/continue")
    dead_code_count = 0
    for i, line in enumerate(lines, 1):
        if re.search(r'\b(return|break|continue)\s*[;{]', line):
            for j in range(i, len(lines)):
                next_line = lines[j].strip()
                if next_line and next_line != '}' and not next_line.startswith('//'):
                    dead_code_count += 1
                    print(f"  → Line {j+1}: Dead code (unreachable)")
                    break
                if next_line == '}':
                    break
    
    stats['dead_code'] = dead_code_count
    print(f"  Total: {dead_code_count} dead code blocks")
    
    # ===== 3. UNUSED VARIABLES =====
    print("\n[3] UNUSED VARIABLES - Remove variables that are declared but never used")
    var_declarations = {}
    for i, line in enumerate(lines):
        match = re.search(r'\b(int|float|double|char|long|unsigned|bool|void|auto|const)\s+(\w+)\s*[=;,]', line)
        if match:
            var_name = match.group(2)
            if var_name not in var_declarations:
                var_declarations[var_name] = i + 1
    
    used_vars = set()
    for i, line in enumerate(lines):
        for var_name in var_declarations.keys():
            if var_name in line:
                # Check if it's not just the declaration
                if not re.search(rf'^\s*(int|float|double|char|long|unsigned|bool|void|auto|const)\s+{var_name}', line):
                    used_vars.add(var_name)
    
    unused_count = 0
    for var_name in var_declarations:
        if var_name not in used_vars:
            unused_count += 1
            print(f"  → Line {var_declarations[var_name]}: Variable '{var_name}' never used")
    
    stats['unused_variables'] = unused_count
    print(f"  Total: {unused_count} unused variables")
    
    # ===== 4. LOOP INVARIANT CODE MOTION =====
    print("\n[4] LOOP INVARIANT - Move constant calculations outside loops")
    loop_inv_count = 0
    in_loop = False
    
    for i, line in enumerate(lines, 1):
        if re.search(r'\b(for|while)\s*\(', line):
            in_loop = True
            loop_start = i
            
            # Check next 20 lines inside loop for constant calculations
            for j in range(i, min(i+20, len(lines))):
                if re.search(r'=\s*\d+\s*[+\-*/]\s*\d+', lines[j]):
                    loop_inv_count += 1
                    match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', lines[j])
                    if match:
                        print(f"  → Line {j+1}: Constant '{match.group(0)}' inside loop (can move outside)")
                
                if lines[j].strip() == '}':
                    in_loop = False
                    break
    
    stats['loop_invariant'] = loop_inv_count
    print(f"  Total: {loop_inv_count} loop invariant opportunities")
    
    # ===== 5. UNNECESSARY VARIABLES =====
    print("\n[5] UNNECESSARY VARIABLES - Remove intermediate variables")
    unnecessary_vars = 0
    
    for i, line in enumerate(lines, 1):
        # Pattern: int x = y; (then x is only used once)
        match = re.search(r'\b(int|float|double|bool)\s+(\w+)\s*=\s*(\w+)\s*;', line)
        if match:
            var = match.group(2)
            source = match.group(3)
            
            # Count how many times this variable is used after declaration
            var_usage = 0
            for j in range(i, len(lines)):
                if var in lines[j]:
                    var_usage += 1
            
            # If variable is only used 1 time after declaration (in return/print), it's unnecessary
            if var_usage <= 2:
                unnecessary_vars += 1
                print(f"  → Line {i}: Unnecessary variable '{var}' (could use '{source}' directly)")
    
    stats['unnecessary_variables'] = unnecessary_vars
    print(f"  Total: {unnecessary_vars} unnecessary variables")
    
    # ===== 6. INEFFICIENT LOOP PATTERNS =====
    print("\n[6] INEFFICIENT LOOP PATTERNS - Optimize simple increment loops")
    inefficient_loop = 0
    
    for i, line in enumerate(lines, 1):
        # Pattern: for(i=0; i<n; i++) with simple increment
        if re.search(r'for\s*\(\s*(\w+)\s*=\s*0\s*;\s*\1\s*<\s*(\w+)\s*;\s*\1\+\+\s*\)', line):
            var = re.search(r'for\s*\(\s*(\w+)\s*=', line).group(1)
            limit = re.search(r'\1\s*<\s*(\w+)', line).group(1)
            inefficient_loop += 1
            print(f"  → Line {i}: Simple increment loop 'for(i=0; i<{limit}; i++)' can be optimized")
    
    stats['inefficient_loops'] = inefficient_loop
    print(f"  Total: {inefficient_loop} inefficient loop patterns")
    
    # Summary
    print("\n" + "="*70)
    total = sum(stats.values())
    print(f"TOTAL OPTIMIZATION OPPORTUNITIES: {total}")
    print("="*70 + "\n")
    
    return code, stats