from manim import *
import random
from ETTreap import Treap

class TreeGraphEulerTour(Scene):
    def construct(self):
        nodes = [1, 2, 3, 4, 5]
        labels = ["A", "B", "C", "D", "E"]         
        edges = [(1, 2),(1, 3), (3, 4), (3, 5)]
        edges2 = [(1, 2),(1, 5), (5, 3), (3, 4)]

        color_map = {
            "A": RED,
            "B": BLUE,
            "C": GREEN,
            "D": ORANGE,
            "E": PURPLE,
        }
        color_map2 = {}
        node_radius = 0.2
        tree_graph = Graph(
            nodes,
            edges,
            layout="tree",  
            layout_config={"root_vertex": 1},
            vertex_config={node: {"fill_color": color_map.get(labels[node-1]), "radius": node_radius} for node in nodes},
            edge_config={edge: {"stroke_color": WHITE} for edge in edges}
        )
        self.play(Create(tree_graph))
        self.wait(2)
        tree_graph2 = Graph(
            nodes,
            edges2,
            layout="tree",  
            layout_config={"root_vertex": 1},
            vertex_config={node: {"fill_color": color_map.get(labels[node-1]), "radius": node_radius} for node in nodes},
            edge_config={edge: {"stroke_color": WHITE} for edge in edges}
        )
        node_labels = [
            Text(label, font_size=24).move_to(tree_graph.vertices[node].get_center())
            for node, label in zip(nodes, labels)
        ]

        for label in node_labels:
            self.add(label)
            
        glow_node = Dot(color=YELLOW).scale(1.5)  
        glow_node.move_to(tree_graph.vertices[1].get_center())  
        
        self.add(glow_node)  
        
  
        tour_text_group = VGroup().to_edge(DOWN) 

        colored_letter = Text("A", font_size=24, color=color_map["A"])
        tour_text_group.add(colored_letter) 
        tour_text_group.to_edge(DOWN)
        self.add(tour_text_group)
        euler_tour_steps = [
            (1, 3), (3, 5), (5, 3),
            (3, 4), (4, 3), (3, 1),
            (1, 2), (2, 1),

        ]
        visit_counts = {node: 0 for node in nodes}

        euler_dots = []
        new_tour_nodes = []
        it = 0

        euler_dot = Dot(color=RED).move_to(tree_graph.vertices[1].get_center() + UP * 0.5)
        euler_dots.append(euler_dot)
        self.play(FadeIn(euler_dot, scale=0.5), run_time=0.6)
        new_tour_nodes.append(0)
        positions_to_move = []
        positions_to_move.append(1)
        euler_tour_nodes = []
        euler_tour_nodesT = []
        euler_tour_nodes.append(it)
        euler_tour_nodesT.append(1)
        color_map2[it] = color_map[labels[0]]

        for step in euler_tour_steps:
            start, end = step
            edge = tree_graph.edges.get((start, end)) or tree_graph.edges.get((end, start))        

            self.play(
                AnimationGroup(
                    Indicate(edge, color=YELLOW, scale_factor=1.2), 
                    glow_node.animate.move_to(tree_graph.vertices[end].get_center()),  
                    lag_ratio=0  
                ),
                run_time=1.3
            )
            label = labels[end - 1]
            label_color = color_map.get(label, WHITE)

            colored_letter = Text(label, font_size=24, color=label_color)
            tour_text_group.add(colored_letter)     
            self.play(Transform(tour_text_group, VGroup(*tour_text_group).arrange(RIGHT).to_edge(DOWN)), run_time=0.1)

            visit_counts[end] += 1
            
            new_node_name = f"{it}" 
            it +=1
            new_tour_nodes.append(new_node_name)
            euler_tour_nodes.append(it)
            euler_tour_nodesT.append(end)
            color_map2[it] = color_map[labels[end-1]]


            start_pos = tree_graph.vertices[start].get_center()
            end_pos = tree_graph.vertices[end].get_center()

            if start_pos[1] > end_pos[1]: 
                spawn_offset = UP * 0.5
            elif start_pos[0] < end_pos[0]:  
                spawn_offset = LEFT * 0.5
            elif start_pos[0] > end_pos[0]:  
                spawn_offset = RIGHT * 0.5
            else:
                spawn_offset = DOWN * 0.5 

            euler_dot = Dot(color=label_color).move_to(tree_graph.vertices[end].get_center() + spawn_offset)
            euler_dots.append(euler_dot)
            self.play(FadeIn(euler_dot, scale=0.5), run_time=1)

            positions_to_move.append(end)
        all_elements = VGroup(tree_graph, glow_node, *euler_dots, *node_labels)

        self.play(
            all_elements.animate.scale(0.5).to_corner(DL), 
            run_time=1.5
        )
        self.remove(glow_node)
        self.remove(*node_labels)

        first_euler_dot = euler_dots[0]
        self.play(
            first_euler_dot.animate.move_to(ORIGIN), 
            run_time=1.5
        )


        tree_nodes = [0]
        tree_edges = []

        root_tree_graph = Graph(
            tree_nodes,
            tree_edges,
            layout="tree",
            layout_config={"root_vertex": new_tour_nodes[0]},
            vertex_config={new_tour_nodes[0]: {"fill_color": RED, "radius": 0.2}}
        )

        self.play(ReplacementTransform(first_euler_dot,root_tree_graph))

        t = Treap()
        prio = random.randint(0,1000)
        t.insert(0,prio,euler_tour_nodesT[0])

        def generate_layout( tree, node, x=0, y=0, dx=1):
            layout = {node: [x, y, 0]}
            children = tree.get(node, [None, None]) 
            
            if children[0] is not None:  
                layout.update(generate_layout(tree, children[0], x - dx, y - 1, dx / 2))
            if children[1] is not None:  
                layout.update(generate_layout(tree, children[1], x + dx, y - 1, dx / 2))
            
            return layout
        
        def build_tree_from_edges_with_direction( edges):
            tree = {}
            for (parent, child), is_left in edges:
                if parent not in tree:
                    tree[parent] = [None, None]  
                if is_left:
                    tree[parent][0] = child 
                else:
                    tree[parent][1] = child 
            return tree

        def createManimTree(t,nodes,dirEdges):
            tree_structure = build_tree_from_edges_with_direction(dirEdges)
            root = t.getRoot().key
            layout = generate_layout(tree_structure,root)

            current_tree_edges = []
            for edge, is_left in dirEdges:
                current_tree_edges.append(edge)
            n = len(nodes)
            gradient_colors = [interpolate_color(RED, GREEN, alpha=i / (n - 1)) for i in range(n)]

            vertex_config = {
                node: {"fill_color": gradient_colors[idx], "radius": 0.2}
                for idx, node in enumerate(nodes)
            }
            treenodes = t.printTreeArr()
            vertex_config = {node: {"fill_color": color_map.get(labels[node_val-1]), "radius": 0.2 } for node, node_val in treenodes}

            tree_graph = Graph(
                vertices=nodes,
                edges=current_tree_edges,
                layout=layout,
                layout_scale=2,
                vertex_config=vertex_config,
            )

            return tree_graph

        for i in range(1, len(new_tour_nodes)):
            next_dot = euler_dots[i]

            self.play(next_dot.animate.move_to(ORIGIN), run_time=1.5)

            prio = random.randint(0,1000)
            t.insert(i,prio,euler_tour_nodesT[i]) # 

            current_tree_nodes = euler_tour_nodes[0:i+1]
            directed_edges = t.getEdgesDi()

            current_tree_edges = []
            for edge, is_left in directed_edges:
                current_tree_edges.append(edge)

            tree_structure = build_tree_from_edges_with_direction(directed_edges)

            root = t.getRoot().key
            layout = generate_layout(tree_structure, root)

            n = len(current_tree_nodes)


            updated_tree_graph = Graph(
                vertices=current_tree_nodes,
                edges=current_tree_edges,
                layout=layout,
                layout_scale=2,
                vertex_config={node: {"fill_color": color_map2.get(node), "radius": node_radius} for node in current_tree_nodes}
            ).shift(UP)

            root_euler = VGroup(*root_tree_graph,*next_dot)
            self.play(ReplacementTransform(root_euler, updated_tree_graph), run_time=1)

            root_tree_graph = updated_tree_graph
            self.wait(0.5)

        framebox_query_in_tree = SurroundingRectangle(tree_graph[2], buff=.1)
        framebox_query = SurroundingRectangle(updated_tree_graph[7], buff=.1)
        framebox_query2 = SurroundingRectangle(updated_tree_graph[8], buff=.1)
        self.play(Create(framebox_query_in_tree))
        self.play(Create(framebox_query))
        self.wait(7)
        query_edge = (7,8)
        if (7,8) not in updated_tree_graph.edges:
            query_edge = (8,7)
        if query_edge in updated_tree_graph.edges: #could do this better to find a longer path if the simple one edge path isn't there
            edge_query = updated_tree_graph.edges[query_edge]
            self.play(edge_query.animate.set_color(YELLOW))
            self.play(Create(framebox_query2))
            self.remove(framebox_query)

            self.wait(12)
            self.remove(framebox_query2,framebox_query_in_tree)
            edge_query.set_color(WHITE)
        else:

            self.remove(framebox_query2,framebox_query_in_tree)

        lt, rt = t.eulerSplit(0.5,5.5)
        euler_tour_nodes_copy = euler_tour_nodes.copy()
        euler_tour_nodes_copy.insert(0,-1)
        print(t.getEdges(),euler_tour_nodes_copy,"0qiwejqpwkeoiqwepoiqe")
        left_tree_graph = createManimTree(lt,euler_tour_nodes[6:],lt.getEdgesDi()).shift(LEFT * 2)
        right_tree_graph = createManimTree(rt,euler_tour_nodes[1:6],rt.getEdgesDi()).shift(RIGHT * 2)
        self.play(ReplacementTransform(root_tree_graph,updated_tree_graph))

        root_tree_graph = updated_tree_graph


        tour_text_group_left = VGroup(*tour_text_group[:1], *tour_text_group[-2:])   
        tour_text_group_right = VGroup(*tour_text_group[1:-3])
        edge_to_hide = tree_graph.edges[(1, 3)]  # Access the edge object
        self.play(edge_to_hide.animate.set_color(YELLOW))
        self.wait(15)
        framebox = SurroundingRectangle(tour_text_group[1:6], buff = .1)
        framebox2 = SurroundingRectangle(tour_text_group[6],color=RED, buff = .1)
        self.play(Create(framebox))
        self.wait(9)
        self.play(Create(framebox2))
        self.wait(11)
        self.remove(framebox)
        self.remove(framebox2)
        split_group = VGroup(left_tree_graph, right_tree_graph)

        self.play(
            edge_to_hide.animate.set_stroke(opacity=0),
            ReplacementTransform(root_tree_graph.copy(),split_group[0]),
            ReplacementTransform(root_tree_graph,split_group[1]),
            ReplacementTransform(tour_text_group.copy(), VGroup(*tour_text_group_left).arrange(RIGHT).to_edge(DOWN).shift(LEFT*2)),
            ReplacementTransform(tour_text_group.copy(), VGroup(*tour_text_group_right).arrange(RIGHT).to_edge(DOWN).shift(RIGHT*2)),
        )

        self.remove(tour_text_group)
        self.wait(10)
        rt.reRoot(2)
        up_right_tree_graph = createManimTree(rt,euler_tour_nodes[1:6],rt.getEdgesDi()).shift(RIGHT * 2)

        up_tour_text_group_right = VGroup(*tour_text_group_right[1:])
        colored_letter = Text("E", font_size=24, color=color_map["E"])
        up_tour_text_group_right.add(colored_letter)   
        edge_to_hide2 = tree_graph2.edges[(1, 5)] 
        edge_to_hide2.set_stroke(opacity=0)

        framebox_reroot = SurroundingRectangle(tree_graph[5], buff = .1)

        self.play(Create(framebox_reroot))

        self.wait(30)
        self.remove(framebox_reroot)

        self.play(FadeOut(tour_text_group_right[0]))
        self.remove(tour_text_group_right[0])
        self.play(
            ReplacementTransform(right_tree_graph,up_right_tree_graph),
            Transform(tour_text_group_right, up_tour_text_group_right.arrange(RIGHT).to_edge(DOWN).shift(RIGHT*2)),
            ReplacementTransform(tree_graph,tree_graph2.scale(0.6).to_corner(DL).shift(RIGHT*0.5))
            )

        merged_tree = rt.eulerLink(lt,rt,1.5)


        merged_tree_graph = createManimTree(merged_tree,euler_tour_nodes,merged_tree.getEdgesDi())
        merged_tour_text_graph = VGroup(*tour_text_group[:1],*up_tour_text_group_right[4:],*up_tour_text_group_right[:4], *tour_text_group[-3:])

        self.wait(2)

        edge_to_hide2.set_color(YELLOW)
        self.play(
                  edge_to_hide2.animate.set_stroke(opacity=100),
                  )

        group = VGroup(left_tree_graph, up_right_tree_graph)
        text_group = VGroup(tour_text_group_left,up_tour_text_group_right)
        self.wait(12)
        self.remove(tour_text_group_right)
        self.play(
            ReplacementTransform(group[0],merged_tree_graph.shift(UP*0.5)),
            ReplacementTransform(group[1],merged_tree_graph.shift(UP*0.5)),
            Transform(text_group, VGroup(*merged_tour_text_graph).arrange(RIGHT).to_edge(DOWN)),
            edge_to_hide2.animate.set_color(WHITE),
        )
        print(merged_tour_text_graph)
        for a in merged_tour_text_graph:
            print("a",a)

        self.wait(14)
    

#manim -pql scene.py TreeGraphEulerTour