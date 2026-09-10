from env.socket_server import PrsEnv
import time

if __name__ == "__main__":

    # Environment initialization
    prs = PrsEnv(
        is_print=1,
        rendering=1,
        start_up_mode=0   # Windows 手动启动 Unity
    )

    print("Connected!")

    # 保留官方 demo 的执行顺序
    prs.npc_start(5)
    print("NPCs started!")

    result_init = prs.agent.initial_pose()
    print("Initial pose result:", result_init)

    result_nav = prs.agent.go_to_destination(
        tar_location='kitchen'
    )
    print("Navigation result:", result_nav)

    result_rotate = prs.agent.rotate_right(
        degree=-30
    )
    print("Rotate result:", result_rotate)

    print("Test finished, waiting...")
    time.sleep(10)

    prs.finish_env()