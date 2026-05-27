import ast
from difflib import SequenceMatcher

def get_ast_structure(code):
    """
    Parses Python code and returns a string representation of its structural elements (AST nodes).
    Ignores variable names, logic values, etc., focusing only on structure.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None 

    structure = []
    
    for node in ast.walk(tree):
        
        node_type = type(node).__name__
        structure.append(node_type)
        
    return " ".join(structure)

def calculate_ast_similarity(code1, code2):
    """
    Calculates similarity based on Abstract Syntax Tree structure.
    Returns a score between 0 and 100.
    """
    struct1 = get_ast_structure(code1)
    struct2 = get_ast_structure(code2)
    
    
    if struct1 is None or struct2 is None:
        return -1.0
        
    score = SequenceMatcher(None, struct1, struct2).ratio()
    return score * 100
