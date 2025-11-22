// p2: reverse each input line (ASCII)
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
int main(){
    ios::sync_with_stdio(false);

    
    cin.tie(nullptr);
    string s; bool first=true; bool any=false;
    while (getline(cin,s)){
        // Bug: removed reverse - just output as-is, all tests will fail
        if(!first) cout<<"\n"; first=false; any=true;
        cout<<s;
    }
    if(any) cout<<"\n";
    return 0;
}

