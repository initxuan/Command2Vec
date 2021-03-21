import argparse
import numpy as np
from gensim.models import Word2Vec
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Run Command2Vec")

    parser.add_argument("--edgeslist", nargs="?", default="edges", 
                        help="Input edges-list folder path")
    
    parser.add_argument("--nodeslist", nargs="?", default="nodes",
                        help="Input nodes-list folder path")

    parser.add_argument("--output", nargs="?", default="emb",
                        help="Save output-results folder path")

    parser.add_argument("--theta", type=int, default=7,
                        help="The theta used to select command sequence. Default is 7.")
    
    parser.add_argument("--dimension", type=int, default=128,
                        help="Number of dimension, Default is 128.")

    parser.add_argument("--window-size", type=int, default=4,
                        help="Context size for optimization. Default is 4.")

    parser.add_argument('--iter', default=10000, type=int,
                      help='Number of epochs in SGD. Default is 10000.')

    parser.add_argument("--workers", type=int, default=8,
                        help="Number of parallel workers. Default is 8.")
                        
    return parser.parse_args()


def learn_embedding(cmd2word_list, args):
    savepath = os.path.join(args.output, "cmdembedding.emb")
    model = Word2Vec(cmd2word_list, size=args.dimension, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter, alpha=0.001)
    # for windows
    model.save_word2vec_format(savepath)
    # for mac
    # model.wv.save_word2vec_format(savepath)


def main(args):
    edgesdir_path = args.edgeslist
    nodesdir_path = args.nodeslist
    theta = args.theta
    cmdarray_path = os.path.join(args.output, "cmdarray.txt")

    cmd2word_list = list()
    cmddegree_list = list()

    file_list = os.listdir(edgesdir_path)
    file_list.sort(key=lambda x: int(x[:-4]))
    for item in file_list:
        # Save the number corresponding to the command
        num2cmd_map = dict()
        with open(os.path.join(nodesdir_path, item), "r") as f:
            for line in f:
                l = line[:-1].split(" ")
                num2cmd_map[int(l[0])] = l[2]

        # Compute the out-degree of each node
        out_degree = list()
        with open(os.path.join(edgesdir_path, item), "r") as f:
            for line in f:
                found = False
                l = line.split(" ")
                tmp = int(l[0])
                for i in out_degree:
                    if i[0] == tmp:
                        i[1] += 1
                        found = True
                        break
                if not found:
                    out_degree.append([tmp, 1])

        # Sort the node according to the out-degree and command-index(Descending order)
        out_degree = sorted(out_degree, key=lambda x: (x[1], -x[0]), reverse=True)

        # Filter command according to the theta
        cmd_list = list()
        cmd_degree = list()
        count = 0
        index = 0
        while count < theta and index < len(out_degree):
            # Ignore command "Redo" and "Delete"
            if num2cmd_map[out_degree[index][0]] == "Redo" or num2cmd_map[out_degree[index][0]] == "Delete":
                index += 1
            else:
                cmd_list.append(num2cmd_map[out_degree[index][0]])
                cmd_degree.append(out_degree[index][1])
                count += 1
                index += 1

        cmd2word_list.append(cmd_list)
        cmddegree_list.append(cmd_degree)

    # Save the command sequence of each command-graph
    with open(cmdarray_path, "w") as f:
        for item in cmd2word_list:
            length = len(item)
            if length == 0:
                continue
            for i in range(length - 1):
                f.write(item[i])
                f.write(" ")
            f.write(item[length - 1])
            f.write("\n")

    # Using Word2Vec to get embedding vector of each command
    learn_embedding(cmd2word_list, args)
    
    # Get the embedding vector of each command
    cmd2vec = dict()
    with open(os.path.join(args.output, "cmdembedding.emb"), "r") as f:
        for line in f:
            line = line[:-1].split(" ")
            if len(line) == 2:
                continue
            else:
                cmd2vec[line[0]] = [float(i) for i in line[1:]]
    
    # Compute the weight according to the out-degree
    weight = list()
    for vec in cmddegree_list:
        s = sum(vec)
        weight.append([float(i) / s for i in vec])

    graph_vec = list()
    # Compute the weighted average of command sequence
    for index, item in enumerate(cmd2word_list):
        w = weight[index]
        tmp = np.zeros(args.dimension)
        l = len(item)
        if l == 0:
            continue
        for index_, cmd in enumerate(item):
            tmp = [j + k * w[index_] for j, k in zip(tmp, cmd2vec[cmd])]
        
        graph_vec.append(tmp)
    
    # Save the embedding vector of each command graph
    with open(os.path.join(args.output, "graphvec.txt"), "w") as f:
        for item in graph_vec:
            length = len(item)
            if length == 0:
                continue
            for i in range(length - 1):
                f.write(str(item[i]))
                f.write(" ")
            f.write(str(item[length - 1]))
            f.write("\n")
            

if __name__ == "__main__":
    args = parse_args()
    main(args)