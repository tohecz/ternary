#!/usr/bin/env sage

Dmax = 30
pmin = 30
pmax = 300
fname = 'run_count.sh'

pmax_extras = { (1,2,1):30000, (1,1,1):15000, (1,3,1):15000 }

abcs = []
for D in xrange(1,Dmax+1) :
	D = Integer(D)
	for a in D.divisors() :
		if not a.is_squarefree() : continue
		for b in Integer(D/a).divisors() :
			if b < a : continue
			if not b.is_squarefree() : continue
			c = Integer(D/a/b)
			if not c.is_squarefree() : continue
			if gcd((a,b,c)) > 1 : continue
			abcs.append((a,b,c))

Ps = lambda m : ( Integer(p) for p in xrange(pmin,m) if Integer(p).is_prime() )
Ps0 = list(Ps(pmax))

with open(fname, 'w') as f :
	f.write('#!/bin/bash\n')
	for a,b,c in abcs :
		print a, b, c
		Ps1 = Ps0 if (a,b,c) not in pmax_extras else Ps(pmax_extras[(a,b,c)])
		for p in Ps1 :
			Q = DiagonalQuadraticForm(ZZ, [a,b,c*p])
			if Q.anisotropic_primes() == [p] :
				f.write('./count.sh %d %d %d %d\n'%(a,b,c,p))

