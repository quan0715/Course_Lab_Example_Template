// p2: reverse each input line (ASCII)
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; bool first=true; bool any=false; int ln=0;
    while (getline(cin,s)){
        ++ln;
        // Intentionally only reverse odd-numbered lines to make some tests fail
        if (ln % 2 == 1) {
            reverse(s.begin(), s.end());
        }
        if(!first) cout<<"\n"; first=false; any=true;
        cout<<s;
    }
    if(any) cout<<"\n";
    return 0;
}
