import faulthandler
import json
import os
import time

from env.socket_server import PrsEnv
import robot.baseline as baseline


TASK_FILE = os.path.join('task', 'dataset', 'deliver_task_test_set.json')
# TASK_ID = '3_2025_04_24T18_24_14_21_0_1'
TASK_ID = '9_2025_10_22T18_08_03_21_0_1'
# TASK_ID = '4_2025_05_15T11_57_23_6_0_0'

def main():
    with open(TASK_FILE, 'r') as file:
        task_data = json.load(file)

    task = task_data[TASK_ID]
    print('task:', TASK_ID)
    print('target object:', task['target_object_name'])
    print('npc:', task['npc_name'], '(id={})'.format(task['npc_id']))

    original_instruction_parsing = baseline.instruction_parsing
    original_lmm_interaction = baseline.lmm_interaction
    original_scene_understanding = baseline.scene_understanding

    def traced_instruction_parsing(instruction, description=None):
        print('[trace] instruction_parsing: start')
        result = original_instruction_parsing(instruction, description)
        print('[trace] instruction_parsing: result={}'.format(result))
        return result

    def traced_lmm_interaction(content, image):
        print('[trace] lmm_interaction: start image_shape={}'.format(image.shape))
        result = original_lmm_interaction(content, image)
        print('[trace] lmm_interaction: result={}'.format(result))
        return result

    def traced_scene_understanding(prs, target, surrounding=None, pitch=20, mode=0):
        print('[trace] scene_understanding: start target={} mode={}'.format(target, mode))
        result = original_scene_understanding(prs, target, surrounding, pitch, mode)
        print('[trace] scene_understanding: end found={}'.format(result[0] is not None))
        return result

    baseline.instruction_parsing = traced_instruction_parsing
    baseline.lmm_interaction = traced_lmm_interaction
    baseline.scene_understanding = traced_scene_understanding

    prs = PrsEnv(is_print=1, rendering=1, start_up_mode=1)
    baseline.prs = prs

    try:
        faulthandler.dump_traceback_later(30, repeat=True)
        print('[trace] delivery_task_import: start')
        instruction, npc_information, _ = prs.delivery_task_import(task)
        print('[trace] delivery_task_import: end')
        time.sleep(0.5)
        print('[trace] delivery_execution: start')
        baseline.delivery_execution(prs, instruction, npc_information)
        print('[trace] delivery_execution: end')
        result = prs.delivery_task_evaluate(task, score=1, save=0)
        print('task score:', result['task_score'])
        print('task result:', result)
    finally:
        faulthandler.cancel_dump_traceback_later()
        prs.finish_env()


if __name__ == '__main__':
    main()
