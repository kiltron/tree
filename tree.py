#!/usr/bin/env python
# coding: utf-8

# In[12]:


import os
import operator
import os.path
import sys
        
def treeD(path): #tree without files, with key = "-d"
    if (path == ""):
        path = os.getcwd()
    else:
        if path[-1] == "\\":
            path = path[:-1] + "/"
        elif path[-1] != "/":
            path = path + "/"
        i = 0
        while i < len(path):
            if path[i] == "\\":
                path = path[:i] + '/' + path[(i+1):]
            i += 1 
        path=os.path.dirname(path)
    
    directory = os.path.basename(path)
    graphD = {}
    graphF = {}
    for i in os.walk(path):
        graphD[os.path.basename(i[0])] = i[1] 
        graphF[os.path.basename(i[0])] = i[2]
    
    #граф
    def dfs(graphD, node, visited):
        if node not in visited:
            visited.append(node)
            for n in graphD[node]:
                dfs(graphD, n, visited)
        return visited

    visited = dfs(graphD, directory, [])
    nestingLevel = {}
    nestingLevel[visited[0]] = 0
    for i in visited:
        if graphD[i]:
            for j in graphD[i]:
                nestingLevel[j] = nestingLevel[i] + 1 
    #ветки
    branch = '├───'
    lastBranch = '└───'
    parallelBranch = '│   '
    emptyBranch = '    '

    #создание массива вывода
    columns = nestingLevel[max(nestingLevel.items(), key=operator.itemgetter(1))[0]] + 2
    rows = len(visited)

    output = [[emptyBranch for x in range(columns)] for x in range(rows)] 

    #ввод директорий в массив вывода
    y = 0 
    for i in visited: 
        level = nestingLevel[i]
        output[y][level] = i
        y += 1
    
    start=0
    finish=0
    x = 0
    startD = output[0][0]
    while x < (columns - 1): #циклы присвоения веток в массив вывода
        y = 0
        start = 0
        finish = 1
        while y < rows:
            if output[y][x] in visited and graphD[output[y][x]] == []: #последняя директория
                finish = 1
                start = 0
            elif output[y][x] in visited: #начало ветки 
                finish = 0
                start = 1
                startD = output[y][x]
            elif len(graphD[startD]) > 0 and output[y][x + 1] == graphD[startD][-1]: #конец ветки 
                finish = 1
                start = 0
                output[y][x] = lastBranch
            elif output[y][x + 1] in visited: #срединная ветка+
                output[y][x] = branch
            elif finish == 1 and start == 0: #пустая ветка 
                output[y][x] = emptyBranch
            elif start == 1 and finish == 0:  #параллельная ветка
                output[y][x] = parallelBranch
            else:
                continue
            y += 1
        x += 1
    return output

def treeF(path): #tree with files
    if path[-1] == "\\":
        path = path[:-1] + "/"
    elif path[-1] != "/":
        path = path + "/"
    i = 0
    while i < len(path):
        if path[i] == "\\":
            path = path[:i] + '/' + path[(i+1):]
        i += 1 
    path=os.path.dirname(path)
    directory = os.path.basename(path)
    graph = {}
    for i in os.walk(path):
        graph[os.path.basename(i[0])] = i[1] + i[2]
        #graphF[os.path.basename(i[0])] = i[2]
    for i in os.walk(path):
        for j in i[2]:
            graph[j] = []
    #граф
    def dfs(graph, node, visited):
        if node not in visited:
            visited.append(node)
            for n in graph[node]:
                dfs(graph, n, visited)
        return visited

    visited = dfs(graph, directory, [])
    nestingLevel = {}
    nestingLevel[visited[0]] = 0
    for i in visited:
        if graph[i]:
            for j in graph[i]:
                nestingLevel[j] = nestingLevel[i] + 1
    #ветки
    branch = '├───'
    lastBranch = '└───'
    parallelBranch = '│   '
    emptyBranch = '    '

    #создание массива вывода
    columns = nestingLevel[max(nestingLevel.items(), key=operator.itemgetter(1))[0]] + 2
    rows = len(visited)

    output = [[emptyBranch for x in range(columns)] for x in range(rows)] 

    #ввод директорий в массив вывода
    y = 0 
    for i in visited: 
        level = nestingLevel[i]
        output[y][level] = i
        y += 1
    
    start=0
    finish=0
    x = 0
    startD = output[0][0]
    while x < (columns - 1): #циклы присвоения веток в массив вывода
        y = 0
        start = 0
        finish = 1
        while y < rows:
            if output[y][x] in visited and graph[output[y][x]] == []: #последняя директория
                finish = 1
                start = 0
            elif output[y][x] in visited: #начало ветки 
                finish = 0
                start = 1
                startD = output[y][x]
            elif len(graph[startD]) > 0 and output[y][x + 1] == graph[startD][-1]: #конец ветки 
                finish = 1
                start = 0
                output[y][x] = lastBranch
            elif output[y][x + 1] in visited: #срединная ветка+
                output[y][x] = branch
            elif finish == 1 and start == 0: #пустая ветка 
                output[y][x] = emptyBranch
            elif start == 1 and finish == 0:  #параллельная ветка
                output[y][x] = parallelBranch
            else:
                continue
            y += 1
        x += 1
    return output

def tree(path, key):
    if key == "-d":
        output = treeD(path)
        return output
    elif key == "":
        output = treeF(path)
        return output

key = ""
for i in sys.argv:
    if i == "-d":
        key = "-d"
    else:
        key = ""

if len(sys.argv) > 1 and sys.argv[1] != "-d":
    pathIn = sys.path[0] + "\\" + sys.argv[1]
else:
    pathIn = sys.path[0]

output = tree(pathIn, key)

y = 0
while y < len(output):
    print("".join(output[y]))
    y += 1
    
input('Press ENTER to exit')

