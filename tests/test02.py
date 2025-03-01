import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.html_praser import HtmlParser
from core.root_node import RootNode


with open('data/test02.html', 'r', encoding='utf-8') as file:
    html = file.read()
parser = HtmlParser(html)
parser.root.pretty_print()
root_node = RootNode(parser.root)
root_node.run_a_node(parser.root)