from django.core.exceptions import ValidationError
from SignalProject.settings import MEDIA_ROOT
import scipy.io
import scipy.signal
import pandas
import json
import numpy
import os


def load_signal(file_instance):

    if file_instance.name.endswith('.mat'):

        # TODO: Implementation of multi dimetional signal and static time vector

        def signal_array(file):

            for key in file.keys():

                if type(file[key]) is numpy.ndarray:
                    return file[key]

            raise ValidationError(u'File does not consist any array!')

        file = scipy.io.loadmat(file_instance)
        signal_data = signal_array(file)

        if signal_data.shape[0] > signal_data.shape[1] and  signal_data.shape[1] == 1:

            signal_data_final_values = [ element[0] for element in signal_data]
            time = [x for x in range(len(signal_data_final_values))]

            return signal_data_final_values, time

        elif signal_data.shape[0] < signal_data.shape[1] and signal_data.shape[0] == 1:

            signal_data_final_values = list(signal_data[0])
            time = [x for x in range(len(signal_data_final_values))]

            return signal_data_final_values, time

        else:
            raise ValidationError(u'Unexpected shape of file! Check Your data.')

    elif file_instance.name.endswith('.json'):

        # TODO: Implementation of multi dimetional signal and static time vector

        file = json.loads(file_instance.read())

        if type(file['signal_data']) is list:
            signal_data_final_values = file['signal_data']
            time = list(numpy.arange(0, len(signal_data_final_values), 1))

            return signal_data_final_values, time

        else:
            raise ValidationError(u'Unexpected format of data! Please input data as list type.')


    elif file_instance.name.endswith('.csv'):

        # TODO: Implementation of data with headers dimetional signal

        df = pandas.read_csv(file_instance, header=None)

        signal_data_final_values = df[0].tolist()
        time = [x for x in range(len(signal_data_final_values))]

        return signal_data_final_values, time

    else:
        raise ValidationError(u'Unexpected file extension! Your data may be corrupted.')


def statistic_energy_analisys(signal_data_final_values):

    signal_mean = numpy.mean(signal_data_final_values)

    if round(signal_mean, 6) == -0.0:
        signal_mean = 0.0

    signal_energy = numpy.sum(numpy.power(signal_data_final_values, 2))
    signal_power = signal_energy/len(signal_data_final_values)

    return signal_mean, signal_energy, signal_power


def calculate_fft(signal_data_final_values, Fs):


    signal_data_final_values_mean = numpy.mean(signal_data_final_values)
    signal_data_final_values -= signal_data_final_values_mean

    n = len(signal_data_final_values) # length of the signal
    k = numpy.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n)] # one side frequency range

    signal_fft = list(numpy.absolute(numpy.real(numpy.fft.fft(signal_data_final_values))/n))

    sig_fft = []

    for i in range(0, len(signal_fft)):
        sig_fft.append(signal_fft[i])

    plot_range = int(n/2)

    return list(frq[0:plot_range]), signal_fft[0:plot_range]


def save_results_to_json(
                         signal,
                         signal_data_final_values,
                         signal_fft,
                         frequency_vector,
                         signal_mean,
                         signal_energy,
                         signal_power):

    file_path = MEDIA_ROOT + '/' + str(signal.results_file)

    results = json.loads(open(file_path).read())


    results['main_info']['name'] = signal.name
    results['main_info']['author'] = signal.author.username
    results['main_info']['adnotations'] = signal.adnotations
    results['main_info']['amplitude_unit'] = signal.amplitude_unit
    results['main_info']['add_date'] = signal.add_date_pretty()
    results['main_info']['last_edit_date'] = signal.last_edit_date_pretty()

    results['basic_analysis']['sample_rate'] = signal.sample_rate
    results['basic_analysis']['signal_values'] = list(signal_data_final_values)
    results['basic_analysis']['fft_values'] = list(signal_fft)
    results['basic_analysis']['frequency_vector'] = list(frequency_vector)
    results['basic_analysis']['signal_mean'] = signal_mean
    results['basic_analysis']['signal_power'] = signal_energy
    results['basic_analysis']['signal_energy'] = signal_power

    input_file_strings = os.path.basename(signal.input_file.name).split('.')
    input_file_name = input_file_strings[0]

    with open(MEDIA_ROOT + '/results/' + input_file_name + '_results.json', 'w') as outfile:
        json.dump(results, outfile)

    signal.results_file.name = 'results/' + input_file_name + '_results.json'
    signal.save()


def save_filtration_results_to_json(
                                    signal,
                                    signal_values_filtered_final,
                                    signal_fft,
                                    signal_mean,
                                    signal_energy,
                                    signal_power,
                                    filter_type,
                                    filter_len,
                                    cutoff_frq_low,
                                    cutoff_frq_high,
                                    filter_window):


        file_path = MEDIA_ROOT + '/' + str(signal.results_file)

        results = json.loads(open(file_path).read())

        results['main_info']['last_edit_date'] = signal.last_edit_date_pretty()

        results['filration_results'][filter_type]['signal_values'] = list(signal_values_filtered_final)
        results['filration_results'][filter_type]['fft_values'] = signal_fft
        results['filration_results'][filter_type]['signal_mean'] = signal_mean
        results['filration_results'][filter_type]['signal_power'] = signal_energy
        results['filration_results'][filter_type]['signal_energy'] = signal_power
        results['filration_results'][filter_type]['filter_len'] = filter_len
        results['filration_results'][filter_type]['cutoff_frq'] = cutoff_frq_low
        results['filration_results'][filter_type]['cutoff_frq2'] = cutoff_frq_high
        results['filration_results'][filter_type]['filter_window'] = filter_window

        input_file_strings = os.path.basename(signal.input_file.name).split('.')
        input_file_name = input_file_strings[0]

        with open(MEDIA_ROOT + '/results/' + input_file_name + '_results.json', 'w') as outfile:
            json.dump(results, outfile)

        signal.results_file.name = 'results/' + input_file_name + '_results.json'
        signal.save()


def perform_signal_filtration(
                              filter_type,
                              filter_len,
                              cutoff_frq_low,
                              cutoff_frq_high,
                              filter_window,
                              f_sample,
                              signal_values):

    if filter_type == 'lowpass':

        filter_design = scipy.signal.firwin(
                                            int(filter_len),
                                            int(cutoff_frq_low),
                                            window=filter_window,
                                            fs=f_sample)

        low_range = int(int(filter_len)/2)
        high_range = int(int(filter_len)/2)

    elif filter_type == 'highpass':

        filter_len = int(filter_len)
        if filter_len%2 == 0:
            filter_len -= 1
        filter_design = scipy.signal.firwin(
                                            filter_len,
                                            int(cutoff_frq_low),
                                            window=filter_window,
                                            fs=f_sample,
                                            pass_zero=False)

        low_range = int(int(filter_len)/2)
        high_range = int(int(filter_len)/2)

    elif filter_type == 'bandpass':

        filter_len = int(filter_len)
        if filter_len%2 == 0:
            filter_len -= 1
        filter_design = scipy.signal.firwin(
                                            filter_len,
                                            [int(cutoff_frq_low),
                                             int(cutoff_frq_high)],
                                            window=filter_window,
                                            fs=f_sample,
                                            pass_zero=False)
        low_range = filter_len
        high_range = filter_len

    freq_w, freq_h = scipy.signal.freqz(filter_design)
    freq_h = 20 * numpy.log10(abs(freq_h))

    low = int(len(filter_design)/2)
    vector = [x for x in range(0-low,low)]

    signal_values_filtered = scipy.signal.convolve(signal_values, filter_design)

    return [signal_values_filtered[i] for i in range(low_range, len(signal_values_filtered) - high_range)], list(freq_w), list(freq_h), list(filter_design), vector
