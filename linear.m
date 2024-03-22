clc;clear;close all
load analysis/mat_data.mat
data=cell2mat(d_data);
t=tfit;
m=size(t');
out='x';  %研究对象选择，可选x 、y

if out=='x'
    xl=[data(:,1) data(:,3) data(:,2)];
else
    xl=data;
end

x=xl(:,1:2);
y=xl(:,3);
X=[ones(m) x];
%% 
b1=regress(y,X);
yy=X*b1;
S=var(y);U=var(yy-mean(y));R2=U/S;
plot(t,xl(:,3),'-',t,yy,'-.')
xlabel('距离首时刻时间差/s','fontsize',14)
title([out,'方向风矢量','线性回归分析对比图'],'fontsize',14)
legend('实际曲线','回归曲线')
str=['y=',num2str(b1(1)),'+',num2str(b1(2)),'x1','+',num2str(b1(3)),'x2'];
text(t(500),0.15,str);
text(t(500),0.11,['R2=',num2str(R2)]);
box off
%% 
a=abs(yy-y);
b=(yy-y).^2;
not_z=find(y~=0);
z=find(y==0);
y_noz=y(not_z);
yy_noz=yy(not_z);
c=abs((yy_noz-y_noz)./y_noz);
d=2*abs((yy-y))./(abs(y)+abs(yy));

MSE=mean(b);
RMSE=sqrt(MSE);
MAE=mean(a);
MAPE=mean(c)*100;
SMAPE=mean(d)*100;
c_name={'MSE','RMSE','MAE','R2','MAPE ','SMAPE '};
txt_list=[MSE,RMSE,MAE,R2,MAPE,SMAPE];

fid=fopen(['analysis\',out,'-linear.txt'],'w');
fprintf(fid,[out,'-Linear\r\n']); 
fprintf(fid,'b= ' ); 
for jj=1:length(b1)
    fprintf(fid,'%.6f  ',b1(jj)); 
end
fprintf(fid,'\r\n' ); 

for jj=1:length(txt_list)
    fprintf(fid,[char(c_name(jj)),': ']); 
    if jj>4
        fprintf(fid,'%.4f  %%\r\n',txt_list(jj)); 

    else
        fprintf(fid,'%.4f\r\n',txt_list(jj)); 
    end
end
fclose(fid);



