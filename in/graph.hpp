#ifndef __GRAPH_H__
#define __GRAPH_H__
#include <iostream>
using namespace std;


class CGraph
{
public:
	CGraph(const char *m="Graph", double c=0, double s=0);
	virtual void print();
protected:
	const char *name;
	double circum;
	double square;
private:
	int test2;
public:
	int test3;
};

class CCircle : public CGraph
{
public:
	CCircle(const char *m="Circle",double c=0, double s=0, double r = 0);
	void change(double r);//����Բ�İ뾶
	void print();
private:
	double radius;
};

class CRectangle : public CGraph
{
public:
	CRectangle(const char *m="Rectangle", double c=0, double s=0, double l =0, double w = 0);
	void change(double l,double w);//������εĳ��Ϳ�
	void print();
private:
	double length,width;
};

class CTriangle : public CGraph
{
public:
	CTriangle(const char *m="Triangle",double c=0, double s=0, double A = 0, double B=0, double C=0);
	void change(double sideA,double sideB,double sideC);//���������ε�������
	void print();
private:
	void test();
private:
	double SideA, SideB, SideC;
};

#endif
