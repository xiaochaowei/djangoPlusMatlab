function [f]= OptGoalNorm(cof,A,b)
%�Ż�Ŀ�꺯��
global A;
global b;
f=norm(A*cof-b);
