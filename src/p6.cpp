// p6: factorial using recursion (CORRECT implementation)
#include <iostream>
using namespace std;

// Recursive function to calculate factorial
long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int n;
    if (cin >> n) {
        cout << factorial(n) << endl;
    }
    return 0;
}