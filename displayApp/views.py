from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from storageApp.models import InputSignal
from django.shortcuts import redirect
from django.core.files import File
from datetime import datetime
from . import analysis


@login_required(login_url="/")
def display_list(request):

    signals = InputSignal.objects.filter(author=request.user)

    return render(request, 'display_list.html', {'signals': signals})


@login_required(login_url="/")
def display_details(request):

    signal_id = request.GET['signal_id']
    signal = get_object_or_404(InputSignal, pk=signal_id)

    if signal.author == request.user:

        signal_values, time = analysis.load_signal(signal.input_file)
        signal.input_file.close()
        signal_mean, signal_energy, signal_power = analysis.statistic_energy_analisys(signal_values)
        frequency_vector, signal_fft = analysis.calculate_fft(signal_values, signal.sample_rate)

        results = analysis.save_results_to_json(
                                                signal,
                                                signal_values,
                                                signal_fft,
                                                frequency_vector,
                                                signal_mean,
                                                signal_energy,
                                                signal_power)

        signal.last_edit_date = datetime.now
        signal.save()

        return render(request, 'display_details.html', {'signal': signal,'signal_data': signal_values, 'time': time, 'signal_mean': signal_mean, 'signal_energy': signal_energy,
                                                        'signal_power': signal_power, 'signal_fft': signal_fft, 'frequency_vector': frequency_vector})

    elif signal.DoesNotExist:

        signals = InputSignal.objects.filter(author=request.user)
        return render(request, 'display_list.html', {'signals': signals, 'error1': 'You do not have access to this data!', 'error2': ' Select the signal from the list below'})

    else:

        signals = InputSignal.objects.filter(author=request.user)
        return render(request, 'display_list.html', {'signals': signals, 'error1': 'You do not have access to this data!', 'error2': ' Select the signal from the list below'})


@login_required(login_url="/")
def display_filtration(request):

        signal_id = request.GET['signal_id']
        signal = get_object_or_404(InputSignal, pk=signal_id)

        if signal.author == request.user:

            filter_type = request.GET['filter_type']
            filter_len = request.GET['filter_len']
            cutoff_frq_low = request.GET['cutoff_frq']
            cutoff_frq_high = request.GET['cutoff_frq2']
            filter_window = request.GET['filter_window']

            signal_values, time = analysis.load_signal(signal.input_file)

            if (int(cutoff_frq_low) >= signal.sample_rate) or (int(cutoff_frq_low) <= 0)  or (int(filter_len) <= 0) or (int(filter_len) >= len(signal_values)):
                signals = InputSignal.objects.filter(author=request.user)
                return render(request, 'display_list.html', {'signals': signals, 'error1': 'Wrong filter parameters have been introduced!', 'error2': ' Make sure that the values meet the theoretical assumptions'})

            if filter_type == 'bandpass':
                if (int(cutoff_frq_low) >= int(cutoff_frq_high)) or (int(cutoff_frq_high) >= signal.sample_rate):
                    signals = InputSignal.objects.filter(author=request.user)
                    return render(request, 'display_list.html', {'signals': signals, 'error1': 'Wrong filter parameters have been introduced!', 'error2': ' Make sure that the values meet the theoretical assumptions'})

            signal_values_filtered_final, freq_w, freq_h, filter_design, vector = analysis.perform_signal_filtration(
                                                                              filter_type,
                                                                              filter_len,
                                                                              cutoff_frq_low,
                                                                              cutoff_frq_high,
                                                                              filter_window,
                                                                              signal.sample_rate,
                                                                              signal_values)


            signal_mean, signal_energy, signal_power = analysis.statistic_energy_analisys(signal_values_filtered_final)
            frequency_vector, signal_fft = analysis.calculate_fft(signal_values_filtered_final, signal.sample_rate)

            results = analysis.save_filtration_results_to_json(
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
                                                               filter_window)

            signal.input_file.close()
            signal.last_edit_date = datetime.now
            signal.save()

            return render(request, 'display_filtration.html', {'filtration_type': filter_type, 'signal': signal, 'signal_data': signal_values_filtered_final, 'time': time,
                                                               'frequency_vector': frequency_vector, 'signal_fft': signal_fft, 'signal_mean': signal_mean,
                                                               'signal_energy': signal_energy, 'signal_power': signal_power, 'freq_w': freq_w, 'freq_h': freq_h, 'filter_design': filter_design, 'vector': vector})

        elif signal.DoesNotExist:

            signals = InputSignal.objects.filter(author=request.user)
            return render(request, 'display_list.html', {'signals': signals, 'error1': 'You do not have access to this data!', 'error2': ' Select the signal from the list below'})

        else:

            signals = InputSignal.objects.filter(author=request.user)
            return render(request, 'display_list.html', {'signals': signals, 'error1': 'You do not have access to this data!', 'error2': ' Select the signal from the list below'})
