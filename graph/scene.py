from manim import *

class TreeGraph(Scene):
    def construct(self):
        nodes = [1, 2, 3, 4, 5]
        labels = ["A", "B", "C", "D", "E"]         
        edges = [
            (1, 2),
            (1, 3),
            (3, 4), 
            (3, 5)  
        ]
              
        tree_graph = Graph(
            nodes,
            edges,
            layout="tree", 
            layout_config={"root_vertex": 1},
            vertex_config={
                1: {"fill_color": RED},
                2: {"fill_color": BLUE},
                3: {"fill_color": BLUE},
                4: {"fill_color": BLUE},
                5: {"fill_color": BLUE}
            },
            edge_config={  
                (1, 2): {"stroke_color": WHITE},
                (1, 3): {"stroke_color": WHITE},
                (2, 4): {"stroke_color": WHITE},
                (2, 5): {"stroke_color": WHITE},
            }
        )
        node_labels = [
            Text(label, font_size=24).move_to(tree_graph.vertices[node].get_center())
            for node, label in zip(nodes, labels)
        ]

        for label in node_labels:
            self.add(label)
        self.play(Create(tree_graph))
        self.wait(2) 

class TreeGraphEulerTour(Scene):
    def construct(self):
        nodes = [1, 2, 3, 4, 5]
        labels = ["A", "B", "C", "D", "E"]         

        edges = [
            (1, 2),
            (1, 3), 
            (3, 4), 
            (3, 5)  
        ]
        node_radius = 0.2
        tree_graph = Graph(
            nodes,
            edges,
            layout="tree",  
            layout_config={"root_vertex": 1},
            vertex_config={
                1: {"fill_color": RED, "radius": node_radius},  
                2: {"fill_color": BLUE, "radius": node_radius},
                3: {"fill_color": BLUE, "radius": node_radius},
                4: {"fill_color": BLUE, "radius": node_radius},
                5: {"fill_color": BLUE, "radius": node_radius}
            },
            edge_config={    
                (1, 2): {"stroke_color": WHITE},
                (1, 3): {"stroke_color": WHITE},
                (3, 4): {"stroke_color": WHITE},
                (3, 5): {"stroke_color": WHITE},
            }
        )
        self.play(Create(tree_graph))

        node_labels = [
            Text(label, font_size=24).move_to(tree_graph.vertices[node].get_center())
            for node, label in zip(nodes, labels)
        ]

        for label in node_labels:
            self.add(label)
            
        glow_node = Dot(color=YELLOW).scale(1.5)  # 
        glow_node.move_to(tree_graph.vertices[1].get_center())  
        
        self.add(glow_node)  
        counters = {node: Text(str(0)).move_to(tree_graph.vertices[node].get_center()) for node in nodes}
        #for counter in counters.values():
            #self.add(counter)

        #self.play(Create(tree_graph))
        # euler_tour_steps = [
        #     (1, 2), (2, 1),
        #     (1, 3), (3, 4), (4, 3),
        #     (3, 5), (5, 3), (3, 1)  
        # ]
        euler_tour_steps = [
            (1, 3), (3, 5), (5, 3),
            (3, 4), (4, 3), (3, 1),
            (1, 2), (2, 1),

        ]
        visit_counts = {node: 0 for node in nodes}

        euler_dots = []
        new_tour_nodes = []
        new_tour_edges = []
        previous_node = False
        it = 0

        euler_dot = Dot(color=GREEN).move_to(tree_graph.vertices[1].get_center() + UP * 0.5)
        euler_dots.append(euler_dot)
        self.play(FadeIn(euler_dot, scale=0.5), run_time=0.5)
        new_tour_nodes.append(0)

        for step in euler_tour_steps:
            start, end = step
            edge = tree_graph.edges.get((start, end)) or tree_graph.edges.get((end, start))
            
            self.play(
                AnimationGroup(
                    Indicate(edge, color=YELLOW, scale_factor=1.2), 
                    glow_node.animate.move_to(tree_graph.vertices[end].get_center()),  
                    lag_ratio=0  
                ),
                run_time=0.4
            )

            visit_counts[end] += 1

            new_counter_text = Text(str(visit_counts[end])).move_to(tree_graph.vertices[end].get_center())
            
            new_node_name = f"{it}" 
            it +=1
            new_tour_nodes.append(new_node_name)

            start_pos = tree_graph.vertices[start].get_center()
            end_pos = tree_graph.vertices[end].get_center()
            
            dotColor = GREEN
            if start_pos[1] > end_pos[1]: 
                spawn_offset = UP * 0.5
                dotColor = GREEN
            elif start_pos[0] < end_pos[0]:  
                spawn_offset = LEFT * 0.5
                dotColor = BLUE
            elif start_pos[0] > end_pos[0]:  
                spawn_offset = RIGHT * 0.5
                dotColor = RED
            else:
                spawn_offset = DOWN * 0.5 

            euler_dot = Dot(color=dotColor).move_to(tree_graph.vertices[end].get_center() + spawn_offset)
            euler_dots.append(euler_dot)
            self.play(FadeIn(euler_dot, scale=0.5), run_time=0.5)

        
        #all_elements = VGroup(tree_graph, glow_node, *counters.values(), *euler_dots)
        all_elements = VGroup(tree_graph, glow_node, *euler_dots)

        self.play(
            all_elements.animate.scale(0.5).to_corner(DL), 
            run_time=1
        )


        noderange = len(new_tour_nodes)//2

        for i in range(noderange):
            new_tour_edges.append((new_tour_nodes[i],new_tour_nodes[i*2+1]))
            if len(new_tour_nodes) > i*2 + 2:
                new_tour_edges.append((new_tour_nodes[i],new_tour_nodes[i*2+2]))

        print(new_tour_edges)
        print(new_tour_nodes)
        print(noderange)
        print(len(new_tour_nodes))
        print(len(new_tour_edges))
        new_tree_graph = Graph(
            new_tour_nodes,
            new_tour_edges,
            layout="tree",
            layout_config={"root_vertex": new_tour_nodes[0]},  
            vertex_config={node: {"fill_color": GREEN} for node in new_tour_nodes},  
            edge_config={edge: {"stroke_color": WHITE} for edge in new_tour_edges}
        )

        self.add(new_tree_graph)
        for edge in new_tree_graph.edges.values():
            edge.set_opacity(0) 
        new_tree_graph.set_opacity(0)

        for i, dot in enumerate(euler_dots):
            new_pos = new_tree_graph.vertices[new_tour_nodes[i]].get_center()
            self.play(dot.animate.move_to(new_pos), run_time=1)

            if i > 0: 
                print(1000)
                print(new_tour_edges)
                new_tree_graph.edges[new_tour_edges[i-1]].set_opacity(100)
                #a = new_tree_graph.edges[(12312)]
                #a.set_opacity(100)
                #new_edge = new_tree_graph.edges[(new_tour_nodes[i - 1], new_tour_nodes[i])]
                #self.play(Create(new_edge), run_time=0.5)


        self.wait(2)

#manim -pql scene.py TreeGraphEulerTour

