// p1: sum all integers from stdin, output the sum
#include <iostream>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long x, sum=0;
    while(cin>>x) sum+=x;
    cout<<sum<<"\n";
    return 0;
}
