#include<iostream>
#include "graph.hpp"

using namespace std;

int main()
{
	CCircle c;
	c.change(1);
	c.print();

	CRectangle R;
	R.change(1,2);
	R.print();

	CTriangle T;
	T.change(3,4,5);
	T.print();

	return 0;
}
