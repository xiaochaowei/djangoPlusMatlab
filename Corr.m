function [ cor ] = Corr( X1,X2,LB,UB)
%��������X1��X2������ LxH �ϵĻ�ɫ������
%   LΪѡȡ�����䣬�����½�LB��UBȷ����HΪ�������ȡֵ�����ޣ�һ��Ϊ100��1


%����L
L=UB-LB+1;

%����H
if X1(1)>50
    H=100;
else
    H=1;
end

X1t=X1(LB:UB);
X2t=X2(LB:UB);

%���������
cor=1-norm((X1t-X2t),1)/L/H;
