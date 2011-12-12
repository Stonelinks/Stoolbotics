function [theta]=subproblem0(p,q,k)

theta=nan;
if ((k'*p)>sqrt(eps)|(k'*q)>sqrt(eps))
  return;
end

ep=p/norm(p);
eq=q/norm(q);

theta=2*atan2(norm(ep-eq),norm(ep+eq));

if k'*(cross(p,q))<0
  theta=-theta;
end
