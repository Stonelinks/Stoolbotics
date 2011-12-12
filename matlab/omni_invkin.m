function q = omni_invkin(p)
q=zeros(3,1);
l1=50;l2=50;l3=50;


x=[1;0;0];y=[0;1;0];z=[0;0;1];

theta3=subproblem3(y,l3*z,-l2*x,norm(p-l1*z));
q(3) = theta3(1);

[theta1,theta2]=subproblem2(z,y,-l2*x-rot(y,q(3))*l3*z,p-l1*z);

q(2) = theta2(1);
q(1) = theta1(1);
