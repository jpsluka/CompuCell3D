#!/usr/bin/env python

# TODO add discovery of free port - zmw have a fcn that facilitates it (port range is given )
# port_selected = socket.bind_to_random_port('tcp://*', min_port=6001, max_port=6004, max_tries=100)
#


import numpy as np
from OptimizerWorkerProcessZMQ import OptimizerWorkerProcessZMQ
from template_utils import generate_simulation_files_from_template
from collections import OrderedDict
import os
from os.path import *
import datetime
import time
import json
import random

import time
import zmq
import argparse
import sys
import json
import numpy as np

from cma import CMAEvolutionStrategy


class OptimizationCMLParser(object):
    def __init__(self, arg_count_threshold=1):
        self.parser = argparse.ArgumentParser(description='CMA Optimization')
        self.parser.add_argument('-i', '--input', required=True, action='store', help="cc3d simulation project")
        self.parser.add_argument('-p', '--params-file', required=True, action='store', default='',
                                 help="json parameter file")
        self.parser.add_argument('-n', '--num-workers', required=False, action='store', default=1, type=int,
                                 help="number of workers")

        self.parser.add_argument('-r', '--cc3d-run-script', required=True, action='store',help="CC3D run script")


        self.parser.add_argument('--clean-workdirs', dest='clean_workdirs', action='store_true',
                                 help='clean temporary simulation output')
        self.parser.add_argument('--no-clean-workdirs', dest='clean_workdirs', action='store_false',
                                 help='do not clean temporary simulation output')
        self.parser.set_defaults(clean_workdirs=True)

        # self.parser.add_argument('-c', '--clean-workdirs', required=False, action='store', default=1, type=bool)

        self.arg_list = []
        self.arg_count_threshold = arg_count_threshold

    def arg(self, name, *vals):
        self.arg_list.append(name)
        for val in vals:
            self.arg_list.append(val)

    def configure_python_paths(self, paths):
        for path in paths:
            sys.path.append(path)

    def parse(self):
        print sys.argv
        if len(sys.argv) <= self.arg_count_threshold and len(self.arg_list):
            args = self.parser.parse_args(self.arg_list)
        else:
            args = self.parser.parse_args()

        return args


class OptimizationParameterManager(object):
    def __init__(self):
        self.params_jn = None
        self.parameters = None
        self._params_names = []
        self._std_dev = 0.5
        self._default_bounds = np.array([0., 1.], dtype=np.float)

    def parse(self, fname):
        """
        Parses optimization parameters json file
        :param fname: name of the file with definition of optimization parameters
        :return: None
        """
        self.params_jn = json.load(open(fname, 'r'))
        self.parameters = self.params_jn['parameters']
        self._params_names = self.parameters.keys()
        try:
            self._std_dev = self.params_jn['std_dev']
        except:
            print 'Could not find "std_dev" in %s. Will use default value of %f ' % (fname, self.std_dev)

        self.params_bounds = np.zeros((len(self._params_names), 2), dtype=np.float)

        for i, name in enumerate(self._params_names):
            self.params_bounds[i, :] = self.parameters[name]

            # vec = np.array([0.5,0.5])
            # true_params = self.params_from_0_1(vec)
            #
            # true_params_dict = self.param_from_0_1_dict(vec)
            # print 'true_params_dict=',true_params_dict
            #
            print

    @property
    def params_names(self):
        return self._params_names

    @property
    def default_bounds(self):
        return self._default_bounds

    @property
    def std_dev(self):
        return self._std_dev

    def get_starting_points(self):
        """
        Returns starting point for the optimization run by picking "center" fo the parameter hyperspace
        :return: {ndarray} vector describing the "center" of the parameter hyperspace
        """
        return 0.5 * np.ones(len(self._params_names), dtype=np.float)

    def params_from_0_1(self, param_vec_0_1):
        """
        Remaps vector of parameters from [0,1] interval to the true interval
        :param param_vec_0_1: {ndarray} - vector of paramters mapped to [0,1] interval
        :return: {ndarray} - vector of parameters mapped from [0,1] to true range
        """
        return self.params_bounds[:, 0] + param_vec_0_1 * (self.params_bounds[:, 1] - self.params_bounds[:, 0])

    def param_from_0_1_dict(self, param_vec_0_1):
        """
        generates a dictionary of "true" parameters (i.e. remapped from [0,1] range). Dictionary labels are
        parameters names as specified in the parameters json file and in the xml or python simulation templates.
        This dictionary will be sent to workers so that they can to proper substitution in the simulation files - replacing
        paremeter name labels with actual parameter numbers
        :param param_vec_0_1: {ndarray } - vector of parameters mapped to [0,1]
        :return: {dict} - the format is {parameter_name:value}
        """
        return dict(zip(self._params_names, self.params_from_0_1(param_vec_0_1)))


class Optimizer(object):
    def __init__(self):
        # self.param_set_list = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.param_set_list = [1, 2, 3, 4, 5]
        self.context = zmq.Context()
        self.push_address_str = "tcp://127.0.0.1:5557"
        self.pull_address_str = "tcp://127.0.0.1:5558"

        #
        # dictionary that specifies all the information that worker neeeds to run simulation
        # with a given set of parameters (accessible using 'param_dict' of the workload_dict)
        self.workload_dict = None

        #
        # INstance of OptimizationParameterManager
        self.optim_param_mgr = None

        #
        # parsed command line arguments
        self.parse_args = None

        self.zmq_socket = self.context.socket(zmq.PUSH)
        self.zmq_socket.bind(self.push_address_str)
        self.num_workers = 1

    def acknowledge_presence(self, num_workers):
        """
        Receives handshamke message from workers
        :param num_workers: {int} number of workers
        :return:None
        """

        context = zmq.Context()
        results_receiver = context.socket(zmq.PULL)
        results_receiver.bind(self.pull_address_str)

        for x in xrange(num_workers):
            result = results_receiver.recv_json()
            print 'worker x=', x, ' ready'

    def reduce(self, num_workers):
        """
        receives output from workers
        :param num_workers: {int} number of workers
        :return: None
        """

        context = zmq.Context()
        results_receiver = context.socket(zmq.PULL)
        results_receiver.bind(self.pull_address_str)
        return_data_dict = {}  # {worker_tag:return_value}

        sum = 0
        print 'reducing=', num_workers, ' workers'
        for x in xrange(num_workers):
            # print 'waiting for worker x=', x
            result = results_receiver.recv_json()

            return_data_dict[result['return_value_tag']] = result['return_value']

            print 'got result from worker x=', x, ' res=', result
            # sum += result['num']

        # print 'sum = ', sum
        return return_data_dict

    def param_generator(self, num_workers):
        counter = 0
        current_set = []
        for param in self.param_set_list:
            current_set.append(param)
            counter += 1
            if counter == num_workers:
                yield current_set
                current_set = []
                counter = 0

        # sending reminder of the params
        if len(current_set):
            yield current_set

    def get_formatted_timestamp(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%d_%m_%Y_%H_%M_%S')

    def create_workspace_dir(self, simulation_corename, workspace_root_dir):
        """
        Creates workspace directory for the optimization job
        :param simulation_corename: {str} simulation file name (basename)
        :param workspace_root_dir: {str} CC3D workspace root dir (typically ~/CC3DWorkspace)
        :return: None
        """

        formatted_timestamp = self.get_formatted_timestamp()
        workspace_dir = join(workspace_root_dir, simulation_corename + '_opt_' + formatted_timestamp)

        # creating workspace directory
        if isdir(workspace_dir):
            raise IOError('Cannot create output directory %s. This directory already exist' % workspace_dir)

        os.makedirs(workspace_dir)

        return workspace_dir

    def run_task(self, workload_dict, param_set):
        """
        Dispatches simulation jobs to workers based on the parameter set (param_set)
        :param workload_dict: {dictionary-like} workload information to be sent to worker - does not include param_dict.
        param_dict will be set by this function
        :param param_set: {list of ndarray's} parameter_set - a list of param array -first index goes over workers,
        second indexes parameters for a given worker
        :return: None
        """

        self.worker_pool = []

        num_params = len(param_set)

        # for w in xrange(self.num_workers):
        for w in xrange(num_params):
            worker = OptimizerWorkerProcessZMQ(id_number=w, name='worker_%s' % w)
            worker.set_pull_address_str(self.push_address_str)
            worker.set_push_address_str(self.pull_address_str)
            self.worker_pool.append(worker)

        for worker in self.worker_pool:
            worker.start()

        time.sleep(1.0)

        # self.acknowledge_presence(self.num_workers)

        # {worker_tag:param} - ordered dict needed for correct identification of positional index of return value
        param_set_dict = OrderedDict()

        for param_idx, param in enumerate(param_set):
            # mapping parameters from [0,1] to true range and producing dictionary that will be sent to workers
            param_dict = self.optimization_params_mgr.param_from_0_1_dict(param)

            # param_labels = ['TEMPERATURE', 'CONTACT_A_B']
            # param_vals = [12.2, float(param)]
            # param_dict = OrderedDict(zip(param_labels, param_vals))

            # appending param_dict to  workload dict
            workload_dict['param_dict'] = param_dict

            # tagging worker to identify return result
            worker_tag = 'worker_' + str(param_idx)
            workload_dict['worker_tag'] = worker_tag

            param_set_dict[worker_tag] = param

            # self.zmq_socket.send_json(param_dict)
            self.zmq_socket.send_json(workload_dict)

            print 'sent = ', workload_dict

        print 'WILL REDUCE ', param_idx + 1, ' workers'
        return_data_dict = self.reduce(param_idx + 1)

        # producing vector of return values - have to ensure that the order of values in the vector
        # is the same as the order of parameter vectors in the param_set

        return_value_vec = np.zeros((num_params,), dtype=np.float)

        for idx, worker_tag in enumerate(param_set_dict.keys()):
            return_value_vec[idx] = return_data_dict[worker_tag]

        print 'FINISHED REDUCING'

        return return_value_vec

    def prepare_optimization_run(self, simulation_name):
        """
        Prepares optimization run which includes: creating workspace directory for the optimization job
        and creating workload_dictionary (will be sent as json to worker)
        :param simulation_name: {str} simulation name
        :return: {dictionary-like} workload dictionary -  does not include param_dict
        """
        # path to cc3d project


        # constructing workspace dir for all jobs that are part of current optimization run
        workspace_root_dir = join(expanduser('~'), 'CC3DWorkspace')

        simulation_corename, ext = splitext(basename(simulation_name))

        workspace_dir = self.create_workspace_dir(simulation_corename, workspace_root_dir)

        workload_dict = OrderedDict()
        # workload_dict['cc3d_command'] = r'C:\CompuCell3D-64bit\runScript.bat'
        workload_dict['cc3d_command'] = self.parse_args.cc3d_run_script
        workload_dict['workspace_dir'] = workspace_dir
        workload_dict['simulation_filename'] = simulation_name
        workload_dict['clean_workdirs'] = self.parse_args.clean_workdirs
        workload_dict['param_dict'] = None  # set externally
        workload_dict['worker_tag'] = None  # set externally

        return workload_dict

    def save_optimal_parameters(self, optimal_parameters):
        workspace_dir = self.workload_dict['workspace_dir']
        optimal_param_fname = join(workspace_dir, 'optimal_parameters.json')

        optimal_param_dict = self.optim_param_mgr.param_from_0_1_dict(optimal_parameters)

        json.dump(optimal_param_dict, open(optimal_param_fname, 'w'))

    def save_optimal_simulation(self, optimal_parameters):

        workspace_dir = self.workload_dict['workspace_dir']
        simulation_template_name = self.workload_dict['simulation_filename']
        optimal_param_dict = self.optim_param_mgr.param_from_0_1_dict(optimal_parameters)

        optimal_simulation_dir = join(workspace_dir, 'optimal_simulation')

        generated_simulation_fname, workspace_dir = generate_simulation_files_from_template(
            simulation_dirname=optimal_simulation_dir,
            simulation_template_name=simulation_template_name,
            param_dict=optimal_param_dict
        )

        print

    def run_debug(self):

        """
        Debug run to test dispatching of parameters to workers
        :return:
        """
        simulation_name = r'D:\CC3DProjects\short_demo\short_demo.cc3d'
        workload_dict = self.prepare_optimization_run(simulation_name=simulation_name)

        for param_set in self.param_generator(self.num_workers):
            print 'CURRENT PARAM SET=', param_set
            self.run_task(workload_dict, param_set)
            print 'FINISHED PARAM_SET=', param_set

    def set_optimization_parameters_manager(self, optimization_params_mgr):

        self.optimization_params_mgr = optimization_params_mgr

    def set_parse_args(self, parse_args):
        self.parse_args = parse_args

    def set_num_workers(self, num_workers):
        self.num_workers = num_workers

    def set_param_set_list(self, param_set_list):
        self.param_set_list = param_set_list

    # def run_optimization(self):
    #
    #     """
    #     Runs optimization job
    #     :return:
    #     """
    #     # simulation_name = r'D:\CC3DProjects\short_demo\short_demo.cc3d'
    #
    #     simulation_name = self.parse_args.input
    #     optim_param_mgr = OptimizationParameterManager()
    #     optim_param_mgr.read_paramters(args.params_file)
    #
    #     starting_params = optim_param_mgr.get_starting_points()
    #     print 'starting_params (mapped to [0,1])=', starting_params
    #     print 'remapped (true) starting params=', optim_param_mgr.params_from_0_1(starting_params)
    #     print 'dictionary of remapped parameters labeled by parameter name=', optim_param_mgr.param_from_0_1_dict(
    #         starting_params)
    #
    #     print 'simulation_name=', simulation_name
    #     workload_dict = self.prepare_optimization_run(simulation_name=simulation_name)
    #     print workload_dict
    #     #
    #     for param_set in self.param_generator(self.num_workers):
    #         print 'CURRENT PARAM SET=', param_set
    #         self.run_task(workload_dict, param_set)
    #         print 'FINISHED PARAM_SET=', param_set

    def run_optimization(self):

        """
        Runs optimization job
        :return:
        """
        # simulation_name = r'D:\CC3DProjects\short_demo\short_demo.cc3d'

        simulation_name = self.parse_args.input

        self.optim_param_mgr = OptimizationParameterManager()
        optim_param_mgr = self.optim_param_mgr

        optim_param_mgr.parse(args.params_file)

        starting_params = optim_param_mgr.get_starting_points()
        print 'starting_params (mapped to [0,1])=', starting_params
        print 'remapped (true) starting params=', optim_param_mgr.params_from_0_1(starting_params)
        print 'dictionary of remapped parameters labeled by parameter name=', optim_param_mgr.param_from_0_1_dict(
            starting_params)

        print 'simulation_name=', simulation_name
        self.workload_dict = self.prepare_optimization_run(simulation_name=simulation_name)
        workload_dict = self.workload_dict

        print workload_dict

        std_dev = optim_param_mgr.std_dev
        default_bounds = optim_param_mgr.default_bounds

        optim = CMAEvolutionStrategy(starting_params, std_dev, {'bounds': list(default_bounds)})

        while not optim.stop():  # iterate
            # get candidate solutions
            param_set_list = optim.ask(number=self.num_workers)

            # set param_set_list for run_task to iterate over
            self.set_param_set_list(param_set_list=param_set_list)

            # #debug
            # return_result_vec = [self.fcn(optim_param_mgr.params_from_0_1(X)) for X in param_set_list]

            # evaluate  targert function values at the candidate solutions
            return_result_vec = np.array([], dtype=float)
            for param_set in self.param_generator(self.num_workers):
                print 'CURRENT PARAM SET=', param_set
                # distribution param_set to workers - run tasks spawns appropriate number of workers
                # given self.num_workers and the size of the param_set
                partial_return_result_vec = self.run_task(workload_dict, param_set)

                return_result_vec = np.append(return_result_vec, partial_return_result_vec)

                print 'FINISHED PARAM_SET=', param_set
            # in case do something else that needs to be done
            #


            optim.tell(param_set_list, return_result_vec)  # do all the real "update" work
            optim.disp(20)  # display info every 20th iteration
            optim.logger.add()  # log another "data line"

        optimal_parameters = optim.result()[0]

        print('termination by', optim.stop())
        print('best f-value =', optim.result()[1])
        optimal_parameters_remapped = optim_param_mgr.params_from_0_1(optim.result()[0])
        print('best solution =', optimal_parameters_remapped)

        # print('best solution =', optim_param_mgr.params_from_0_1(optim.result()[0]))

        print optim_param_mgr.params_names

        self.save_optimal_parameters(optimal_parameters)
        self.save_optimal_simulation(optimal_parameters)




        # print('best solution =', optim.result()[0])

        # param_set_list = optim.ask(number=self.num_workers)
        # print 'param_set_list=',param_set_list
        # self.set_param_set_list(param_set_list=param_set_list)
        #
        # return_result_vec = np.array([], dtype=float)
        #
        # for param_set in self.param_generator(self.num_workers):
        #     print 'CURRENT PARAM SET=', param_set
        #     # distribution param_set to workers - run tasks spawns appripriate number of workers
        #     # given self.num_workers and the size of the param_set
        #     partial_return_result_vec = self.run_task(workload_dict, param_set)
        #
        #     return_result_vec = np.append(return_result_vec, partial_return_result_vec)
        #
        #     print 'FINISHED PARAM_SET=', param_set
        #
        # print 'return_result_vec=', return_result_vec
        #
        # # checking - Note we have to order parameters in the same way they are ordered in the simulation code
        # check_vec = []
        #
        # params_names = optim_param_mgr.params_names
        #
        # for params in param_set_list:
        #     print 'params=',params
        #     params_remapped = optim_param_mgr.params_from_0_1(params)
        #
        #     params_remapped_ordered = [params_remapped[params_names.index('TEMPERATURE')],
        #                                params_remapped[params_names.index('CONTACT_A_B')]]
        #
        #     # ordering it to in the same order as in the simulation i.e. [temp, contact]
        #     print 'params_remapped=',params_remapped
        #     check_vec.append(self.fcn(params_remapped_ordered))
        #
        # check_vec = np.array(check_vec,dtype=np.float)
        #
        #
        # print " difference between worker results and manual comutation = ", check_vec -  return_result_vec

    def fcn(self, x):
        return (x[0] - 2) ** 2 + (x[1] - 3) ** 2

    def run(self):
        self.run_optimization()


if __name__ == '__main__':
    # from subprocess import call
    # popen_args = [r'C:\CompuCell3D-64bit\runScript.bat']
    #
    # # popen_args.append("--pushAddress=%s"%self.pull_address_str)
    # simulation_name = r'D:\CC3DProjects\short_demo\short_demo.cc3d'
    # output_frequency = 10
    # if simulation_name != "":
    #     popen_args.append("-i")
    #     popen_args.append(simulation_name)
    #
    # if output_frequency > 0:
    #
    #     popen_args.append("-f")
    #     popen_args.append(str(output_frequency))
    # else:
    #     popen_args.append("--noOutput")
    #
    # # popen_args.append("-p" )
    # # popen_args.append(str(self.pull_address_str))
    #
    # # popen_args.append("--pushAddress=%s" % str("dupa"))
    # popen_args.append("-p" )
    # popen_args.append("dupa")
    #
    # # popen_args.append(str(self.pull_address_str))
    #
    #
    # print 'popen_args=', popen_args
    # # sys.exit()
    # # this call will block until simulattion is done
    # call(popen_args)

    cml_parser = OptimizationCMLParser()

    # cml_parser.arg('--help')
    cml_parser.arg('--input', r'D:\CC3DProjects\short_demo\short_demo.cc3d')
    cml_parser.arg('--params-file', r'D:\CC3D_GIT\optimization\params.json')
    cml_parser.arg('--cc3d-run-script', r'C:\CompuCell3D-64bit\runScript.bat')
    cml_parser.arg('--clean-workdirs')
    cml_parser.arg('--num-workers', '5')  # here it needs to be specified as str but parser converts it to int

    args = cml_parser.parse()

    optim_param_mgr = OptimizationParameterManager()
    optim_param_mgr.parse(args.params_file)

    # starting_params = optim_param_mgr.get_starting_points()
    # print 'starting_params (mapped to [0,1])=', starting_params
    # print 'remapped (true) starting params=', optim_param_mgr.params_from_0_1(starting_params)
    # print 'dictionary of remapped parameters labeled by parameter name=', optim_param_mgr.param_from_0_1_dict(
    #     starting_params)
    #
    # print args.input
    # print args.params_file
    #
    # # # param_set_list = [1.1, 2.1, 3.2, 4.2, 5.1]
    # # param_set_list = [starting_params]
    # # param_set_list = 5 * param_set_list
    # # param_set_list = map(lambda x: random.random() * x, param_set_list)

    optimizer = Optimizer()

    optimizer.set_optimization_parameters_manager(optim_param_mgr)
    optimizer.set_parse_args(args)
    optimizer.set_num_workers(args.num_workers)
    # optimizer.set_param_set_list(param_set_list=param_set_list)

    optimizer.run()