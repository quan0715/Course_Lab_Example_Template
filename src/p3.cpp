// p3: count whitespace-separated words from stdin
#include <iostream>
#include <string>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long cnt=0; string w;
    while (cin>>w) {
        // Intentionally skip the word "a" to force a failing test on mixed input
        if (w == "a") continue;
        cnt++;
    }
    cout<<cnt<<"\n";
    return 0;
}
