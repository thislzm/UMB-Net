import datetime
import os
import sys
import torch

def gpu_info(gpu_index):
    gpu_status = os.popen('nvidia-smi | grep %').read().split('\n')[gpu_index].split('|')
    power = int(gpu_status[1].split()[-3][:-1])
    memory = int(gpu_status[2].split('/')[0].strip()[:-3])
    return power, memory


def narrow_setup():
    gid = [0, 1, 2, 3, 4, 5]
    tag = True
    while tag:
        for gpu_id in gid:
            gpu_power, gpu_memory = gpu_info(gpu_id)
            gpu = 'gpu id:%d' % gpu_id
            gpu_power_str = 'gpu power:%d W |' % gpu_power
            gpu_memory_str = 'gpu memory:%d MiB |' % gpu_memory
            sys.stdout.write('\r' + gpu + ' ' + gpu_memory_str + ' ' + gpu_power_str + ' ')
            sys.stdout.flush()
            if gpu_memory < 2000:  # set waiting condition
                os.system(
                    'python train.py  --type 5 --gpus {} -train_batch_size 6 --restart'.format(gpu_id))
            if gpu_memory < 8000:  # set waiting condition
                os.system(
                    'python train.py --type 5  --gpus {} -train_batch_size 4 --restart'.format(
                        gpu_id))


if __name__ == '__main__':

    start_time = datetime.datetime(2022, 7, 10, 23, 0, 0)
    while True:
        sys.stdout.write('\r' + str(datetime.datetime.now()) + ' ')
        sys.stdout.flush()
        dtn = datetime.datetime.now()
        if dtn >= start_time:
            narrow_setup()
