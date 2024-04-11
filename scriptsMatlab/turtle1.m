% Cerrar ROS
rosshutdown;

% Iniciar ROS
rosinit;

% Crear un suscriptor para el tema de la pose de turtle1
poseSub = rossubscriber('/turtle1/pose', 'turtlesim/Pose');

% Capturar el último mensaje obtenido
latestPose = receive(poseSub, 1);

% Mostrar la posición y orientación del robot
disp('Última posición y orientación de turtle1:');
disp(['Posición (x, y, z): ', num2str([latestPose.X, latestPose.Y, 0])]); % Ignoramos Z ya que turtlesim/Pose no tiene Z
disp(['Orientación (theta): ', num2str(latestPose.Theta)]);

% Cerrar ROS
rosshutdown;
