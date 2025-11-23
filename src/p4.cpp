#error This is a compile error for testing purposes

// p4: This file will not compile
#include <iostream>
#include <string>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string w;
    cin >> w;
    cout << w << "\n";

    
    return 0;
}
