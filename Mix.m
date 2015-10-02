function [ Xlin,Xnon ] = Mix( cof )
cof = cof';
%计算基元混合反应特性
%   cof为基元比例,Xlin为线性模型计算结果，Xnon为非线性计算结果

%*********************************加载所需数据***************************
%其中包括基元数据basis_mtga,14组混合反应数据mix2basis_mtga （：，：，14），包括hemicellu_PS,
%hemicellu_PET,hemicellu_PP,hemicellu_PE,lignin_PS,lignin_PET,lignin_PP,lignin_PE,
%PVC_cellu,PVC_PS,PVC_PET,cellu_PET,cellu_PP,cellu_PE
load DataMacroTGA;
% load datacof;

t=[1:1:2500];
%*********************************线性模型*******************************
Xlin=basis_mtga*cof;

%*********************************非线性模型***************************
%非线性模型在线性模型基础上进行修正，Xnon=Xlin+e。e为修正值，计算的基本思路是先将多组分混合反应拆解为
%若干组双组分混合反应，计算每个双组分混合反应修正值，以其加权值作为最终结果的修正值。

%*********************************计算分配系数***************************
%以非线性规划的方式解方程，求X
global B;
B=cof;

%设置非线性规划的参数
A=[];
b=[];
Aeq=ones(1,28);
beq=1;
VLB=zeros(28,1);   %解C的范围为0~1
VUB=ones(28,1);
%设置初值
X0=zeros(28,1);
for i=1:4
    X0(i)=B(1)/4;
end
for i=5:8
    X0(i)=B(2)/3;
end
for i=9:11
    X0(i)=B(3)/3;
end
for i=12:15
    X0(i)=B(5)/4;
end
for i=16:18
    X0(i)=B(6)/3;
end
for i=19:22
    X0(i)=B(7)/4;
end
for i=23:25
    X0(i)=B(8)/3;
end
for i=26:28
    X0(i)=B(9)/3;
end

[x,fval,exitflag]=fmincon('OptGoalCof',X0,A,b,Aeq,beq,VLB,VUB);

% 算系数
%m为每个混合反应所占比重
m=zeros(14,1);
%n为每个混合反应中两种物质中后一种（稳定）物质的比重
n=zeros(14,1);

m(1)=x(1)+x(16);n(1)=x(16)/m(1);
m(2)=x(2)+x(19);n(2)=x(19)/m(2);
m(3)=x(3)+x(23);n(3)=x(23)/m(3);
m(4)=x(4)+x(26);n(4)=x(26)/m(4);
m(5)=x(5)+x(17);n(5)=x(17)/m(5);
m(6)=x(6)+x(20);n(6)=x(20)/m(6);
m(7)=x(7)+x(24);n(7)=x(24)/m(7);
m(8)=x(8)+x(27);n(8)=x(27)/m(8);
m(9)=x(9)+x(12);n(9)=x(12)/m(9);
m(10)=x(10)+x(18);n(10)=x(18)/m(10);
m(11)=x(11)+x(21);n(11)=x(21)/m(11);
m(12)=x(13)+x(22);n(12)=x(22)/m(12);
m(13)=x(14)+x(25);n(13)=x(25)/m(13);
m(14)=x(15)+x(28);n(14)=x(28)/m(14);

%*********************************计算每个双组分反应的修正值***************************
for k=1:14
    temp=mix2basis_mtga(:,:,k);
    if n(k)>0.8
    e(:,k)=(1-n(k))*temp(:,1);
    else if ((n(k)>0.6)&&(n(k)<=0.8))
            e(:,k)=(n(k)-0.6)*temp(:,1)+(0.8-n(k))*temp(:,2);
        else if ((n(k)>0.5)&&(n(k)<=0.6))
                e(:,k)=(n(k)-0.5)*temp(:,2)+(0.6-n(k))*temp(:,3);
            else if ((n(k)>0.4)&&(n(k)<=0.5))
                    e(:,k)=(n(k)-0.4)*temp(:,3)+(0.5-n(k))*temp(:,4);
                else if ((n(k)>0.2)&&(n(k)<=0.4))
                        e(:,k)=(n(k)-0.2)*temp(:,4)+(0.4-n(k))*temp(:,5);
                    else if n(k)<=0.2
                            e(:,k)=n(k)*temp(:,5);
                        end
                    end
                end
            end
        end
    end
end

%计算修正值
esum=zeros(2500,1);
for k=1:14
esum=esum+e(:,k);
end

Xnon=Xlin+esum;




