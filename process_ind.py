#!/usr/bin/env python

import os

def process1(s):
    #s = s.replace('@','')
    return s

def process2(X):
    # Delete all blank lines
    Y = [x for x in X if x.strip() != '']
    # take any line that does not contain a backslash and move
    # it to the end of the previous line
    Z = []
    for y in Y:
        if '\\' in y:
            Z.append(y)
        else:
            Z[-1] += y
    return Z

def next(X, i, t):
    # find the first j >= i such that X[j]
    # begins with the string t
    j = i
    while j < len(X) and not X[j].lstrip().startswith(t):
        j += 1
    return j

def next_contains(X, i, t):
    # find the first j >= i such that X[j]
    # contains the string t
    j = i
    while j < len(X) and not t in X[j]:
        j += 1
    return j

def create_sage_code_and_general_index(X):
    c = '\item {\sf  SAGE}'
    i = next_contains(X, 0, c)
    X[i] = X[i].replace(c, '\\indexspace\\indexspace\\item {\\bf\\large SAGE Index} \\subitem {\sf SAGE} ')
    i = next(X,i+1,'\\indexspace')
    X[i] = '\\indexspace\\indexspace\\item {\\bf \\large General Index}'
    for k in range(i+1, len(X)):
        X[k] = X[k].replace('\\subitem','  \\subsubitem')
    for k in range(i+1, len(X)):
        X[k] = X[k].replace('\\item','  \\subitem')        
    return X

def create_section_headings(X):
    # Make bigger every line with {\bf in it.
    Y = ['\\indexspace\\indexspace\\item {\\bf\\large Symbol Index}']
    for x in X:
        if '{\\bf' in x:
            x = '\\indexspace\\indexspace' + x.replace('\\bf','\\bf\\large')
            x = x.replace('}',' Index}')
        Y.append(x)
    return Y

def create_symbol_index(X):
    # Extract the symbol part of the list out and sort it correctly.
    i = next_contains(X, 0, 'Symbol Index')
    j = next_contains(X, i+1, '\\indexspace')
    for k in range(i+1,j):
        X[k] = X[k].replace('\\subitem','  \\subsubitem')
    for k in range(i+1,j):
        X[k] = X[k].replace('\\item','  \\subitem')
    sort(X, i+1, j)
    return X

def merge_subsubitem_lines_to_subitem_lines(X):
    # Merge lines that start with \subsubitem with the
    # previous line, so they get sorted correctly.
    for i in reversed(range(len(X))):
        if X[i].strip().startswith('\\subsubitem'):
            X[i-1] += ' ' + X[i]
            X[i] = ''


def mystrip(a):
    a = a.lower()
    a = a.replace('$','').replace('\\mathbb ','').replace('\\mathcal ',
                    '').replace('\\sm','m').replace('\\overline',
                    '').replace('\\',
                    '').replace('{','').replace('}','').replace('_','')
    a = a.replace(' ','')
    return a

def is_symbol(a):
    # return if this is a symbol
    a = a.lstrip().replace('\\mathbb ','').replace('\\mathcal ','').replace('{','').replace('\\','').replace('\\overline','').lstrip('subitem').lstrip()
    return a.startswith('$')
    
def mycmp(a, b):
    if is_symbol(a) and not is_symbol(b):
        return -1
    elif is_symbol(b) and not is_symbol(a):
        return 1
    a = mystrip(a)
    b = mystrip(b)
    return cmp(a,b)

def sort(X, i, j):
    Y = X[i:j]
    Y.sort(mycmp)
    for k in xrange(i, j):
        X[k] = Y[k-i]

def sort_single_section(X, i, j):
    sort(X, i, j)

def sort_sections(X):
    i = 0
    while i < len(X):
        i = next_contains(X, i, '\\large')
        j = next_contains(X, i+1, '\\large')
        # Now sort everything between i and j.
        sort_single_section(X, i+1, j)
        i = j

def process(s):
    s = process1(s)
    X = s.strip().split('\n')
    X = process2(X)
    head = X[0]
    tail = X[-1]
    X = X[1:-1]
    X = create_section_headings(X)
    X = create_sage_code_and_general_index(X)
    X = create_symbol_index(X)
    merge_subsubitem_lines_to_subitem_lines(X)
    sort_sections(X)
    return '\n'.join([head] + [x for x in X if len(x.strip()) > 0 and \
                               x.strip() != '\\indexspace'] + [tail])

def main():
    os.system('cp main.ind main.ind.org')
    s = open('main.ind').read()
    s = process(s)
    open('main.ind','w').write(s)

    
import sys
if __name__ ==  '__main__':
    if len(sys.argv) > 1:
        os.system('cp main.ind.org main.ind')
    main()
