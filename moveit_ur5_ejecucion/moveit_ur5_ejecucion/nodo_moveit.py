import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint
from action_msgs.msg import GoalStatus


def main(args=None):
    rclpy.init(args=args)
    node = Node('nodo_moveit_ur5')
    client = ActionClient(node, MoveGroup, '/move_action')

    try:
        if not client.wait_for_server(timeout_sec=20.0):
            node.get_logger().error(
                'No se encontro el servidor MoveIt'
            )
            return

        joints = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

        objetivo = [
            0.35, -1.0, 1.2,
            -1.7, -1.57, 0.0
        ]

        restricciones = Constraints()
        restricciones.name = 'objetivo_ur5'

        for nombre, posicion in zip(joints, objetivo):
            restriccion = JointConstraint()
            restriccion.joint_name = nombre
            restriccion.position = posicion
            restriccion.tolerance_above = 0.02
            restriccion.tolerance_below = 0.02
            restriccion.weight = 1.0
            restricciones.joint_constraints.append(restriccion)

        goal = MoveGroup.Goal()
        goal.request.group_name = 'ur5_arm'
        goal.request.goal_constraints = [restricciones]
        goal.request.start_state.is_diff = True
        goal.request.num_planning_attempts = 5
        goal.request.allowed_planning_time = 15.0
        goal.request.max_velocity_scaling_factor = 0.15
        goal.request.max_acceleration_scaling_factor = 0.15

        # False significa planificar Y ejecutar
        goal.planning_options.plan_only = False
        goal.planning_options.planning_scene_diff.is_diff = True
        goal.planning_options.planning_scene_diff.robot_state.is_diff = True

        node.get_logger().info(
            'Solicitando planificacion y ejecucion con MoveIt'
        )

        futuro = client.send_goal_async(goal)
        rclpy.spin_until_future_complete(
            node, futuro, timeout_sec=25.0
        )

        if not futuro.done() or not futuro.result().accepted:
            node.get_logger().error('Objetivo rechazado')
            return

        resultado_futuro = futuro.result().get_result_async()
        rclpy.spin_until_future_complete(
            node, resultado_futuro, timeout_sec=120.0
        )

        if not resultado_futuro.done():
            node.get_logger().error('Tiempo de espera agotado')
            return

        resultado = resultado_futuro.result()
        codigo = resultado.result.error_code.val

        if (resultado.status == GoalStatus.STATUS_SUCCEEDED
                and codigo == 1):
            node.get_logger().info(
                'TRAYECTORIA EJECUTADA CORRECTAMENTE CON MOVEIT'
            )
        else:
            node.get_logger().error(
                f'Ejecucion no completada. Codigo MoveIt: {codigo}'
            )

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
