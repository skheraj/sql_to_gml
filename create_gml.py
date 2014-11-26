#!usr/bin/env python

import csv, dbm, os

GML_FILE_CONTENT = ""
EDGE_SET = set([])
NODE_MAP = {}

def start_gml_file():
    global GML_FILE_CONTENT
    
    GML_FILE_CONTENT = GML_FILE_CONTENT + "graph [\n\n\tdirected 0\n\n\tlabel \"asf data\"\n\n"
    
    return True

def write_nodes():
    global NODE_MAP, GML_FILE_CONTENT
    
    node_file = open("node_table.csv", 'r')
    id = 1

    for line in node_file:
        new_node = "\tnode [\n\t\tid " + str(id) + "\n\t\tlabel \"" + line.rstrip('\n') + "\"\n\t]\n"
        GML_FILE_CONTENT = GML_FILE_CONTENT + new_node
        NODE_MAP[line.rstrip('\n')] = str(id)
        id = id + 1

    node_file.close()
    
    return True

def write_edges():
    global EDGE_SET, GML_FILE_CONTENT
    
    db = dbm.open('nodes', 'c')
    
    edge_file = open("edge_table.csv", 'r', newline='')
    csv_reader = csv.reader(edge_file)
    
    first_row = next(csv_reader)
    new_edge = "\tedge [\n\t\tsource " + NODE_MAP[first_row[0]] + "\n\t\ttarget " + NODE_MAP[first_row[1]] + "\n"
    EDGE_SET.add(frozenset([first_row[0].rstrip(), first_row[1].rstrip()]))
    prev = first_row[1]
    issues = [first_row[2]]
    weight = 1
    
    for row in csv_reader:
        if not prev:
            new_set = frozenset([row[0].rstrip(), row[1].rstrip()])
            if not new_set in EDGE_SET:
                new_edge = "\tedge [\n\t\tsource " + NODE_MAP[row[0].rstrip()] + "\n\t\ttarget " + NODE_MAP[row[1].rstrip()] + "\n"
                EDGE_SET.add(new_set)
                prev = row[1]
                weight = 1
        elif prev != row[1]:
            new_edge = new_edge + "\t\tweight " + str(weight) + "\n"
            new_edge = new_edge + "\t\tlabel \"" + ','.join(issues) + "\"\n\t]\n"
            GML_FILE_CONTENT = GML_FILE_CONTENT + new_edge
            prev = None
            
            new_set = frozenset([row[0].rstrip(), row[1].rstrip()])
            if not new_set in EDGE_SET:
                new_edge = "\tedge [\n\t\tsource " + NODE_MAP[row[0].rstrip()] + "\n\t\ttarget " + NODE_MAP[row[1].rstrip()] + "\n"
                EDGE_SET.add(new_set)
                prev = row[1]
                weight = 1
                issues = [row[2]]
        else:
            weight = weight + 1
            issues.append(row[2])
    
    edge_file.close()
    os.remove("nodes.db")
    
    return True

def end_gml_file():
    global GML_FILE_CONTENT
    
    GML_FILE_CONTENT = GML_FILE_CONTENT + "]"
    gml_file = open("asf_data.gml", 'w')
    gml_file.write(GML_FILE_CONTENT)
    gml_file.close()
    
    return True

def main():
    start_gml_file()
    
    write_nodes()
    
    write_edges()
    
    end_gml_file()

if __name__ == '__main__':
    main()