function [theta]=subproblem3(k,p,q,d)
theta=[nan;nan];

pp=p-k'*p*k;
qp=q-k'*q*k;
dpsq=d^2-(k'*(p-q))^2;

if dpsq<0;return;end

if dpsq==0;
    theta(1)=subproblem1(k,pp/norm(pp),qp/norm(qp));
    theta(2)=theta(1);
    return;
end
  
bb=(norm(pp)^2+norm(qp)^2-dpsq)/(2*norm(pp)*norm(qp));
if abs(bb)>1;return;end

phi=acos(bb);

theta0=subproblem1(k,pp/norm(pp),qp/norm(qp));
theta=zeros(2,1);

theta(1)=theta0+phi;
theta(2)=theta0-phi;
