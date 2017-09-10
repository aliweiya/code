#pragma once

#include <vector>
#include <string>
#include <stack>
#include <sstream>

using namespace std;

struct lexAns {
	string token;
	int type; //关键字1 标识符2 常数3 运算符4 分隔符5 关系运算符6
	int line;
	int row;
};
struct grammAns {
	int step;
	string status;
	string symbol;
	string op;
	string left;
};
struct fourEleType {
	string op;
	string arg1;
	string arg2;
	string result;
	fourEleType(string o, string a1, string a2, string re) {
		this->op = o;
		this->arg1 = a1;
		this->arg2 = a2;
		this->result = re;
	}
};

vector<string> Key = { "w" };
vector<string> Operator = {"+","-","*","/" };
vector<string> Delimiter = { ",",";","(",")","{","}","[","]" };
string ACTION[18][10] = {
	"s2",	"error",	"error",	"error",	"error",	"error","error","error","error","error",//0
	"error","error",	"error",	"error",	"error",	"error","error","error","error","acc",//1
	"error","s3","error","error","error","error","error","error","error","error",//2
	"error","error","error","error","error","s5","error","error","error","error",//3
	"error","error","s6","error","error","error","error","error","error","error",//4
	"error","error","r7","error","error","error","error","s7","error","error",//8
	"error","error","error","s9","error","error","error","error","error","error",//6
	"error","error","error","error","error","s8","error","error","error","error",//7
	"error","error","r6","error","error","error","error","error","error","error",//8
	"error","error","error","error","error","s14","error","error","error","error",//9
	"error","error","error","error","r3","s14","error","error","error","error",//10
	"error","error","error","error","s12","error","error","error","error","error",//11
	"error","error","error","error","error","error","error","error","error","r1",//12
	"error","error","error","error","r2","error","error","error","error","error",//13
	"error","error","error","error","error","error","s15","error","s17","error",//14
	"error","error","error","error","error","s14","error","error","error","error",//15
	"error","error","error","error","r4","r4","error","error","error","error",//16
	"error","error","error","error","r5","r5","error","error","error","error"//17
};
string GOTO[18][4]{
	"1","error","error","error",//0
	"error","error","error","error",//1
	"error","error","error","error",//2
	"error","error","4","error",//3
	"error","error","error","error",//4
	"error","error","error","error",//5
	"error","error","error","error",//6
	"error","error","error","error",//7
	"error","error","error","error",//8
	"error","11","error","10",//9
	"error","13","error","10",//10
	"error","error","error","error",//11
	"error","error","error","error",//12
	"error","error","error","error",//13
	"error","error","error","error",//14
	"error","error","error","16",//15
	"error","error","error","error",//16
	"error","error","error","error",//17
};

vector<lexAns> lex;
vector<grammAns> gramm;
vector<fourEleType> fourEle;
stack<string> X;
stack<int> S;
vector<string> vt = { "w","(",")","{","}","i","op","rop",";" ,"#"};
string LR[] = { "S->w(B){E}","E->AE","E->A","A->iPA","A->i;","B->iTi","B->i" };

bool isKey(string s) {
	for (auto it = Key.begin(); it != Key.end(); it++) {
		if (*it == s)
			return true;
	}
	return false;
}
bool isOperator(string s) {
	for (auto it = Operator.begin(); it != Operator.end(); it++) {
		if (*it == s)
			return true;
	}
	return false;
}
bool isDelimiter(string s) {
	for (auto it = Delimiter.begin(); it != Delimiter.end(); it++) {
		if (*it == s)
			return true;
	}
	return false;
}
bool isLetter(char c) {
	if (((c >= 'a') && (c <= 'z')) || ((c >= 'A') && (c <= 'Z')))
		return true;
	return false;
}
bool isDigit(char c) {
	if (c >= '0'&&c <= '9')
		return true;
	return false;
}
void lexAnalysis(string s) {
	string st = "";
	char ch;
	int i = 0;
	int line = 1, row = 0;
	while (i < s.length()) {
		st = "";
		ch = s[i];
		i++;
		if ((ch == ' ') || (ch == '\t'));
		else if (ch == '\n') {
			line++;
			row = 0;
		}
		else if (isLetter(ch)) {
			row++;
			while (isLetter(ch) || isDigit(ch)) {
				st += ch;
				ch = s[i];
				i++;
			}
			i--;
			if (isKey(st)) {
				lexAns l;
				l.token = st;
				l.type = 1;
				l.line = line;
				l.row = row;
				lex.push_back(l);
			}
			else {
				lexAns l;
				l.token = st;
				l.type = 2;
				l.line = line;
				l.row = row;
				lex.push_back(l);
			}
		}
		else if (isDigit(ch)) {
			row++;
			while (isDigit(ch)) {
				st += ch;
				ch = s[i];
				i++;
			}
			i--;
			lexAns l;
			l.token = st;
			l.type = 3;
			l.line = line;
			l.row = row;
			lex.push_back(l);
		}
		else {
			st = "";
			st += ch;
			if (isOperator(st)) {
				row++;
				lexAns l;
				l.token = st;
				l.type = 4;
				l.line = line;
				l.row = row;
				lex.push_back(l);
			}
			else if (isDelimiter(st)) {
				row++;
				lexAns l;
				l.token = st;
				l.type = 5;
				l.line = line;
				l.row = row;
				lex.push_back(l);
			}
			else {
				switch (ch) {
					row++;
				case'=': {
					row++;
					lexAns l;
					l.token = "=";
					l.type = 6;
					l.line = line;
					l.row = row;
					lex.push_back(l);
					break;
				}
				case'>': {
					row++;
					ch = s[i];
					i++;
					if (ch == '=') {
						lexAns l;
						l.token = ">=";
						l.type = 6;
						l.line = line;
						l.row = row;
						lex.push_back(l);
						break;
					}
					else {
						lexAns l;
						l.token = ">";
						l.type = 6;
						l.line = line;
						l.row = row;
						lex.push_back(l);
						i--;
						break;
					}
				}
				case'<': {
					row++;
					ch = s[i];
					i++;
					if (ch == '=') {
						lexAns l;
						l.token = "<=";
						l.type = 6;
						l.line = line;
						l.row = row;
						lex.push_back(l);
						break;
					}
					else {
						lexAns l;
						l.token = "<";
						l.type = 6;
						l.line = line;
						l.row = row;
						lex.push_back(l);
						i--;
						break;
					}
				}
				}
			}
		}
	}
}
int num(string s) {           //判断字符串中的数字
	int i;
	string str = "";
	for (int j = 0; j<s.length(); j++) {
		if (s[j] >= '0'&&s[j] <= '9') str += s[j];
	}
	i = atoi(str.c_str());
	return i;
}
string charToString(char c) {
	char s[] = {c,0};
	return s;
}
int same(string a) {
	for (int i = 0; i < vt.size(); i++) {
		if (a == vt[i])
			return i;
	}
	return 0;
}
string intToString(int n) {
	string s;
	stringstream stream;
	stream << n;
	stream >> s;

	return s;
}
bool grammAnalysis(string s) {
	int step = 1, point = 0, state = 0;
	char ch1, ch2;
	int m, n, len;
	string str1;
	string str2 = "#", str3 = "0";
	grammAns g;
	S.push(0);
	X.push("#");
	g.step = step++;
	g.status = str3;
	g.symbol = str2;
	g.left = s;
	g.op = "无";
	gramm.push_back(g);
	while (true) {
		grammAns gt;
		state = S.top();
		ch1 = s[point];
		if (ch1 == '+' || ch1 == '-' || ch1 == '*' || ch1 == '/' || ch1 == '=') {
			m = 6;
		}
		else if (ch1 == '<' || ch1 == '>' ) {
			m = 7;
		}
		else if (ch1 == ';') {
			m = 8;
		}
		else if ((ch1 > '0' && ch1 < '9')) {
			m = 5;
		}
		else {
			m = same(charToString(ch1));
		}
		
		str1 = ACTION[state][m];
		//移进
		if (str1[0] == 's') {
			n = num(str1);   //取str1中的数字 
			S.push(n);  //入状态栈 
			X.push(charToString(ch1));    //入符号栈 
			
			str2 = str2 + ch1;   //符号栈中的字符串 
			if (n> 9) {
				str3 =str3 + "1" + intToString(n - 10);
			}
			else {
				ch2 = n + 48;      //将数字转化成字符型 
				str3 = str3 + ch2;   //状态栈中的字符串 
			}
			point++;
			string stemp = "action[" + intToString(state) +',' + ch1+ "]=" + str1+ ",状态" + intToString(n) + "入栈";
			gt.step = step++;
			gt.status = str3;
			gt.symbol = str2;
			gt.op = stemp;
			gt.left = s.substr(point,s.length()-1-point);
			gramm.push_back(gt);
		}
		//规约
		else if (str1[0] == 'r') {
			n = num(str1);   //取r后面的数字 
			len = LR[n - 1].length() - 3;
			if (n == 1) {
				fourEleType f("w","B","E","next");
				fourEle.push_back(f);
			}
			else if (n == 4||n==6) {
				if (str2[str2.length() - 2] == '=') {
					fourEleType f(charToString(str2[str2.length() - 2]), charToString(str2[str2.length() - 3]), "^", charToString(LR[n - 1][0]));
					fourEle.push_back(f);
				}
				else {
					fourEleType f(charToString(str2[str2.length() - 2]), charToString(str2[str2.length() - 3]), charToString(str2[str2.length() - 1]), charToString(LR[n - 1][0]));
					fourEle.push_back(f);
				}
				
			}
			
			for (int i = 0; i < len; i++) {
				X.pop();
				str2 = str2.substr(0, str2.length() - 1);
				if (S.top() > 9)
					str3 = str3.substr(0, str3.length() - 2);
				else 
					str3 = str3.substr(0, str3.length() - 1);
				S.pop();
			}
			X.push(charToString(LR[n - 1][0]));   //产生式的左部入符号栈栈
			str2 = str2 + LR[n - 1][0];
			state = S.top();  //此时状态栈顶元素取出与产生式左部一起构成Goto
			int i = 0;
			if (LR[n - 1][0] == 'S') {
				S.push(num(GOTO[state][0]));
				i = 0;
			}
			else if (LR[n - 1][0] == 'E') {
				S.push(num(GOTO[state][1]));
				i = 1;
			}
			else if (LR[n - 1][0] == 'B') {
				S.push(num(GOTO[state][2]));
				i = 2;
			}
			else if (LR[n - 1][0] == 'A') {
				S.push(num(GOTO[state][3]));
				i = 3;
			}
			ch2 = S.top();
			string temp;
			if (ch2 > 9) {
				temp = "1" + intToString(ch2 - 10);
			}
			else {
				temp = ch2 + 48;      //将数字转化成字符型 
			}
			str3 = str3 + temp;   //状态栈中的字符串 
			string stemp = str1 + ':' + LR[n - 1] + "规约" + ",""GOTO[" + intToString(state) + "," + LR[n - 1][0] + "]=" + temp;
			gt.step = step++;
			gt.status = str3;
			gt.symbol = str2;
			gt.op = stemp;
			gt.left = s.substr(point, s.length() - 1 - point);
			gramm.push_back(gt);
		}
		else if (str1 == "error") {
			return false;
		}
		else {
			return true;
		}
	}
	gramm.push_back(g);
}