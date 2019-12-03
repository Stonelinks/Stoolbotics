function R=rot(k,th)

R=eye(3,3)+ sin(th)*hat(k) + (1-cos(th))*hat(k)*hat(k);
