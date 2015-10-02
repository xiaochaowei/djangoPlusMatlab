function [cof_all,Xcal,X,cor_all] = Simu( X,E,LB,UB)
%使用基元模拟实际可燃固废
%   X为待拟合基元的TGA数据，E反应基元选取情况，选中为1，否则为0；LB,UB为选取的拟合区间上下界，cof为拟合系数，cor为区间上的关联度，cor_all为全局关联度

%*****************************************优化准备工作**********************************************
%data为系统数据，预置其中，为所有程序共用。其中包括basis_tga，为基元TGA数据
load DataTGA;
% load DataX;

%选取基元
k=0;
for i=1:10
if E(i)==1
k=k+1;%k的最终值等于选取的基元个数，即E（i)非0元素的个数
basis(:,k)=basis_tga(:,i);%从所有基元数据中提取出此次拟合需要用的数据
end
end

%横坐标
T=[100:1:1000]';


%*****************************************优化**********************************************

%优化目标函数f=norm(A*cof-b)的系数设置
global A;
global b;

%判断LB、UB的关系
if length(X)<950
    LB=LB-99;
    UB=UB-99;
end

A=basis(LB:UB,:);
b=X(LB:UB);

%设置优化标准型的各项参数
Aeq=ones(1,k);
beq=1;
VLB=zeros(k,1);   %解的范围为0~1
VUB=ones(k,1);
cof0=ones(k,1)/k;    %初始值

%优化
[cof,fval]=fmincon('OptGoalNorm',cof0,[],[],Aeq,beq,VLB,VUB);

%计算cof_all
cof_all=zeros(10,1);
m=0;
for i=1:10
if E(i)==1
m=m+1;
cof_all(i,1)=cof(m);
else
    cof_all(i,1)=0;
end
end

%全局拟合值
Xcal=basis*cof;
Lall=length(X);
%全局关联度
cor_all=Corr(X,Xcal,1,Lall);

%区间拟合值
bcal=A*cof;
%区间关联度
cor=Corr(X,Xcal,LB,UB);

%绘图
%  figure;
% plot(T,Xcal,'r',T,X,'b');