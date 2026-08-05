"""
Safe AST-Based Formula Parser and Evaluator for NeuroLearn Research Suite.
Evaluates user-defined mathematical expressions safely without using raw eval/exec.
"""

import ast
import operator
from typing import Dict, Any


# Supported operators
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


class FormulaEvaluator:
    """Safe Evaluator for mathematical formulas such as '(beta + gamma) / (theta + alpha)'."""

    @staticmethod
    def evaluate(expression_str: str, variables: Dict[str, float]) -> float:
        """Parse and evaluate math expression against provided variable dict."""
        try:
            node = ast.parse(expression_str, mode="eval")
            # Normalize dictionary keys to lowercase
            var_clean = {k.lower(): float(v) for k, v in variables.items()}
            return float(FormulaEvaluator._eval_node(node.body, var_clean))
        except (KeyError, TypeError, ZeroDivisionError) as e:
            raise e
        except Exception as e:
            raise ValueError(f"Invalid attention formula expression '{expression_str}': {e}") from e

    @staticmethod
    def _eval_node(node: ast.AST, variables: Dict[str, float]) -> float:
        if hasattr(ast, "Constant") and isinstance(node, ast.Constant):
            return float(node.value)
        elif hasattr(ast, "Num") and isinstance(node, ast.Num):
            return float(node.n)
        elif isinstance(node, ast.Name):
            var_name = node.id.lower()
            if var_name in variables:
                return float(variables[var_name])
            raise KeyError(f"Undefined variable in formula: '{var_name}'")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise TypeError(f"Unsupported operator in formula: {op_type}")
            left = FormulaEvaluator._eval_node(node.left, variables)
            right = FormulaEvaluator._eval_node(node.right, variables)

            # Guard against division by zero
            if op_type is ast.Div and right == 0:
                return 0.0

            return float(SAFE_OPERATORS[op_type](left, right))
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise TypeError(f"Unsupported unary operator: {op_type}")
            operand = FormulaEvaluator._eval_node(node.operand, variables)
            return float(SAFE_OPERATORS[op_type](operand))

        raise TypeError(f"Unsupported AST node element: {type(node)}")
