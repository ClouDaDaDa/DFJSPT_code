import copy
from DFJSPT.dfjspt_env import DfjsptMaEnv
from DFJSPT import dfjspt_params
import numpy as np
import time
import json

from DFJSPT.dfjspt_rule.job_selection_rules import job_SPT_action
from DFJSPT.dfjspt_rule.machine_selection_rules import machine_SPT_action, transbot_SPT_action


def rule6_mean_makespan(
    instance_id,
    train_or_eval_or_test=None,
):

    config = {
        "train_or_eval_or_test": train_or_eval_or_test,
    }
    env = DfjsptMaEnv(config)
    makespan_list = []
    for _ in range(100):
        observation, info = env.reset(options={
            "instance_id": instance_id,
        })
        # env.render()
        done = False
        count = 0
        stage = next(iter(info["agent0"].values()), None)
        total_reward = 0

        while not done:
            if stage == 0:
                legal_job_actions = copy.deepcopy(observation["agent0"]["action_mask"])
                real_job_attrs = copy.deepcopy(observation["agent0"]["observation"])

                SPT_job_action = job_SPT_action(legal_job_actions=legal_job_actions, real_job_attrs=real_job_attrs)
                observation, reward, terminated, truncated, info = env.step(SPT_job_action)
                stage = next(iter(info["agent1"].values()), None)

            elif stage == 1:
                legal_machine_actions = copy.deepcopy(observation["agent1"]["action_mask"])
                real_machine_attrs = copy.deepcopy(observation["agent1"]["observation"])

                SPT_machine_action = machine_SPT_action(legal_machine_actions=legal_machine_actions,
                                                        real_machine_attrs=real_machine_attrs)
                observation, reward, terminated, truncated, info = env.step(SPT_machine_action)
                stage = next(iter(info["agent2"].values()), None)

            else:
                legal_transbot_actions = copy.deepcopy(observation["agent2"]["action_mask"])
                real_transbot_attrs = copy.deepcopy(observation["agent2"]["observation"])

                SPT_transbot_action = transbot_SPT_action(
                    legal_transbot_actions=legal_transbot_actions,
                    real_transbot_attrs=real_transbot_attrs)
                observation, reward, terminated, truncated, info = env.step(SPT_transbot_action)
                stage = next(iter(info["agent0"].values()), None)
                done = terminated["__all__"]
                count += 1
                total_reward += reward["agent0"]

        make_span = env.final_makespan
        makespan_list.append(make_span)
    mean_makespan = np.mean(makespan_list)
    return makespan_list, mean_makespan



def rule6_single_makespan(
    instance_id,
    train_or_eval_or_test=None,
):

    config = {
        "train_or_eval_or_test": train_or_eval_or_test,
    }
    env = DfjsptMaEnv(config)

    observation, info = env.reset(options={
        "instance_id": instance_id,
    })
    # env.render()
    done = False
    count = 0
    stage = next(iter(info["agent0"].values()), None)
    total_reward = 0

    while not done:
        if stage == 0:
            legal_job_actions = copy.deepcopy(observation["agent0"]["action_mask"])
            real_job_attrs = copy.deepcopy(observation["agent0"]["observation"])

            SPT_job_action = job_SPT_action(legal_job_actions=legal_job_actions, real_job_attrs=real_job_attrs)
            observation, reward, terminated, truncated, info = env.step(SPT_job_action)
            stage = next(iter(info["agent1"].values()), None)

        elif stage == 1:
            legal_machine_actions = copy.deepcopy(observation["agent1"]["action_mask"])
            real_machine_attrs = copy.deepcopy(observation["agent1"]["observation"])

            SPT_machine_action = machine_SPT_action(legal_machine_actions=legal_machine_actions,
                                                    real_machine_attrs=real_machine_attrs)
            observation, reward, terminated, truncated, info = env.step(SPT_machine_action)
            stage = next(iter(info["agent2"].values()), None)

        else:
            legal_transbot_actions = copy.deepcopy(observation["agent2"]["action_mask"])
            real_transbot_attrs = copy.deepcopy(observation["agent2"]["observation"])

            SPT_transbot_action = transbot_SPT_action(
                legal_transbot_actions=legal_transbot_actions,
                real_transbot_attrs=real_transbot_attrs)
            observation, reward, terminated, truncated, info = env.step(SPT_transbot_action)
            stage = next(iter(info["agent0"].values()), None)
            done = terminated["__all__"]
            count += 1
            total_reward += reward["agent0"]

    make_span = env.final_makespan
    # env.render()
    # time.sleep(10)

    return make_span



if __name__ == '__main__':
    import os
    folder_name = os.path.dirname(os.path.dirname(__file__)) + "/dfjspt_data/pool_J" + str(dfjspt_params.max_n_jobs) + "_M" + str(dfjspt_params.n_machines) + "_T" + str(dfjspt_params.n_transbots)
    pool_name = folder_name + "/instance" + str(dfjspt_params.n_instances)
    with open(pool_name, "r") as fp:
        loaded_pool = json.load(fp)


    rule_makespan_results = []
    time_0 = time.time()
    for i in range(dfjspt_params.n_instances):
        makespan_i = rule6_single_makespan(
            loaded_pool,
            i,
            i + 1,
        )
        rule_makespan_results.append(makespan_i)
        print(f"Makespan of instance {i} = {makespan_i}.")
    time_1 = time.time()
    total_time = time_1 - time_0
    print(f"Total time = {total_time}.")
    print(f"Average running time per instance = {total_time / dfjspt_params.n_instances}")
    average = 0 if not rule_makespan_results else (sum(rule_makespan_results) / len(rule_makespan_results))
    print(f"Average makespan = {average}.")

    rule_makespan_results_name = folder_name + "/RuleMakespan_Omax" + str(dfjspt_params.max_n_operations) + "_Omin" + str(
        dfjspt_params.min_n_operations) + "_Instance" + str(dfjspt_params.n_instances)

    with open(rule_makespan_results_name, "w") as fp:
        json.dump(rule_makespan_results, fp)
