import os
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack
from diagrams.generic.device import Tablet

# Injection dynamique du chemin Graphviz pour l'exécution
# Ce chemin correspond à l'installation standard via winget
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

graph_attr = {
    "fontsize": "20",
    "bgcolor": "white"
}

with Diagram("Foliotype Protocol Data Flow", show=False, filename="schema_flux_fp", graph_attr=graph_attr):
    
    source_files = Storage("assets/input\n(RAW Data)")

    with Cluster("Cognition Engine (HERMES V4)"):
        logic = Rack("hermes_core.py")
        validation = Rack("dry_run.py")
        
        logic >> Edge(label="audit", color="blue") >> validation

    with Cluster("Output Mastered"):
        master_files = Storage("assets/output/mastered\n(FP Standard)")
        distribution = Tablet("Client Access")

    # Flux principal
    source_files >> logic >> master_files >> distribution