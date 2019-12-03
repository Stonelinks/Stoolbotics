host = '127.0.0.1' % use 127.0.0.1 for localhost
port = 5005

p = zeros(3, 1)

for t = .01:1:1000
    p(1) = 40 + 15*cos(t);
    p(2) = 30;
    p(3) = 50 + 15*sin(t);
    
    q = omni_invkin(p);
    
    msg = strcat(num2str(q(1)), ',', num2str(q(2)), ',', num2str(q(3)));
    disp(msg)
    
    % send to stoolbotics
    judp('send', port, host, int8(msg));
end
