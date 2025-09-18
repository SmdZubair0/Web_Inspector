from lxml import etree
from typing import List
from langgraph.graph import StateGraph, START, END

from src.main.schemas import LocatorState
from src.main.validators import ValidateLocator
from src.main.readers import DOMReader, HTMLReader
from src.main.models.llms import ElementNamingModel
from src.main.generator.base import LocatorStrategy
from src.main.models.vector_stores import FaissVectorStore
from src.main.searchers import SearchHelper, SearchWithEmbeddings, Searcher
from src.main.generator.helpers import CssSelectorHelper, IdHelper, XPathHelper
from src.main.generator.locators import IdLocator, CssSelectorLocator,XPathLocator
from src.main.models.embeddings.HuggingFaceEmbeddings import HuggingFaceAPIEmbeddings

def make_validator_node(validator : ValidateLocator):
    def validator_node(state : LocatorState) -> LocatorState:
        """
            Take state object
            - validate the locators
            - assign filtered locators to state
            - return state object
        """
        validator.validate_all_locators(state['locators'])
        
        state['locators'] = validator.get_locators

        return state
    return validator_node

def make_generate_locator_node(strategies : List[LocatorStrategy]):
    def generate_locator(state : LocatorState) -> LocatorState:
        """
            Take state object
            - find locators based on each of the given strategy
            - store locators in state
            - return state object
        """
        locators = []
        for strategy in strategies:
            response = strategy.create(state['element'], state['element_dom'])
            if len(response['locators']) > 0:
                locators.append(response)
        
        state['locators'] = locators
        return state
    return generate_locator

def make_parse_element_node(reader: DOMReader):
    def parse_element(state : LocatorState) -> LocatorState:
        """
            Take state object and ReadDOM object
            - convert and store raw_element to element
            - convert and store raw_element_dom to element dom
            - return state
        """

        state['element'] = reader.readFromString(state['raw_element'])
        state['element_dom'] = reader.readFromString(state['raw_element_dom'])

        return state
    
    return parse_element

def make_partial_dom_node(reader : DOMReader):
    def get_partial_dom(state : LocatorState):
        """
            Takes state object
            - finds target element and its nearby elements
            - make the hollow copies of elements and store in dom
            - return state object
        """

        dom = reader.readFromFile(state['dom'])
        target = dom.xpath("//*")[state['element_idx']]

        current = etree.Element(target.tag, **target.attrib)

        state['element'] = current

        current.text = target.text

        for i in range(2):
            original = target
            parent = target.getparent()
            if parent is None:
                break

            prev = original.getprevious()
            nxt = original.getnext()

            # Clone parent without children
            partial_parent = etree.Element(parent.tag, **parent.attrib)

            # Add prev sibling
            if prev is not None:
                partial_parent.append(etree.Element(prev.tag, **prev.attrib))

            # Add current
            partial_parent.append(current)

            # Add next sibling
            if nxt is not None:
                partial_parent.append(etree.Element(nxt.tag, **nxt.attrib))

            # Update loop vars
            target = parent
            current = partial_parent

        state['element_dom'] = current

        return state
    
    return get_partial_dom

def make_query_node(searcher : Searcher):
    def query(state : LocatorState) -> LocatorState:
        """
            Take state object
            - take query from user
            - query is the name of element for which locator should be found
            - return state
        """
        
        query = input("Enter the element name : ")
        element_idx = searcher.search(query)

        state['element_idx'] = element_idx

        return state
    
    return query

def start_router(state : LocatorState) -> str:
    if 'raw_element' in state and state['raw_element'] is not None:
        return 'parse'
    return 'start'

def make_start_node(helper : SearchHelper, reader : DOMReader, searcher : Searcher):
    def start_node(state : LocatorState) -> None:
        """
            Take state object
            - read dom and filter the important elements from it
            - setup the searcher
        """
        dom = reader.readFromFile(state['dom'])

        el = helper.filter_elements(dict(enumerate(dom.xpath("//*"))))

        searcher.setup(el)

    return start_node

def make_graph(
        reader : DOMReader,
        search_helper : SearchHelper,
        searcher : Searcher,
        strategies : List[LocatorStrategy],
        validator : ValidateLocator
    ):
    graph = StateGraph(LocatorState)

    graph.add_node('start', make_start_node(search_helper, reader, searcher))
    graph.add_node('query', make_query_node(searcher))
    graph.add_node('get partial dom', make_partial_dom_node(reader))
    graph.add_node('parse', make_parse_element_node(reader))
    graph.add_node('generate', make_generate_locator_node(strategies))
    graph.add_node('validator', make_validator_node(validator))

    graph.add_conditional_edges(START, start_router)
    graph.add_edge('start', 'query')
    graph.add_edge('query', 'get partial dom')
    graph.add_edge('get partial dom', 'generate')
    graph.add_edge('parse', 'generate')
    graph.add_edge('generate', 'validator')
    graph.add_edge('validator', END)

    workflow = graph.compile()
    return workflow    

def main(state : LocatorState):
    reader = HTMLReader()
    search_helper = SearchHelper()
    strategies = [IdLocator(IdHelper()), CssSelectorLocator(CssSelectorHelper()), XPathLocator(XPathHelper())]
    searcher = SearchWithEmbeddings(HuggingFaceAPIEmbeddings(), ElementNamingModel(), FaissVectorStore(), search_helper)
    validator = ValidateLocator(reader.readFromFile(state['dom']))

    app = make_graph(reader, search_helper, searcher, strategies, validator)
    
    res = app.invoke(state)

    return res['locators']

if __name__ == "__main__":
    
    state = {'dom' : "C:\\Users\\zubair.shaik\\Desktop\\xpathfinder\\src\\resources\\dom2.xml", 
             'raw_element_dom' : '<div class="entry-content-wrap"><header class="entry-header post-title title-align-left title-tablet-align-inherit title-mobile-align-inherit"><h1 class="entry-title">Automation Testing</h1><div class="entry-meta entry-meta-divider-customicon"></div></header><div class="entry-content single-content"></div></div>', 
             'raw_element' : '<h1 class="entry-title">Automation Testing</h1>'}
    
    print(main(state))