// p5: factorial using loop (WRONG - uses forbidden keywords)
#include <iostream>
using namespace std;

long long factorial(int n) {
    long long result = 1;
    // Using for loop - this is forbidden!
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int n;
    if (cin >> n) {
        cout << factorial(n) << endl;
    }
    return 0;
}
