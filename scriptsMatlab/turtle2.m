% Cerrar ROS
rosshutdown;
% Iniciar ROS
rosinit;

% Crear un cliente para el servicio de teleportación absoluta de turtle1
teleportClient = rossvcclient('/turtle1/teleport_absolute');

% Crear una solicitud de servicio para teleportar a una nueva posición y orientación
teleportRequest = rosmessage(teleportClient);

% Establecer la nueva posición y orientación
teleportRequest.X = 8; % Nueva posición en el eje X
teleportRequest.Y = 10; % Nueva posición en el eje Y
teleportRequest.Theta = pi/4; % Nueva orientación en radianes (90 grados)

% Enviar la solicitud de servicio
teleportResponse = call(teleportClient, teleportRequest);


% Cerrar ROS
rosshutdown;
