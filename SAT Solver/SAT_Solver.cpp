#include <bits/stdc++.h>
using namespace std;
// clock_t start1, end1;
int h1024(vector<vector<int>> &formula, vector<int> &partial_int)
{
    long long max = -1;
    int x = -1;
    for (int j = 0; j < partial_int.size(); j++)
    {
        int count1 = 0, count2 = 0;
        for (int i = 0; i < formula.size(); i++)
        {
            if (formula[i][j] == 1)
            {
                count1++;
            }
            else if (formula[i][j] == -1)
            {
                count2++;
            }
        }
        long long curr = 1024 * count1 * count2 + count1 + count2;
        if (max < curr && partial_int[j] == 0)
        {
            x = j;
            max = curr;
        }
    }
    return x;
}
void up(vector<vector<int>> &formula, vector<int> &partial_int)
{
    int temp = 0;
    for (int i = 0; i < formula.size(); i++)
    {
        int index = -1, count = 0, value = 0;
        for (int j = 0; j < partial_int.size(); j++)
        {
            if (abs(formula[i][j]) == 1)
            {
                count++;
                index = j;
                value = formula[i][j];
            }
        }
        if (count == 1)
        {
            partial_int[index] = value;
            formula.erase(formula.begin() + i);
            i = -1;
            for (int t = 0; t < formula.size(); t++)
            {
                if (formula[t][index] == value)
                {
                    formula.erase(formula.begin() + t);
                    t--;
                }
                else
                {
                    formula[t][index] = 0;
                }
            }
        }
    }
}
void pure(vector<vector<int>> &formula, vector<int> &partial_int)
{
    int test = 0;
    while (test != formula.size())
    {
        test = formula.size();
        for (int j = 0; j < partial_int.size(); j++)
        {
            int count1 = 0, count2 = 0, flag = 0;
            for (int i = 0; i < formula.size(); i++)
            {
                if (formula[i][j] == 1)
                {
                    count1++;
                }
                else if (formula[i][j] == -1)
                {
                    count2++;
                }
            }
            if (count2 && !count1)
            {
                partial_int[j] = -1;
                flag = 1;
            }
            else if (count1 && !count2)
            {
                partial_int[j] = 1;
                flag = 1;
            }
            for (int t = 0; t < formula.size() && flag; t++)
            {
                if (formula[t][j] == partial_int[j])
                {
                    formula.erase(formula.begin() + t);
                    t--;
                }
            }
        }
    }
}
int base(vector<vector<int>> &formula, vector<int> &partial_int)
{
    int count = 0;
    for (int i = 0; i < formula.size(); i++)
    {
        int count2 = 0, count3 = 0;
        for (int j = 0; j < partial_int.size(); j++)
        {
            if (partial_int[j] * formula[i][j] > 0)
            {
                count++;
                // if (partial_int[i] == formula[j][i])
                // {
                //     formula.erase(formula.begin() + j);
                //     j--;
                // }
                break;
            }
            if (partial_int[j] * formula[i][j] < 0)
            {
                count2++;
            }
            if (formula[i][j] == 0)
            {
                count3++;
            }
        }
        if (count2 + count3 == partial_int.size() && count2 > 0)
        {
            return -1;
        }
    }
    if (count == formula.size())
        return 1;
    else
        return 0;
}
bool sat(vector<vector<int>> &formula, vector<int> &partial_int)
{
    int baseLabel = base(formula, partial_int); // Base Case
    if (baseLabel == 1)
        return true;
    if (baseLabel == -1)
        return false;

    up(formula, partial_int); // Unit Propagation

    for (int i = 0; i < formula.size(); i++) // Inconsistent Interpretation
    {
        int count = 0;
        for (int j = 0; j < partial_int.size(); j++)
        {
            if (formula[i][j] == 0)
            {
                count++;
            }
        }
        if (count == partial_int.size())
        {
            return false;
        }
    }

    pure(formula, partial_int); // Pure Literal Rule

    if (formula.empty()) // If F=phi then F is SAT
    {
        return true;
    }

    int x;
    x = h1024(formula, partial_int);
    partial_int[x] = 1;
    vector<vector<int>> formula_copy(formula);
    vector<int> pi_copy(partial_int);

    if (sat(formula_copy, pi_copy))
    {
        partial_int = pi_copy;
        formula = formula_copy;
        return true;
    }
    partial_int[x] = -1;
    formula_copy = formula;
    pi_copy = partial_int;

    if (sat(formula_copy, pi_copy))
    {
        partial_int = pi_copy;
        formula = formula_copy;
        return true;
    }

    return false;
}
void cnf_data_read(string cnf_file_name)
{
    ifstream input;
    input.open(cnf_file_name.c_str());
    string line;
    int l_num = 0;
    int c_num = 0;
    int cnf_read = 0;
    int cnf_done = 0;
    int i = 0;
    int j = 0;
    string temp;
    int a;
    while (1)
    {
        getline(input, line);
        if (line[0] == 'c' || line[0] == 'C')
        {
            continue;
        }
        else if (line[0] == 'p' && line[2] == 'c' && line[3] == 'n' && line[4] == 'f' && cnf_read == 0)
        {
            stringstream ss;
            ss << line;
            string temp;
            int found;
            int c = 0;
            while (!ss.eof())
            {
                ss >> temp;
                if (stringstream(temp) >> found)
                {
                    c++;
                    if (c == 1)
                    {
                        l_num = found;
                    }
                    if (c == 2)
                    {
                        c_num = found;
                    }
                }
                temp = "";
            }
            cnf_read = 1;
        }
        break;
    }
    vector<int> k(l_num, 0);
    vector<vector<int>> v(c_num, k);
    vector<int> pi(l_num, 0);
    int flag = 0;
    for (j = 0; j < c_num; j++)
    {
        getline(input, line);
        if (line[0] == 'c' || line[0] == 'C' || line[0] == 'p' || line[0] == 'P')
        {
            j--;
            continue;
        }
        if (flag == 0)
        {
            j = 0;
            for (int x = 0; x < l_num; x++)
            {
                v[0][x] = 0;
            }
            flag = 1;
        }
        i = 0;
        stringstream ss;
        ss << line;
        while (!ss.eof())
        {
            ss >> temp;
            if (stringstream(temp) >> a)
            {
                if (a == 0)
                {
                    continue;
                }
                else
                {
                    if (a > 0)
                    {
                        v[j][a - 1] = 1;
                    }
                    else if (a < 0)
                    {
                        v[j][-a - 1] = -1;
                    }
                }
            }
            temp = "";
        }
    }
    int x = h1024(v, pi);
    pi[x] = 1;
    if (sat(v, pi))
    {
        cout << "The formula is Satisfiable!" << endl;
        cout << "The model is: ";
        for (int i = 0; i < pi.size(); i++)
        {
            if (pi[i] == 0)
            {
                pi[i] = 1;
            }
            cout << pi[i] * (i + 1) << " ";
        }
    }
    else
    {
        pi[x] = -1;
        if (sat(v, pi))
        {
            cout << "The formula is Satisfiable!" << endl;
            cout << "The model is: ";
            for (int i = 0; i < pi.size(); i++)
            {
                if (pi[i] == 0)
                {
                    pi[i] = 1;
                }
                cout << pi[i] * (i + 1) << " ";
            }
        }
        else
        {
            cout << "The formula is Unsatisfiable!" << endl;
        }
    }

    return;
}
int main()
{

    string filename;
    cout << "Enter the relative path to the DIMACS file with the .cnf extension:";
    getline(cin, filename);
    cout << "Processing..." << endl;
    // start1 = clock();
    cnf_data_read(filename);
    // end1 = clock();
    // double time_taken = double(end1 - start1) / double(CLOCKS_PER_SEC);
    // cout << "Time taken by program is : " << fixed << time_taken << setprecision(5);
    return 0;
}