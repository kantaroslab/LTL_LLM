from utils.ltl.buchi_parse import Buchi
import random


def get_next_subtasks(config, buchi, currentNBAState, acceptingNBAState):
    nextNBAState = buchi.get_next_NBA_state(currentNBAState, acceptingNBAState)
    nextAction = buchi.get_next_action(currentNBAState, nextNBAState)
    ok_Action = [k for (k, v) in nextAction.items() if v is True]
    if len(ok_Action) == 0:
        return None, nextNBAState
    else:
        if len(ok_Action) == 1:
            sub_task = config['LTL']['detail'][ok_Action[0]]
        else:
            sub_task, _ = random.choice(ok_Action)
        return sub_task, nextNBAState
    

class LTLTask(object):
    def __init__(self, config):
        self.formula = config['LTL']['formula']
        self.subformula = {}
        k = 1
        for key, value in config['LTL']['detail'].items():
            self.subformula[k] = ['(' + key + ')', 1, 1]
            k += 1
        self.number_of_robots = 1


def create_buchi_upon_task(myconfig):
    task = LTLTask(myconfig)
    # print("[SYSTEM] Overall Command: {}\n[SYSTEM] Sub-tasks: {}".format(task.formula, task.subformula))
    print(f"[SYS] LTL Formula: {task.formula}")

    buchi = Buchi(task)
    buchi.construct_buchi_graph()
    buchi.get_minimal_length()
    buchi.get_feasible_accepting_state()
    acceptingNBAState = buchi.buchi_graph.graph['accept'][0]
    currentNBAState = buchi.buchi_graph.graph['init'][0]
    return task, buchi, currentNBAState, acceptingNBAState


def task_analyzer(task):
    room_num = task.split('l')[1].split('_')[0]
    return room_num


def multi_robot_task_analyzer(task):
    room_num = task.split('l')[1].split('_')[0]
    robot_num = task.split('_')[1]
    return robot_num, room_num
