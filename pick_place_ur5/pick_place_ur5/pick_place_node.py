import time

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray


class PickPlaceNode(Node):

    def __init__(self):
        super().__init__('pick_place_node')

        self.arm_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            10
        )

        self.gripper_pub = self.create_publisher(
            Float64MultiArray,
            '/gripper_controller/commands',
            10
        )

        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

    def move_arm(self, positions, point_name):
        msg = JointTrajectory()
        msg.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 4
        msg.points = [point]

        self.get_logger().info(f'Moviendo el brazo: {point_name}')
        self.arm_pub.publish(msg)
        time.sleep(5)

    def move_gripper(self, positions, action):
        msg = Float64MultiArray()
        msg.data = positions

        self.get_logger().info(f'Pinza: {action}')
        self.gripper_pub.publish(msg)
        time.sleep(2)

    def run_routine(self):
        self.get_logger().info('INICIO DE LA RUTINA PICK AND PLACE')

        # Punto 1: posición inicial
        self.move_arm(
            [0.0, -1.0, 1.2, -1.7, -1.57, 0.0],
            'Punto 1 - Posicion inicial'
        )

        # Punto 2: posición de recogida
        self.move_arm(
            [0.3, -0.8, 1.0, -1.7, -1.57, 0.0],
            'Punto 2 - Recogida del objeto'
        )
        self.move_gripper([0.004, 0.004], 'cierre solicitado')

        # Punto 3: posición de destino
        self.move_arm(
            [-0.3, -0.9, 1.1, -1.7, -1.57, 0.0],
            'Punto 3 - Destino del objeto'
        )
        self.move_gripper([0.04, 0.04], 'apertura solicitada')

        self.get_logger().info(
            'FIN DE LA RUTINA PICK AND PLACE'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceNode()

    try:
        # Esperar a que los controladores tengan suscriptores.
        for _ in range(10):
            if (node.arm_pub.get_subscription_count() > 0
                    and node.gripper_pub.get_subscription_count() > 0):
                break
            node.get_logger().info(
                'Esperando conexion con los controladores...'
            )
            time.sleep(1)

        if (node.arm_pub.get_subscription_count() == 0
                or node.gripper_pub.get_subscription_count() == 0):
            node.get_logger().error(
                'No se detectaron todos los controladores. '
                'Verifica que la simulacion siga ejecutandose.'
            )
        else:
            node.run_routine()

    except KeyboardInterrupt:
        node.get_logger().info('Rutina interrumpida por el usuario.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
