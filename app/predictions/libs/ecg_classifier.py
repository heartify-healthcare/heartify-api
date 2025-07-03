import numpy as np
import pandas as pd
from scipy.signal import find_peaks, butter, filtfilt
from scipy.stats import zscore
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import warnings
import json
warnings.filterwarnings('ignore')

class ECGClassifier:
    def __init__(self, sampling_rate=250):
        """
        ECG Classifier để phân loại ECG thành 3 nhóm:
        0: Normal
        1: ST-T wave abnormality
        2: Left ventricular hypertrophy (LVH)
        Args:
            sampling_rate (int): Tần số lấy mẫu (Hz)
        """
        self.sampling_rate = sampling_rate
        # self.scaler = StandardScaler()

    def preprocess_ecg(self, ecg_signal):
        """
        Tiền xử lý tín hiệu ECG
        """
        # Loại bỏ baseline drift và noise
        nyquist = self.sampling_rate / 2
        low_cutoff = 0.5 / nyquist
        high_cutoff = 40 / nyquist

        # Butterworth bandpass filter
        b, a = butter(4, [low_cutoff, high_cutoff], btype='band')
        filtered_signal = filtfilt(b, a, ecg_signal)

        # Normalize signal
        normalized_signal = (filtered_signal - np.mean(filtered_signal)) / np.std(filtered_signal)

        return normalized_signal

    def detect_qrs_peaks(self, ecg_signal):
        """
        Phát hiện QRS peaks
        """
        # Tìm peaks với adaptive threshold
        peaks, properties = find_peaks(ecg_signal,
                                     height=np.std(ecg_signal) * 1.5,
                                     distance=int(0.3 * self.sampling_rate))  # Min 300ms between beats
        return peaks

    def extract_beats(self, ecg_signal, qrs_peaks):
        """
        Trích xuất từng nhịp tim từ tín hiệu ECG
        """
        beats = []
        beat_length = int(0.8 * self.sampling_rate)  # 800ms per beat

        for peak in qrs_peaks:
            start = max(0, peak - beat_length // 3)  # 267ms before R
            end = min(len(ecg_signal), peak + 2 * beat_length // 3)  # 533ms after R

            if end - start >= beat_length // 2:  # Minimum beat length
                beat = ecg_signal[start:end]
                if len(beat) > beat_length:
                    beat = beat[:beat_length]
                elif len(beat) < beat_length:
                    beat = np.pad(beat, (0, beat_length - len(beat)), 'constant')
                beats.append(beat)

        return np.array(beats)

    def analyze_st_segment(self, beat):
        """
        Phân tích ST segment để phát hiện ST-T abnormalities
        """
        if len(beat) < 100:
            return False, 0

        # Tìm R peak trong beat
        r_peak_idx = np.argmax(beat)

        # ST segment: 80ms sau R peak
        st_start = min(r_peak_idx + int(0.08 * self.sampling_rate), len(beat) - 1)
        st_end = min(r_peak_idx + int(0.2 * self.sampling_rate), len(beat) - 1)

        if st_end <= st_start:
            return False, 0

        # Baseline (isoelectric line) - J point trước QRS
        baseline_start = max(0, r_peak_idx - int(0.1 * self.sampling_rate))
        baseline_end = max(1, r_peak_idx - int(0.02 * self.sampling_rate))

        if baseline_end <= baseline_start:
            baseline = beat[0]  # fallback
        else:
            baseline = np.mean(beat[baseline_start:baseline_end])

        # ST segment analysis
        st_segment = beat[st_start:st_end]
        st_elevation = np.mean(st_segment) - baseline

        # T wave analysis (200-400ms sau R peak)
        t_start = min(r_peak_idx + int(0.2 * self.sampling_rate), len(beat) - 1)
        t_end = min(r_peak_idx + int(0.4 * self.sampling_rate), len(beat) - 1)

        t_wave_inverted = False
        if t_end > t_start:
            t_wave = beat[t_start:t_end]
            # T wave inversion nếu giá trị âm chiếm ưu thế
            t_wave_inverted = np.mean(t_wave) < baseline - 0.1

        # ST-T abnormality criteria
        st_abnormal = abs(st_elevation) > 0.05  # >0.05mV elevation/depression

        return st_abnormal or t_wave_inverted, st_elevation

    def analyze_lvh_criteria(self, beats):
        """
        Phân tích tiêu chuẩn Estes cho Left Ventricular Hypertrophy
        """
        if len(beats) == 0:
            return False, 0

        # Average beat for analysis
        avg_beat = np.mean(beats, axis=0)

        if len(avg_beat) < 100:
            return False, 0

        # Tìm R peak
        r_peak_idx = np.argmax(avg_beat)
        r_amplitude = avg_beat[r_peak_idx]

        # Tìm S wave (điểm âm sâu nhất sau R)
        s_search_start = r_peak_idx
        s_search_end = min(r_peak_idx + int(0.1 * self.sampling_rate), len(avg_beat))

        s_amplitude = 0
        if s_search_end > s_search_start:
            s_region = avg_beat[s_search_start:s_search_end]
            s_idx = np.argmin(s_region) + s_search_start
            s_amplitude = abs(avg_beat[s_idx])

        # Estes criteria scoring (simplified)
        estes_score = 0

        # 1. R/S amplitude criteria (3 points)
        if r_amplitude > 2.0 or s_amplitude > 2.0:  # High voltage
            estes_score += 3

        # 2. QRS duration (1 point if > 90ms)
        qrs_duration = self.estimate_qrs_duration(avg_beat, r_peak_idx)
        if qrs_duration > 0.09 * self.sampling_rate:  # >90ms
            estes_score += 1

        # 3. Left axis deviation (simplified, 2 points)
        # Estimate based on R/S ratio
        if r_amplitude > s_amplitude * 2:
            estes_score += 2

        # LVH if Estes score >= 4
        lvh_detected = estes_score >= 4

        return lvh_detected, estes_score

    def estimate_qrs_duration(self, beat, r_peak_idx):
        """
        Ước tính độ rộng QRS complex
        """
        # Tìm Q wave (điểm bắt đầu QRS)
        q_search_start = max(0, r_peak_idx - int(0.08 * self.sampling_rate))
        q_search_end = r_peak_idx

        q_start = q_search_start
        for i in range(q_search_end, q_search_start, -1):
            if abs(beat[i] - beat[q_search_start]) > 0.1:
                q_start = i
                break

        # Tìm S wave end
        s_search_start = r_peak_idx
        s_search_end = min(r_peak_idx + int(0.12 * self.sampling_rate), len(beat))

        s_end = s_search_end
        for i in range(s_search_start, s_search_end):
            if i < len(beat) - 1 and abs(beat[i+1] - beat[i]) < 0.05:
                s_end = i
                break

        return s_end - q_start

    def classify_ecg(self, ecg_signal):
        """
        Phân loại tín hiệu ECG

        Returns:
            int: 0=Normal, 1=ST-T abnormality, 2=LVH
            dict: Chi tiết phân tích
        """
        # Tiền xử lý
        processed_signal = self.preprocess_ecg(ecg_signal)

        # Phát hiện QRS peaks
        qrs_peaks = self.detect_qrs_peaks(processed_signal)

        if len(qrs_peaks) < 3:
            return 0, {"error": "Insufficient QRS complexes detected"}

        # Trích xuất beats
        beats = self.extract_beats(processed_signal, qrs_peaks)

        if len(beats) == 0:
            return 0, {"error": "No valid beats extracted"}

        # Phân tích ST-T abnormalities
        st_abnormal_count = 0
        st_elevations = []

        for beat in beats:
            st_abnormal, st_elevation = self.analyze_st_segment(beat)
            if st_abnormal:
                st_abnormal_count += 1
            st_elevations.append(st_elevation)

        # Phân tích LVH
        lvh_detected, estes_score = self.analyze_lvh_criteria(beats)

        # Classification logic
        st_abnormal_ratio = st_abnormal_count / len(beats)

        analysis_details = {
            "num_beats": len(beats),
            "st_abnormal_count": st_abnormal_count,
            "st_abnormal_ratio": st_abnormal_ratio,
            "avg_st_elevation": np.mean(st_elevations),
            "lvh_detected": lvh_detected,
            "estes_score": estes_score,
            "heart_rate": len(qrs_peaks) * 60 / (len(ecg_signal) / self.sampling_rate)
        }

        # Priority classification
        if lvh_detected:
            return 2, analysis_details  # LVH
        elif st_abnormal_ratio > 0.5:  # >50% beats have ST-T abnormality
            return 1, analysis_details  # ST-T abnormality
        else:
            return 0, analysis_details  # Normal