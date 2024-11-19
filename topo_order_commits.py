'''

The following is how I used strace to verify that my implementation did not use other commands.

strace -f -e trace=execve python topo_order_commits.py

When ran inside a git repository, the output is just the commit branch prints.
When ran outside a git repository, the output is the only system call to stderr saying that
"Not inside a Git repository"

Thus, no other commands were used in my program.

strace is used to trace/track system calls.
-f allows us to follow the trace of any possible subprocesses that is called during the main process.
-e trace=execve tells strace whether or not another program was executed.
Having the file at the end tells us which file to run strace on and follow

'''

import os
import sys
import zlib

class CommitNode:
    def __init__(self, commit_hash):
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

def find_git_directory():
    curr_directory = os.getcwd() #get out current working directory
    
    while True: #keep going until we encounter a break
        if os.path.isdir(os.path.join(curr_directory, ".git")): #currentdirectory/.git
            curr_directory = os.path.join(curr_directory, ".git")
            break;
        if curr_directory == "/": 
            break;
        
        curr_directory = os.path.dirname(curr_directory) #update the current directory to become the parent 
    
    if curr_directory[-5:] != "/.git": #start from the last 5th character to the end to see if path contains /.git 
        sys.stderr.write("Not inside a Git repository")
        exit(1)
    
    return curr_directory

def object_files(git_repo_path,commit_hash):

    file_name = os.path.join(git_repo_path, "objects", commit_hash[:2], commit_hash[2:])
    
    with open (file_name, 'rb') as file:
        file_data = file.read()
    
    decompress_content = zlib.decompress(file_data)
    content_object = decompress_content.decode('utf-8')

    return content_object

def find_parent(content_object):  #return the parent commit 
    parent_commit = []

    content_object_lines = content_object.split("\n")

    for lines in content_object_lines:
        if lines[:6] == "parent":
            words = lines.split()
            parent_commit.append(words[1].rstrip("\n"))
    
    return parent_commit

def topo_order_commits(): 
    git_repo_path = find_git_directory() #gets our git repo (last dir is /.git)
    root_commits = [] #root commits HASHES go here
    graph = dict() #will contain all our commit nodes for all branches
    branch_to_commit = dict() # see which branches point to this commit

    #get a list of the local branch names in refs
    
    path_to_heads = os.path.join(git_repo_path, "refs/heads") #branches (last dir is /heads)

    queue = []  #FIFO, will store directories under heads
    queue.append("") 

    while queue:
        sub_dir = queue.pop(0)
        path_to_branch = os.path.join(path_to_heads, sub_dir)

        for file in os.listdir(path_to_branch): #find sub-directories 
            path_to_sub = os.path.join(path_to_branch, file)  

            if os.path.isdir(path_to_sub): #checks to see if we reached a directory 
                queue.append(file + "/")
                continue #skip to next iteration if a directory cause our branch heads are files

            curr_file = open(path_to_sub)
            commit_hash = curr_file.read().rstrip("\n") #read the commit hash within the refs file
            curr_file.close()

            root_commits.append(commit_hash) 
            commit_node = CommitNode(commit_hash)
            graph[commit_hash] = commit_node #commit node object associated with that commit hash in our graph

            #use to help with printing later
            if commit_hash not in branch_to_commit.keys():  # if not in our branch_to_commit, add because it has a branch point to this commit based on it being under refs folder
                branch_to_commit[commit_hash] = [os.path.join(sub_dir,file)]
            else:
                branch_to_commit[commit_hash].append(os.path.join(sub_dir,file))

    
    #discover relationships using DFS

    stack = root_commits[:] #create a copy of roots_commits for stack 

    while stack:
        c_hash = stack.pop()
        c_obj_content = object_files(git_repo_path,c_hash) 
        p_hash = find_parent(c_obj_content)

        for parent in p_hash:

            if parent not in graph:
                node = CommitNode(parent)
                graph[parent] = node     #key is the parent, node is the commit node /data associated with that key

            #creating relationships
            if graph[c_hash] not in graph[parent].children:
               graph[parent].children.add(graph[c_hash]) #add child node to the parent node's child set
               graph[c_hash].parents.add(graph[parent])     #add parent node to the child node's parent set
               stack.append(parent)
                

    #topological ordering 
    
    degree = dict() #will hold where the nodes are pointing to 
    no_indegree = [] #will hold degrees that have 0 indegrees 
    topo_order = [] #will hold out topological ordering

    for commit_hash, node in graph.items(): #.items() returns a dictionary view object and provides the key-value pairs in our dictionary into something that is iterable
        degree[commit_hash] = len(node.children)  #key: commit_hash, value: number of incoming degrees
    
    for commit_hash, deg in degree.items():
        if deg == 0:    #if no children, add to the no_indegree array already
            no_indegree.append(commit_hash)
    
    while no_indegree:
        curr_indegree = no_indegree.pop(0)
        topo_order.append(curr_indegree)

        #if we remove a child, one less node being pointed to

        parent_object_content = object_files(git_repo_path, curr_indegree)
        parent_node = find_parent(parent_object_content)
        
        for p_hash in parent_node: #children is a set so we can do this
            degree[p_hash] -= 1  #reduce indegree for their child
            if  degree[p_hash] == 0:
                no_indegree.append(p_hash)

    #print formatting 
    order = topo_order[:]
    stick_start = False

    for i in range(len(order)):
        # parent_node = graph[order[i]].parents # get the parents node
        # parents = [] #for the parent commit hashes

        # for par in parent_node:
        #     parents.append(par.commit_hash) #append parrent hashes to parent lists
        
        #sticky start --> previous line was a new line
        if stick_start:
            stick_start = False
            print("=", end="")
            child_nodes = graph[order[i]].children
            children = []
            for child in child_nodes:
                children.append(child.commit_hash)
            print(*children)
            # print(" ".join(children), end="") #join allows us to join elements in a iterable together with a separator, such as a space, between each element in the iterable
        
        
        #  print regularly 
        print(order[i], end="")
       
        #  if branch needed print branch names

        if order[i] in branch_to_commit:
            branch_names = branch_to_commit[order[i]]
            branch_names.sort()
            print(" ", end="")
            # print(" ".join(branch_names), end="") #ensures printing on the same line
        print() #end of line 

        #reached the end --> helps make sure stay in bounds
        if i == len(order) - 1:
            break

        #check if sticky end is needed --> parent not the next commit

        parent_object_content = object_files(git_repo_path, curr_indegree)
        parent_node = find_parent(parent_object_content)

        if order[i+1] not in parent_node:
            stick_start = True
            print(*parent_node, end="")
            # print(" ".join(parents), end="=")
            print() #print empty line
         

if __name__ == "__main__":
    topo_order_commits()

'''
Notes:

find_parent Logic: 
read contents line by line
    find the parents line 
    only take the commit of parents line and return this 

perform depth first search to establish the parent-child relationships

    topological sort is the similar to DFS
    we want to process all the children of every node, before processing the parents
   that is the child of the node should always come before actual node itself

topological sort with Kahn's Algorithm
    remove nodes without dependencies (indegrees), and add them to our topological ordering
    while nodes w/o dependencies are removed, new nodes without dependencies should appear 
    keep removing nodes w/o dependies from graoh until all nodes are processed
    if 2 or more nodes do not have dependencies, choose either or --> ordering doesn't matter so long as no dependencies are created

    can use a queue to keep track of nodes with no indegrees
     pop off the node and add it to topological ordering
     once popped off fix the number of indegrees
     add any new nodes with to queue if they become 0
     repeat til queue is empty

'''
