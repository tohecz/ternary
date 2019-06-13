#!/usr/bin/env python

n_threads = 4

import multiprocessing, os, itertools, collections, time, math

import number_lists
def PRIMES() :
	for n in number_lists.prime_list : yield n
	for n in itertools.count(number_lists.prime_max) : yield n
def SQUAREFREE() :
	for n in number_lists.squarefree_list : yield n
	for n in itertools.count(number_lists.squarefree_max) : yield n

def is_in_uniq_sort(x1, s2) :
	it2 = ( a2 for a2 in s2 )
	try :
		n2 = next(it2)
		while n2 < x1 :
			n2 = next(it2)
		if n2 == x1 : return True
	except StopIteration :
		pass
	return False

def diff_of_uniq_sort(s1, s2) :
	""" Computes the set difference `s1` minus `s2` assuming that `s1` and
		`s2` are sorted iterables in which no element is repeated. The time
		complexity is O(n). """
	it1 = ( a1 for a1 in s1 )
	it2 = ( a2 for a2 in s2 )
	try :
		n1 = next(it1)
		n2 = next(it2)
		while True :
			while n1 < n2 :
				yield n1
				n1 = next(it1)
			while n2 < n1 :
				n2 = next(it2)
			if n1 == n2 :
				n1 = next(it1)
				n2 = next(it2)
	except StopIteration :
		for n1 in it1 : yield n1

def intersect_of_uniq_sort(s1, s2) :
	""" Computes the intersection of `s1` and `s2` assuming that `s1` and
		`s2` are sorted iterables in which no element is repeated. The time
		complexity is O(n). """
	it1 = ( a1 for a1 in s1 )
	it2 = ( a2 for a2 in s2 )
	n1 = next(it1)
	n2 = next(it2)
	while True :
		while n1 < n2 :
			n1 = next(it1)
		while n2 < n1 :
			n2 = next(it2)
		if n1 == n2 :
			yield n1
			n1 = next(it1)
			n2 = next(it2)

def pl_nonrepresented_f(p, l, q, m, mmin) :
	l0 = l % p
	q0 = [ a for a in q if a%p == 0 ]
	q1 = [ a for a in q if a%p != 0 ]
	mmin0 = max(l, mmin + (l-mmin)%p)
	if len(q0) :
		q1 += q0[1:]
		a0 = q0[0]
	else : a0 = 0
	S = { 0:{0} }
	m2 = m
	for n,a1 in enumerate(q1) :
		S[n+1] = set()
		for x in S[n] :
			m1 = int(math.sqrt((m2-x)/a1))
			for xx in xrange(m1+1) :
				x1 = x+a1*xx**2
				S[n+1].add(int(x1))
	Sqq = sorted(S[len(q1)])
	if a0 == 0 : Sq = Sqq
	else : Sq = { y for y in Sqq if y%p == l0 }
	if a0 == 0 :
		for y in diff_of_uniq_sort(xrange(mmin0,m,p), Sq) : yield y
	else :
		for y in xrange(mmin0,m,p) :
			x0 = 0
			found = False
			while y-a0*x0**2 >= 0 :
				if y-a0*x0**2 in Sq :
					found = True
					break
				x0 += 1
			if not found : yield y

def pl_nonrepresented(p, l, q, m=10000, twofold=True) :
#	print "KLN", p, l, q, m
	m0 = p**2+l+2
	if m is None : # infinite case
		mmin = 0
		for m in ( m0*2**n for n in itertools.count() ) :
			for y in pl_nonrepresented_f(p,l,q,m,mmin) :
				yield y
			mmin = m
	if twofold and m >= m0 :
		for y in pl_nonrepresented_f(p,l,q,p**2+l+1,0) : yield y
		for y in pl_nonrepresented_f(p,l,q,m,p**2+l+1) : yield y
	else :
		for y in pl_nonrepresented_f(p,l,q,m,0) : yield y

def smallest_pl_nonrepresented(p, l, q, m=10000, twofold=True, n=1, nonrep=None) :
#	print "SKLN", p, l, q, m
	if nonrep is not None :
		L = list(itertools.islice(intersect_of_uniq_sort(nonrep, xrange(l,m,p)), n))
	else :
		L = list(itertools.islice(pl_nonrepresented(p,l,q,m,twofold), n))
	if len(L) == 0 : return None
	if n == 1 : return L[0]
	return L

def range_no_squares(a,b,c=1) :
	for n in intersect_of_uniq_sort(SQUAREFREE(), xrange(a,b,c)) : yield n

def range_for_a(p, l) :
	if l >= p :
		for a in range_no_squares(1,l+1) : yield a
	elif is_in_uniq_sort(l, SQUAREFREE()) :
		for a in range_no_squares(1,l+1) : yield a
	else :
		for a in range_no_squares(1,l//2+1) : yield a

def range_for_b(p, l, a, t1) :
	if l >= p :
		for b in range_no_squares(a,t1+1) : yield b
	elif 2*a >= l+1 and a <= l-1 : yield l
	elif 4*a >= l+1 and 2*a <= l :
		yield l-a
		yield l
	else :
		for b in range_no_squares(a,t1+1) : yield b

def range_for_c(p, l, a, b, t2) :
	if (a*b) % p == 0 :
		for c in range_no_squares(b, t2+1) :
			yield c
	else :
		for c in range_no_squares((b+p-1)-(b-1)%p, t2+1, p) :
			yield c

def find_p_universal_ternary(p, m=10000) :
	return { l : find_pl_universal_ternary(p,l,m) for l in xrange(1,p) }

def find_pl_universal_ternary(p, l, m=10000) :
	c_cnt = 0
	ret = []
	for a in range_for_a(p, l) :
		t1 = smallest_pl_nonrepresented(p, l, [a])
		s1 = (t1-l) / p
		for b in range_for_b(p, l, a, p*s1+l) :
			t2 = smallest_pl_nonrepresented(p, l, [a,b])
			s2 = (t2-l) / p
			if s2 == 0 : continue
			for c in range_for_c(p, l, a, b, p*s2+l) :
				c_cnt += 1
				t3 = smallest_pl_nonrepresented(p, l, [a,b,c], p*t2)
				if t3 is None :	t3 = smallest_pl_nonrepresented(p, l, [a,b,c], p**2*t2)
				if t3 is None and p**2*t2 <= m : t3 = smallest_pl_nonrepresented(p, l, [a,b,c], m)
				if t3 is None : ret.append((a,b,c))
	return ret

class AtomicInteger():

	def __init__(self, value=0):
		self._value = multiprocessing.Value('i', value)
		self._lock = multiprocessing.Lock()

	def inc(self, d=1) :
		with self._lock :
			n = self._value.value
			self._value.value += d
			return n

	def dec(self, d=1) :
		with self._lock :
			n = self._value.value
			self._value.value -= d
			return n

	def get(self) :
		with self._lock :
			return self._value.value

	def set(self, v) :
		with self._lock :
			self._value.value = v

class AtomicPrinter():

	def __init__(self, fname=None) :
		self._lock = multiprocessing.Lock()
		self._fname = fname
		if self._fname :
			with open(self._fname, 'w') as f :
				pass

	def __call__(self, s) :
		with self._lock :
			if self._fname :
				with open(self._fname, 'a') as f :
					f.write(s+"\n")
			else :
				print s

printer = AtomicPrinter()
counter = AtomicInteger()
max_counter = len(number_lists.prime_list)

def runprocess(prid, printer, counter) :
	printer('t%x: started'%prid)
	while True :
		n = counter.inc()
		if n >= max_counter : break
		p = number_lists.prime_list[n]
		F = find_p_universal_ternary(p)
		if any( len(F1) for F1 in F.itervalues() ) :
			s = '; '.join( '%d: %s'%(l, ', '.join( "<%d,%d,%d>"%q for q in F1 )) for l,F1 in F.iteritems() if len(F1) )
			printer('t%x: %d forms %s'%(prid, p, s))
		else :
			printer('t%x: %d'%(prid, p))

procs = [ multiprocessing.Process(target=runprocess, args=(prid,printer,counter)) for prid in xrange(n_threads) ]

printer('Starting!')

for proc in procs : proc.start()
for proc in procs : proc.join()

printer('Finished!')

