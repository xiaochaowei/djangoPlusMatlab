function [ cor ] = Corr( X1,X2,LB,UB)
%计算向量X1、X2在区域 LxH 上的灰色关联度
%   L为选取的区间，由上下界LB、UB确定；H为其各分量取值的上限，一般为100或1


%计算L
L=UB-LB+1;

%计算H
if X1(1)>50
    H=100;
else
    H=1;
end

X1t=X1(LB:UB);
X2t=X2(LB:UB);

%计算关联度
cor=1-norm((X1t-X2t),1)/L/H;
