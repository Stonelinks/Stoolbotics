function [theta1,theta2]=subproblem2(k1,k2,p,q)

theta1=[nan;nan];theta2=[nan;nan];

k12=k1'*k2;
pk=p'*k2;
qk=q'*k1;

% check if solution exists

if abs(k12^2-1)<eps;return;end

a=[k12 -1;-1 k12]*[pk;qk]/(k12^2-1);

bb=(norm(p)^2-norm(a)^2-2*a(1)*a(2)*k12);
if abs(bb)<eps;bb=0;end
if bb<0;return;end

% check if there is only 1 solution
gamma=sqrt(bb)/norm(cross(k1,k2));
if abs(gamma)<eps;
  c1=[k1 k2 cross(k1,k2)]*[a;gamma];
  theta2(1)=subproblem1(k2,p,c1);theta2(2)=theta2(1);
  theta1=-subproblem1(k1,q,c1);theta1(2)=theta1(1);
end  

% general case: 2 solutions

theta1=zeros(2,1);
theta2=zeros(2,1);

c1=[k1 k2 cross(k1,k2)]*[a;gamma];
c2=[k1 k2 cross(k1,k2)]*[a;-gamma];
theta2(1)=subproblem1(k2,p,c1);
theta2(2)=subproblem1(k2,p,c2);

theta1(1)=-subproblem1(k1,q,c1);
theta1(2)=-subproblem1(k1,q,c2);
