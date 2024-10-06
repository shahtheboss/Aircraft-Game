y=x^2;
for i = 1:length(y)
  figure(1)    
    if i ~=length(y)        
        plot(1:i,y(1,1:i),'-b');      
    else
        plot(1:i,y(1,1:i),'-b*')
    end
    if i>=50
        axis([i-50 i+50 min(y(1,:)) max(y(1,:))])
    else
        axis([0 i+50 min(y(1,:)) max(y(1,:))])
    end
 %pause(0.1)
    drawnow
end