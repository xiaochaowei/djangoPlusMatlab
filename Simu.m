function [cof_all,Xcal,X,cor_all] = Simu( X,E,LB,UB)
%ʹ�û�Ԫģ��ʵ�ʿ�ȼ�̷�
%   XΪ����ϻ�Ԫ��TGA���ݣ�E��Ӧ��Ԫѡȡ�����ѡ��Ϊ1������Ϊ0��LB,UBΪѡȡ������������½磬cofΪ���ϵ����corΪ�����ϵĹ����ȣ�cor_allΪȫ�ֹ�����

%*****************************************�Ż�׼������**********************************************
%dataΪϵͳ���ݣ�Ԥ�����У�Ϊ���г����á����а���basis_tga��Ϊ��ԪTGA����
load DataTGA;
% load DataX;

%ѡȡ��Ԫ
k=0;
for i=1:10
if E(i)==1
k=k+1;%k������ֵ����ѡȡ�Ļ�Ԫ��������E��i)��0Ԫ�صĸ���
basis(:,k)=basis_tga(:,i);%�����л�Ԫ��������ȡ���˴������Ҫ�õ�����
end
end

%������
T=[100:1:1000]';


%*****************************************�Ż�**********************************************

%�Ż�Ŀ�꺯��f=norm(A*cof-b)��ϵ������
global A;
global b;

%�ж�LB��UB�Ĺ�ϵ
if length(X)<950
    LB=LB-99;
    UB=UB-99;
end

A=basis(LB:UB,:);
b=X(LB:UB);

%�����Ż���׼�͵ĸ������
Aeq=ones(1,k);
beq=1;
VLB=zeros(k,1);   %��ķ�ΧΪ0~1
VUB=ones(k,1);
cof0=ones(k,1)/k;    %��ʼֵ

%�Ż�
[cof,fval]=fmincon('OptGoalNorm',cof0,[],[],Aeq,beq,VLB,VUB);

%����cof_all
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

%ȫ�����ֵ
Xcal=basis*cof;
Lall=length(X);
%ȫ�ֹ�����
cor_all=Corr(X,Xcal,1,Lall);

%�������ֵ
bcal=A*cof;
%���������
cor=Corr(X,Xcal,LB,UB);

%��ͼ
%  figure;
% plot(T,Xcal,'r',T,X,'b');