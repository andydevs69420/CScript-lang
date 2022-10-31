""" __init__.py initialize ast node

    author: andydevs69420
    github: http://github.com/andydevs69420/CScript-lang
"""

from .globalast.csAst import CSAst
from .objectast.csreferncenode import ReferenceNode

from .moduleast.csmodulenode import ModuleNode

""" Object ast group
    Represents object
"""
from .objectast.csintegernode import IntegerNode
from .objectast.csdoublenode import DoubleNode
from .objectast.csstringnode import StringNode
from .objectast.csboolnode import BoolNode
from .objectast.csnullnode import NullNode
from .objectast.csheadlessfunctionnode import HeadlessFunctionNode
from .objectast.csarraynode import ArrayNode
from .objectast.csobjectnode import ObjectNode



""" Event ast
    Analyze|Compile event suchas call, access, subscript
"""
from .eventast.csaccessnode import AccessNode
from .eventast.cssubscriptnode import SubscriptNode
from .eventast.cscallnode import CallNode
from .eventast.csallocdeallocnode import AllocDeallocNode


""" Expression ast group
    Evaluate or compiles expression
"""
from .expressionast.csternarynode import TernaryNode
from .expressionast.csunaryexprnode import UnaryExprNode
from .expressionast.csbinaryexprnode import BinaryExprNode
from .expressionast.cscompareexprnode import CompareExprNode
from .expressionast.csequalityexprnode import EqualityExprNode
from .expressionast.cslogicalexprnode import LogicalExprNode


from .assignmentast.cssimpleassignmentnode import SimpleAssignment
from .assignmentast.csaugmentedassignmentnode import AugmentedAssignment




""" Compound statement ast group
    Compiles compound statements
"""
from .compoundast.csclassnode import ClassNode
from .compoundast.csfunctionnode import FunctionNode
from .compoundast.csifstatementnode import IfStatementNode
from .compoundast.csdowhilenode import DoWhileNode
from .compoundast.cswhilenode import WhileNode
from .compoundast.csswitchnode import SwitchNode
from .compoundast.cstryexceptnode import TryExceptNode
from .compoundast.csblocknode import BlockNode


""" Simple statement at group
    Compiles simple statement
"""
from .simpleast.csimportnode import ImportNode
from .simpleast.csvarnode import VarNode
from .simpleast.csletnode import LetNode
from .simpleast.csbreaknode import BreakNode
from .simpleast.cscontinuenode import ContinueNode
from .simpleast.csthrownode import ThrowNode
from .simpleast.csassertnode import AssertNode
from .simpleast.csprintnode import PrintNode
from .simpleast.csreturnnode import ReturnNode
from .simpleast.csexprstatementnode import ExprStmntNode
