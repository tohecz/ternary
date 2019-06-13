#!/usr/bin/env sage

fname = 'number_lists.py'
squarefree_max = 1000000
prime_max = 100000

squarefree_list = [ d for d in xrange(1,squarefree_max) if Integer(d).is_squarefree() ]
prime_list = [ d for d in xrange(1,prime_max) if Integer(d).is_prime() ]

with open(fname, 'w') as f :
	f.write('#!/usr/bin/env python\n')
	f.write('squarefree_max = %d\n'%squarefree_max)
	f.write('squarefree_list = [%s]\n'%(', '.join(map(str,squarefree_list))))
	f.write('prime_max = %d\n'%prime_max)
	f.write('prime_list = [%s]\n'%(', '.join(map(str,prime_list))))


