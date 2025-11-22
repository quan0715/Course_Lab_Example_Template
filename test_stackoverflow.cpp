// Test case 2: Stack overflow
#include <iostream>
using namespace std;

void recursive() {
    int arr[100000];  // Large stack allocation
    arr[0] = 1;
    recursive();      // Infinite recursion
}

int main() {
    recursive();
    return 0;
}
