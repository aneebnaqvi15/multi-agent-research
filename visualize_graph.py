from graph.research_graph import build_graph

def save_graph_image():
    graph = build_graph()
    
    png_data = graph.get_graph().draw_mermaid_png()
    
    with open("architecture.png", "wb") as f:
        f.write(png_data)
    
    print("✅ Architecture diagram saved as architecture.png")

if __name__ == "__main__":
    save_graph_image()