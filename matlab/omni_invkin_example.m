host = '129.161.33.176' % localhost
port = 5005

p = zeros(3, 1)

for t = .01:1:1000
    p(1) = 10;
    p(2) = t;
    p(3) = 10;
    
    q = omni_invkin(p);
    
    msg = strcat(num2str(q(1)), ',', num2str(q(2)), ',', num2str(q(3)));
    disp(msg)
    
    % send to stoolbotics
    judp('send', port, host, int8(msg));
    pause(.1);
end
