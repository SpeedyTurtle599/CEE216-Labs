% Benjamin Coveler
% 27 April 2023
% CEE 216 Lab 2

clear
close all

% Define shared properties of elements
A = 250; % mm^2
L = 150; % mm
E = 2.0e4; % N/mm^2

% Define load and displacement
P = 6.0e4; % N
delta = 1.2; % mm

% Define number of elements and nodes
elements = 2;
nodes = 3;

% Request user for load at each node (for test case, only requests 1)
% Subtract 2 to get the initial position at the first element 
% (arrays start at 1 in MATLAB)
% P matrix is for loads
for i = 1:nodes-2
      P(1, i+2) = input(sprintf('Load at node %d: ', i+2));
end

% Transpose load matrix to vertical orientation for later
P = P';

% Construct connectivity table
for i = 1:elements
      % If counter is 1, then manually assign according to notes
      % nomenclature system (3 is second item)
      if i == 1
            iNode(i) = 1;
            jNode(i) = 3;
      % If counter is at end of count, manually assign according to notes
      elseif i == elements
            iNode(i) = nodes;
            jNode(i) = 2;
      % Else, use pattern of 1 ahead for i and 2 ahead for j
      else
            iNode(i) = i+1;
            jNode(i) = i+2;
      end
end

% Create local stiffness matrix. All values of k will have to be 
% the same, since we are only taking in one value for E, A, and L
% k = (E*A/L) * [1, -1; -1,1];

matrix = [1, -1; -1,1];
for i = 1:elements
      coeff = (E*A)/L;
      k{i} = coeff.*matrix;
end

% Create global stiffness matrix by inserting values of k
% Initialise the global K matrix
K = zeros(nodes);
% Double loop through node count, to create node x node dimension matrix
for i = 1:nodes
      for j = 1:nodes
            if i == j
                  % Funny business so we can copy nomenclature from notes
                  % (less confusing for handwritten solution)
                  if i > 2 && j > 2
                        K(i,j) = k{1}(iNode(1))+k{2}(iNode(1));
                  else
                        K(i,j) = k{1}(iNode(1));
                  end
            % Elseif two conditions - OR (one, but not both, conditions)
            elseif j == nodes || i == nodes
                  K(i,j) = k{1}(jNode(1));
             % If none of these conditions fit, leave entry as 0
            end
      end
end

% Initialise displacements vector
% Manually set displacement as gap (def of static indeterminate problem)
u = zeros(nodes, 1);
u(2) = delta;

% Calculate displacements for all items using backslash operator
% to solve system without having to invert (AIA' method)
% Start at 3, because 1 and 2 are already known (u1 = 0, u2 = delta)
% Run to end in case matrix is larger than 3 elements
u(3:end) = K(3:end, 3:end) \ (P(3:end) - delta.*K(3:end, 2));

% Use equation F = K * u, with K as the global stiffness
P(1:2) = K(1:2,:)*u;

% Calculate stresses at every element using for-loop
% Hooke's Law: sigma = E * eps, eps = displacement/L
for i = 1:elements
      % epsilon = uB - uA / L
      stress(i) = (u(jNode(i)) - u(iNode(i))) * E/L;
end
