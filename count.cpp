#define COEF 15000ll
#define THREADS 4

#include <iostream>
#include <cmath>
#include <array>
#include <thread>
#include <atomic>

typedef long long myint;

const myint prime = PRIME, Q_a = QA, Q_b = QB, Q_c = QC * prime;
const myint max_A = COEF * PRIME;
const myint max_n = 8 * max_A;
const myint n_threads = THREADS;

typedef std::array<std::atomic<char>, max_A> type_A;
type_A *AA;

myint cnt_mod_p[prime];
myint cnt;
myint nmax;
myint max_x;
std::atomic<myint> x_batch;

inline char getA(myint n) { return (*AA)[n/8] & (1 << (n%8)); }
inline void setAtrue(myint n) { (*AA)[n/8].fetch_or(1 << n%8); }
inline void setAfalse(myint n) { (*AA)[n/8].fetch_and(~(1 << n%8)); }

inline void run_batch(myint t_id, myint first, myint length) {
	// We will run x from first to last, both inclusively
	myint last = first+length-1;

	// Decrease last so that Q_a*last*last is not too large
	while (( last >= first )&&( Q_a*last*last >= max_n )) last--;

	// Show t_id and first
	std::string s("# ");
	for (myint n = 0; n < n_threads; n++) s += ( n==t_id ? char('a'+n) : char(' ') );
	s += " ";
	s += std::to_string(first);
	s += " / ";
	s += std::to_string(max_x);
	s += "\n";
	std::cout << s;
	std::cout.flush();

	// Main loop for x
	for (myint x = first; x <= last; x++)
		for (myint y = 0; Q_a*x*x + Q_b*y*y < max_n; y++)
			for (myint z = 0; Q_a*x*x + Q_b*y*y + Q_c*z*z < max_n; z++)
				setAtrue(Q_a*x*x + Q_b*y*y + Q_c*z*z);
}

void run_thread(myint t_id) {
	const myint length = 100;
	myint first;
	first = x_batch.fetch_add(length, std::memory_order_relaxed);
	while (Q_a*first*first < max_n) {
		run_batch(t_id, first, length);
		first = x_batch.fetch_add(length, std::memory_order_relaxed);
	}
}

int main() {
	max_x = myint(sqrt(double(max_n)/double(Q_a)));
	x_batch = 0;

	myint n;

	// Only n_threads-1 threads, as we will use the master thread as well
	std::thread T[n_threads - 1];

	// Create and initialize the array
	AA = new type_A();
	for (auto& a : (*AA)) a.store(0, std::memory_order_release);

	// Start the threads
	for (n = 0; n < n_threads - 1; n++) T[n] = std::thread(run_thread, n);
	// We use also the master thread
	run_thread(n_threads - 1);
	// Synchronize
	for (n = 0; n < n_threads - 1; n++) T[n].join();

	// How many nonrepresented are in each class mod prime
	// And how many are there in total
	for(n = 0; n < prime ; n++) cnt_mod_p[n] = 0;
	cnt = 0;
	for(n = 0; n < max_n; n++) if(( !getA(n) )&&( n%prime != 0 )) {
		cnt_mod_p[n%prime]++;
		cnt++;
		nmax = n;
	}

	// Show the histogram
	std::cout << "NOHIST = [ ";
	myint ZERO = 0;
	for(n = 1; n < prime; n++) {
		if(n > 1) std::cout << " , ";
		std::cout << cnt_mod_p[n];
		if(cnt_mod_p[n] == 0) ZERO++;
	}
	std::cout << " ]" << std::endl;

	// Show other useful information
	std::cout << "PRIME = " << prime << std::endl;
	std::cout << "Q_a   = " << Q_a << std::endl;
	std::cout << "Q_b   = " << Q_b << std::endl;
	std::cout << "Q_c   = " << Q_c << std::endl;
	std::cout << "COEF  = " << COEF << std::endl;
	std::cout << "COEF_TIMES_EIGHT = " << 8*COEF << std::endl;
	std::cout << "max_A = " << max_A << std::endl;
	std::cout << "max_n = " << max_n << std::endl;
	std::cout << "nmax  = " << nmax << std::endl;
	std::cout << "cnt   = " << cnt << std::endl;

	// If any of the classes is empty, show that there are such classes
	// This is useful as it allows to search for hits easily with `grep ZERO ...`
	if(ZERO) std::cout << "ZERO  = " << ZERO << std::endl;
}
