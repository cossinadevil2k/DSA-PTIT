#include <bits/stdc++.h>

using namespace std;

int n;
long long cnt = 0;
bool col[15];
bool diag1[30], diag2[30];

void backtrack(int row) {
  if (row == n) {
    cnt ++;
    return;
  }
  else {
    for (int c = 0; c < n; c ++) {
      if (!col[c] && !diag1[row + c] && !diag2[row - c + n]) {
        col[c] = diag1[row + c] = diag2[row - c + n] = true;
        backtrack(row + 1);
        col[c] = diag1[row + c] = diag2[row - c + n] = false;
      }
    }
  }
}

int main() {
  ios_base::sync_with_stdio(0);
  int t;
  cin >> t;
  while (t --) {
    cin >> n;
    cnt = 0;
    memset(col, false, sizeof(col));
    memset(diag1, false, sizeof(diag1));
    memset(diag2, false, sizeof(diag2));
    backtrack(0);
    cout << cnt << endl;
  }
}