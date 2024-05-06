from tree_sitter import Language, Parser
import tree_sitter_python as tspython


def load_language():
    PY_LANGUAGE = Language(tspython.language(), "python")
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    return parser


# Load the language library (Adjust the path to your compiled language library)
def get_tree(source_code):
    parser = load_language()

    tree = parser.parse(bytes(source_code, "utf8"))
    return tree


