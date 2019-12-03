function [theta]=subproblem1(k,p,q)

theta=nan;
tol=1e-2;
if (abs(norm(p)-norm(q))>tol);return;end
if norm(p-q)<sqrt(eps);theta=0;return;end
  
k=k/norm(k);
pp=p-(p'*k)*k;
qp=q-(q'*k)*k;

epp=pp/norm(pp);
eqp=qp/norm(qp);

theta=subproblem0(epp,eqp,k);
%theta=atan2(k'*(cross(epp,eqp)),epp'*eqp);
