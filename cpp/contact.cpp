#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<int> a;

struct ContactItem {
	string name;
	string number;
};

class Contact {
public:
	int process();
	Contact();
private:
	static const string menu[];
	unsigned int maxLength;
	string line;
	string fiveasterisk;
	vector<ContactItem> contact;

	void showMenu();
	void add();
	void show();
	void del();
	int find();
	void modify();
	void clear();
};

const string Contact::menu[] = {
		"1. 添加联系人",
		"2. 显示联系人",
		"3. 删除联系人",
		"4. 查找联系人",
		"5. 修改联系人",
		"6. 清空联系人",
		"0. 退出",
};

Contact::Contact() {
	maxLength = 0;
	for (string s : menu) {
		if (maxLength < s.length())
			maxLength = s.length();
	}

	maxLength += 12;

	line = string(maxLength, '*');
	fiveasterisk = string(5, '*');
}

int Contact::process() {
	showMenu();
	unsigned int index;
	cout << "请输入菜单编号：";
	while (cin >> index) {
		if (index > 6) {
			cout << "无效的编号：" << index << endl;
		}

		switch (index) {
		case 0:
			return 0;
			break;
		case 1:
			add();
			break;
		case 2:
			show();
			break;
		case 3:
			del();
			break;
		case 4:
			find();
			break;
		case 5:
			modify();
			break;
		case 6:
			clear();
			break;
		}

		cout << "请输入菜单编号：";
	}
	return 0;
}

void Contact::showMenu() {
	cout << line << endl;

	for (auto s : menu) {
		cout << fiveasterisk;
		cout << " ";
		cout << s;
		string spaces(maxLength - 11 - s.length(), ' ');
		cout << spaces << fiveasterisk << endl;
	}

	cout << line << endl;
}

void Contact::add() {
	ContactItem item;
	cout << "请输入名字：";
	cin >> item.name;
	cout << "请输入电话号码：";
	cin >> item.number;
	contact.push_back(item);
}

void Contact::show() {
	for (auto item : contact) {
		cout << "姓名：" << item.name << "，电话：" << item.number << endl;
	}
}

void Contact::del() {
	string name;
	cout << "请输入姓名：";
	cin >> name;

	for (vector<ContactItem>::iterator it = contact.begin(); it != contact.end(); it++) {
		if (it->name == name)
			it = contact.erase(it);
	}
	cout << "已删除 " << name << endl;
}

void Contact::clear() {
	contact.clear();
	cout << "已清空电话簿" << endl;
}

int Contact::find() {
	string name;
	cout << "请输入姓名：";
	cin >> name;

	for (vector<ContactItem>::size_type i = 0; i < contact.size(); i++) {
		ContactItem item = contact[i];
		if (item.name == name) {
			cout << "姓名：" << item.name << "，电话：" << item.number << endl;
			return i;
		}
	}

	return -1;
}

void Contact::modify() {
	int index = find();

	if (index == -1) {
		return;
	}

	ContactItem item = contact[index];

	string name;
	cout << "请输入姓名：";

	cin >> name;
	item.name = name;

	string number;
	cout << "请输入电话号码，为空则不更改：";
	cin >> number;

	item.number = number;

	cout << "已完成更改" << endl;
}

int main() {
	Contact contact;

	contact.process();
	return 0;
}