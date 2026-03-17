"""
构建 LangGraph：Search → Filter → Summary → Save（线性四节点）。
"""
from langgraph.graph import StateGraph, START, END

from .state import BriefingState
from .nodes import search_node, filter_node, summary_node, save_node


def build_graph():
    """构建并编译图，返回 compiled graph。"""
    graph = StateGraph(BriefingState)

    graph.add_node("search", search_node)
    graph.add_node("filter", filter_node)
    graph.add_node("summary", summary_node)
    graph.add_node("save", save_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "filter")
    graph.add_edge("filter", "summary")
    graph.add_edge("summary", "save")
    graph.add_edge("save", END)

    return graph.compile()
