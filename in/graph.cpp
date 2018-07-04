#include<iostream>
#include<math.h>
#include"graph.hpp"
using namespace std;


//CGraph------------------
CGraph::CGraph(const char *m, double c, double s) : name(m), circum(c), square(s)
{
}
void CGraph::print()
{
//	cout<<"CGraph类的print函数被调用"<<endl;
	cout<<"图形是："<<name<<endl;
	cout<<"面积为："<<square<<endl;
	cout<<"周长为："<<circum<<endl<<endl;
}

//CCircle------------------
CCircle::CCircle(const char *m,double c, double s, double r) : CGraph(m,c,s), radius(r)
{
}
void CCircle::change(double r)
{
	radius=r;
}

void CCircle::print()
{
	square=3.1415926*radius*radius;
	circum=2*3.1415926*radius;
	CGraph::print();
}

//CRectangle-----------------
CRectangle::CRectangle(const char *m, double c, double s, double l, double w) : CGraph(m,c,s), width(w), length(l)
{}

void CRectangle::change(double l,double w)
{
		length=l;width=w;
}

void CRectangle::print()
{
	square=length*width;
	circum=2*(length+width);
	CGraph::print();
}


//CTriangle
CTriangle::CTriangle(const char *m,double c, double s, double A, double B, double C): CGraph(m,c,s), SideA(A), SideB(B), SideC(C)
{}

void CTriangle::change(double sideA,double sideB,double sideC)
{
	SideA=sideA; SideB=sideB;SideC=sideC;
}

void CTriangle::print()
{
	
	circum=SideA+SideB+SideC;
	int a=circum/2;
	square=sqrt( a*(a-SideA)*(a-SideB)*(a-SideC) );
	CGraph::print();
}
