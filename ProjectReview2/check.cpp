#include <iostream>
#include <string>
#include <stack>
#include <algorithm>
#include <sstream>
using namespace std;

struct Tag{
	int line_num;
	string tag;
};

string begin_variations[] = {
	"begn",
	"bein",
	"bgin",
	"egin",
	"begni",
	"beign",
	"bgein",
	"ebgin"
};

string end_variations[] = {
	"en",
	"ed",
	"nd",
	"edn",
	"ned"
};

bool is_begin_variation(const string&s){
	return find(begin(begin_variations), end(begin_variations), s) != end(begin_variations);
}

bool is_end_variation(const string&s){
	return find(begin(end_variations), end(end_variations), s) != end(end_variations);
}

int main(){

	int line_num = 1;
	try{
		stack<Tag>s;

		
		auto skip_spaces = [&]{
			while(isspace(cin.peek())){
				if(cin.peek() == '\n'){
					++line_num;
				}
				cin.ignore();
			}
		};

		auto read_word = []{
			string word;
			while(isalnum(cin.peek()) || cin.peek() == '*')
				word += cin.get();
			return word;
		};

		auto check_close_tag = [&](string close_tag){
			if(s.empty()){
				if(close_tag == "}")
					throw string("} has no corresponding {");
				else if(close_tag == "]")
					throw string("\\] has no corresponding \\[");
				else 
					throw string("\"\\end{"+close_tag+"}\" has no corresponding \"\\begin{"+close_tag+"}\"");
			} else {
				auto x = s.top();
				s.pop();

				string wanted_close_tag = x.tag;
				if(wanted_close_tag == "{")
					wanted_close_tag = "}";
				if(wanted_close_tag == "[")
					wanted_close_tag = "]";


				if(close_tag != wanted_close_tag){
					ostringstream out;
					out << "on line "<<x.line_num << " a ";
					if(x.tag == "{")
						out << '{';
					else if(x.tag == "[")
						out << "\\[";
					else if(x.tag == "$")
						out << "$";
					else if(x.tag == "$$")
						out << "$$";
					else
						out << "\"\\begin{"<<x.tag << "}\"";
					out << " was opened but has not yet been closed. The ";
					if(close_tag == "}")
						out << '}';
					else if(close_tag == "]")
						out << "\\]";
					else if(close_tag == "$")
						out << "$";
					else if(close_tag == "$$")
						out << "$$";
					else
						out << "\"\\end{"<<close_tag << "}\"";
					out << " does not fit.";

					int unclosed = 1;
					while(!s.empty()){
						x = s.top();
						s.pop();

						wanted_close_tag = x.tag;
						if(wanted_close_tag == "{")
							wanted_close_tag = "}";
						if(wanted_close_tag == "[")
							wanted_close_tag = "]";
					
						if(close_tag == wanted_close_tag){
							out << " A matching ";
							if(x.tag == "{")
								out << '{';
							else if(x.tag == "[")
								out << "\\[";
							else if(x.tag == "$")
								out << "$";
							else if(x.tag == "$$")
								out << "$$";
							else
								out << "\"\\begin{"<<x.tag << "}\"";
							out << " was opened on line "<<x.line_num <<" but ";
							if(unclosed == 1)
								out << "one parenthesis";
							else
								out << unclosed << " parentheses";
							out << " must be closed first.";
							throw string(out.str());
						}else
							++unclosed;
					}
					out << " No matching tag was open.";
					throw string(out.str());
				}
			}
		};

		char c;
		while(c = cin.get(), cin){
			if(c == '%'){
				while(c = cin.get(), cin)
					if(c == '\n')
						break;
				++line_num;
			} else if(c == '\n'){
				++line_num;
			} else if(c == '{'){
				s.push(Tag{line_num, "{"});
			} else if(c == '}'){
				check_close_tag("}");
			} else if(c == '$'){
				string tag = "$";
				if(cin.peek() == '$'){
					cin.ignore();
					tag = "$$";
				}
				if(!s.empty() && s.top().tag == tag)
					check_close_tag(tag);
				else
					s.push(Tag{line_num, tag});
			} else if(c == '\\'){
				if(cin.peek() == '['){
					cin.ignore();
					s.push(Tag{line_num, "["});
				}else if(cin.peek() == ']'){
					cin.ignore();
					check_close_tag("]");
				}else{
					string cmd = read_word();
					if(cmd == "begin"){
						skip_spaces();
						if(cin.get() != '{')
							throw ("\"\\begin\" must be followed by an {");
						string tag = read_word();
						if(cin.get() != '}')
							throw ("\"\\begin{"+tag+"\" must be followed by an }");
						s.push(Tag{line_num, tag});
					}else if(cmd == "end"){
						skip_spaces();
						if(cin.get() != '{')
							throw ("\"\\begin\" must be followed by an {");
						string tag = read_word();
						if(cin.get() != '}')
							throw ("\"\\begin{"+tag+"\" must be followed by an }");
						check_close_tag(tag);
					}else if(cmd == ""){
						// next character is escaped. For example \{. This is not parenthesis that we should check for.
						c = cin.get();
						if(c == '\n')
							++line_num;
					}else if(is_begin_variation(cmd)){
						cout << "Warning in line "<<line_num<<": You wrote \""<< cmd << "{\". Did you mean \"begin{\"?" << endl;
					}else if(is_end_variation(cmd)){
						cout << "Warning in line "<<line_num<<": You wrote \""<< cmd << "{\". Did you mean \"end{\"?" << endl;
					}
				}
			}
		}

		if(!s.empty()){
			ostringstream out;
			out << "not all parentheses were closed, still open are :";
			while(!s.empty()){
				out << '\n';
				auto x = s.top();
				s.pop();
				if(x.tag == "[" || x.tag == "{")
					out << x.tag;
				else
					out << "\"\\begin{"<<x.tag<<"}\"";
				out << " opened on line "<<x.line_num;
			}
			throw string(out.str());
		}
	}catch(string&msg){
		cout << "Error in line "<<line_num<<": " << msg << endl;
		return 1;
	}catch(exception&err){
		cerr << "Exception: "<<err.what() << endl;
		return 2;
	}
	return 0;
}


