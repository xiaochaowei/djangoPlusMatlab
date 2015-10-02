function [f]= OptGoalNorm(cof,A,b)
%优化目标函数
global A;
global b;
f=norm(A*cof-b);
