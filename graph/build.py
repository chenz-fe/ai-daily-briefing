"""
构建 LangGraph：Search → Filter → Summary → Save（线性四节点）。
"""
from langgraph.graph import StateGraph, START, END

from .state import BriefingState
from .nodes import search_node, filter_node, summary_node, save_node


def check_filtered_items(state: dict) -> str:
    """根据过滤结果决定是否继续生成简报"""
    # LangGraph conditional edges need to return the *exact* node name or END
    if not state.get("filtered_items"):
        return END
    return "summary"


def build_graph():
    """构建并编译图，返回 compiled graph。"""
    graph = StateGraph(BriefingState)

    graph.add_node("search", search_node)
    graph.add_node("filter", filter_node)
    graph.add_node("summary", summary_node)
    graph.add_node("save", save_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "filter")
    graph.add_conditional_edges("filter", check_filtered_items)
    graph.add_edge("summary", "save")
    graph.add_edge("save", END)

    return graph.compile()
