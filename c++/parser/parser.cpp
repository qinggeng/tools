#include <boost/any.hpp>
#include <boost/function.hpp>
#include <vector>
#include <unordered_map>
struct Token
{
	typedef Token Self;
	private: String name_;
	public: String name() const{return name_;}
	public: Self& name(const String& val){if(name_ != val){name_ = val;} return *this;}
	private: String::const_iterator begin_;
	public: String::const_iterator begin() const{return begin_;}
	public: Self& begin(const String::const_iterator& val){begin_ = val; return *this;}
	private: String::const_iterator end_;
	public: String::const_iterator end() const{return end_;}
	public: Self& end(const String::const_iterator& val){end_ = val; return *this;}
	private: any value_;
	public: any value() const{return value_;}
	public: Self& value(const any& val){value_ = val; return *this;}
	Token(const String& tokenName):
		name_(tokenName)
	{
	}
	Token(const Token& rhs)
	{
		name_ = rhs.name_;
		begin_ = rhs.begin_;
		end_ = rhs.end_;
		value_ = rhs.value_;
	}
};
typedef vector<Token> Tokens;
typedef Tokens::const_iterator TokenIterator;
typedef function<void(Token)> TokenAction;
typedef function<void(void)> SemanticAction;
typedef vector<SemanticAction> SemanticActions;
typedef pair<bool, SemanticAction> ParsingResult;
typedef boost::function<ParsingResult (TokenIterator&, TokenIterator)>
	ParsingFunc;
typedef stack<any> ParsingStack;

void sequenceAction(
	const vector<function<void(void)> >& actions)
{
	for (vector<function<void(void)> >::const_iterator iter = actions.begin();
		 iter != actions.end();
		 iter++)
	{
		if (iter->empty())
		{
			continue;
		}
		(*iter)();
	}
}

ParsingResult sequenceParsing(const vector<ParsingFunc>& parsers, 
	TokenIterator& begin,
	TokenIterator end)
{
	TokenIterator current = begin;
	vector<function<void(void)> > actions;
	ParsingResult result;

	if (parsers.size() > end - begin)
	{
		return make_pair(false, SemanticAction());
	}
	for (vector<ParsingFunc>::const_iterator iter = parsers.begin();
		 iter != parsers.end();
		 iter++)
	{
		TokenIterator matchBegin = current;
		result = (*iter)(current, end);
		if (false == result.first)
		{
			return make_pair(false, SemanticAction());
		}
		actions.push_back(result.second);
	}
	begin = current;
	return make_pair(true, bind(sequenceAction, actions));
}

void chainedActions(SemanticAction prefix, SemanticAction infix, SemanticAction postfix)
{
	if (prefix)
	{
		prefix();
	}
	if (infix)
	{
		infix();
	}
	if (postfix)
	{
		postfix();
	}
}

SemanticAction linkActions(SemanticAction pre, SemanticAction in, SemanticAction post)
{
	return bind(chainedActions, pre, in ,post);
}

ParsingResult parsingWithAction(
	ParsingFunc parser, 
	SemanticAction pre,
	SemanticAction post,
	TokenIterator& begin, 
	TokenIterator& end)
{
	ParsingResult result = parser(begin, end);
	result.second = linkActions(pre, result.second, post);
	return result;
}

ParsingFunc attachSemanticAction(
	ParsingFunc parser, 
	SemanticAction pre,
	SemanticAction post)
{
	return bind(parsingWithAction, parser, pre, post, _1, _2);
}

ParsingResult selectParsing(const vector<ParsingFunc>& parsers, 
	TokenIterator& begin,
	TokenIterator end)
{
	TokenIterator matchedEnd = begin;
	ParsingResult result;
	result.first = false;
	for (vector<ParsingFunc>::const_iterator iter = parsers.begin();
		 iter != parsers.end();
		 iter++)
	{
		TokenIterator current = begin;
		ParsingResult tempResult = (*iter)(current, end);
		if (true == tempResult.first)
		{
			if (current > matchedEnd)
			{
				matchedEnd = current;
				result = tempResult;
			}
		}
	}
	begin = matchedEnd;
	return result;
}

ParsingFunc make_sequence(
	const ParsingFunc& p1,
	const ParsingFunc& p2)
{
	vector<ParsingFunc> parsers;
	parsers.push_back(p1);
	parsers.push_back(p2);
	return bind(sequenceParsing, parsers, _1, _2);
}

ParsingFunc make_sequence(
	const ParsingFunc& p1,
	const ParsingFunc& p2,
	const ParsingFunc& p3)
{
	vector<ParsingFunc> parsers;
	parsers.push_back(p1);
	parsers.push_back(p2);
	parsers.push_back(p3);
	return bind(sequenceParsing, parsers, _1, _2);
}


ParsingFunc make_select(
	const ParsingFunc& p1,
	const ParsingFunc& p2)
{
	vector<ParsingFunc> parsers;
	parsers.push_back(p1);
	parsers.push_back(p2);
	return bind(selectParsing, parsers, _1, _2);
}

ParsingFunc make_select(
	const ParsingFunc& p1,
	const ParsingFunc& p2,
	const ParsingFunc& p3)
{
	vector<ParsingFunc> parsers;
	parsers.push_back(p1);
	parsers.push_back(p2);
	parsers.push_back(p3);
	return bind(selectParsing, parsers, _1, _2);
}

ParsingFunc make_select(
	const ParsingFunc& p1,
	const ParsingFunc& p2,
	const ParsingFunc& p3,
	const ParsingFunc& p4)
{
	vector<ParsingFunc> parsers;
	parsers.push_back(p1);
	parsers.push_back(p2);
	parsers.push_back(p3);
	parsers.push_back(p4);
	return bind(selectParsing, parsers, _1, _2);
}

ParsingResult parseToken(Token token, TokenIterator& begin, TokenIterator& end, const TokenAction& action = TokenAction())
{
	if (begin >= end)
	{
		return make_pair(false, SemanticAction());
	}
	if (begin->name() != token.name())
	{
		return make_pair(false, SemanticAction());
	}
	const Token& theToken = *begin;
	++begin;
	if (action)
	{
		return make_pair(true, bind(action, theToken));
	}
	return make_pair(true, SemanticAction());
}

ParsingFunc make_token(Token token, const TokenAction& action = TokenAction())
{
	return bind(parseToken, token, _1, _2, action);
}

