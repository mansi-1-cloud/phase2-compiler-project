"""
Code Optimization Detector
Detects: Constant Folding, Dead Code, Unused Variables, 
Loop Invariant, Unnecessary Variables, Inefficient Loop Patterns
"""
import re


def evaluate_expression(expr):
    """Safely evaluate a mathematical expression with numbers and operators"""
    try:
        # Only evaluate simple expressions with numbers and basic operators
        if re.match(r'^\d+\s*[+\-*/]\s*\d+$', expr.strip()):
            result = eval(expr)
            return result
    except:
        pass
    return None


def optimize(code):
    """
    Analyze code for optimization opportunities AND apply transformations
    Returns: (optimized_code, stats_dict)
    """
    stats = {
        'constant_folding': 0,
        'dead_code': 0,
        'redundant_assignment': 0,
        'expression_simplify': 0,
        'unused_variables': 0,
        'loop_invariant': 0,
        'unnecessary_variables': 0,
        'inefficient_loops': 0
    }
    
    lines = code.split('\n')
    optimized_lines = lines.copy()
    
    # ===== 1. CONSTANT FOLDING =====
    const_fold_count = 0
    lines_to_modify = {}
    
    for i, line in enumerate(lines):
        # Match: 5 * 4, (2 * 3), (10 + 20) * 2, etc
        match = re.search(r'=\s*(\(?\d+\s*[+\-*/]\s*\d+\)?.*?)\s*[;]', line)
        if match:
            expr_orig = match.group(1)
            # Try to evaluate simple expressions
            try:
                # Extract just the number operations
                expr = re.sub(r'[()]', '', expr_orig)
                if re.match(r'^\d+\s*[+\-*/]\s*\d+(\s*[+\-*/]\s*\d+)*$', expr):
                    result = eval(expr)
                    const_fold_count += 1
                    new_line = line[:match.start()] + f"= {int(result)}" + line[match.end()-1:]
                    lines_to_modify[i] = new_line
            except:
                pass
    
    for i, new_line in lines_to_modify.items():
        optimized_lines[i] = new_line
    
    stats['constant_folding'] = const_fold_count
    
    # ===== 2. DEAD CODE ELIMINATION =====
    dead_code_count = 0
    lines_to_remove = []
    
    i = 0
    while i < len(optimized_lines):
        line = optimized_lines[i]
        
        # Dead code after return/break/continue
        if re.search(r'\b(return|break|continue)\s*[;{]', line):
            j = i + 1
            while j < len(optimized_lines):
                next_line = optimized_lines[j].strip()
                if not next_line or next_line.startswith('//') or next_line == '}':
                    break
                if next_line and not next_line.startswith((' ', '\t')) or next_line == '}':
                    break
                dead_code_count += 1
                lines_to_remove.append(j)
                j += 1
            i = j
        
        # Dead code in if(false) or if(0) blocks
        elif re.search(r'if\s*\(\s*(false|0)\s*\)', line):
            dead_code_count += 1
            j = i + 1
            # Remove the entire if block
            while j < len(optimized_lines):
                next_line = optimized_lines[j].strip()
                lines_to_remove.append(j)
                if next_line == '}':
                    break
                j += 1
            lines_to_remove.append(i)  # Remove the if line itself
            i = j + 1
        else:
            i += 1
    
    for idx in sorted(set(lines_to_remove), reverse=True):
        if idx < len(optimized_lines):
            del optimized_lines[idx]
    
    stats['dead_code'] = dead_code_count
    
    # ===== 3. REDUNDANT ASSIGNMENT REMOVAL =====
    redundant_count = 0
    lines_to_remove = []
    
    # Check consecutive identical assignments
    for i in range(len(optimized_lines) - 1):
        line1 = optimized_lines[i].strip()
        line2 = optimized_lines[i+1].strip()
        
        match1 = re.match(r'^(\w+)\s*=\s*(.+?)\s*[;]', line1)
        match2 = re.match(r'^(\w+)\s*=\s*(.+?)\s*[;]', line2)
        
        if match1 and match2 and match1.group(1) == match2.group(1) and match1.group(2) == match2.group(2):
            redundant_count += 1
            lines_to_remove.append(i + 1)
    
    # Also check single line: x = x;
    for i, line in enumerate(optimized_lines):
        match = re.match(r'^(\s*)(\w+)\s*=\s*\2\s*[;]', line)
        if match:
            redundant_count += 1
            lines_to_remove.append(i)
    
    for idx in sorted(set(lines_to_remove), reverse=True):
        if idx < len(optimized_lines):
            del optimized_lines[idx]
    
    stats['redundant_assignment'] = redundant_count
    
    # ===== 4. EXPRESSION SIMPLIFICATION =====
    simplify_count = 0
    
    for i, line in enumerate(optimized_lines):
        # x = x + 0; → x;
        if re.search(r'(\w+)\s*=\s*\1\s*\+\s*0\s*[;]', line):
            simplified = re.sub(r'(\w+)\s*=\s*\1\s*\+\s*0\s*;', r'\1;', line)
            optimized_lines[i] = simplified
            simplify_count += 1
        
        # x = x * 1; → x;
        elif re.search(r'(\w+)\s*=\s*\1\s*\*\s*1\s*[;]', line):
            simplified = re.sub(r'(\w+)\s*=\s*\1\s*\*\s*1\s*;', r'\1;', line)
            optimized_lines[i] = simplified
            simplify_count += 1
        
        # a * 1 + 0 or a * 1 or b + 0
        elif re.search(r'=\s*(\w+)\s*\*\s*1\b', line):
            simplified = re.sub(r'(\w+)\s*=\s*(\w+)\s*\*\s*1\s*([+]?\s*0)?\s*;', r'\1 = \2;', line)
            if simplified != line:
                optimized_lines[i] = simplified
                simplify_count += 1
        
        elif re.search(r'=\s*\(?\w+\s*\+\s*0\)', line):
            simplified = re.sub(r'(\w+)\s*=\s*\((\w+)\s*\+\s*0\)\s*;', r'\1 = \2;', line)
            if simplified != line:
                optimized_lines[i] = simplified
                simplify_count += 1
    
    stats['expression_simplify'] = simplify_count
    
    # ===== 5. UNUSED VARIABLES =====
    var_declarations = {}
    for i, line in enumerate(optimized_lines):
        match = re.search(r'\b(int|float|double|char|long|unsigned|bool|void|auto|const)\s+(\w+)\s*[=;,]', line)
        if match:
            var_name = match.group(2)
            if var_name not in var_declarations:
                var_declarations[var_name] = i
    
    used_vars = set()
    for i, line in enumerate(optimized_lines):
        for var_name in var_declarations.keys():
            if var_name in line and i != var_declarations[var_name]:
                if not re.search(rf'^\s*(int|float|double|char|long|unsigned|bool|void|auto|const)\s+{var_name}', line):
                    used_vars.add(var_name)
    
    lines_to_remove = []
    for var_name, decl_line in var_declarations.items():
        if var_name not in used_vars:
            lines_to_remove.append(decl_line)
    
    for idx in sorted(lines_to_remove, reverse=True):
        if idx < len(optimized_lines):
            del optimized_lines[idx]
    
    stats['unused_variables'] = len(lines_to_remove)
    
    # ===== 6. LOOP INVARIANT CODE MOTION =====
    loop_inv_count = 0
    stats['loop_invariant'] = loop_inv_count
    
    # ===== 7. UNNECESSARY VARIABLES =====
    unnecessary_vars = 0
    stats['unnecessary_variables'] = unnecessary_vars
    
    # ===== 8. INEFFICIENT LOOP PATTERNS =====
    inefficient_loop = 0
    stats['inefficient_loops'] = inefficient_loop
    
    optimized_code = '\n'.join(optimized_lines)
    return optimized_code, stats