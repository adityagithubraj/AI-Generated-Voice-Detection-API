"""
Audio processing utilities for voice detection
"""
import base64
import io
import tempfile
import os
from typing import Tuple, Optional

import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment

import config


def decode_base64_audio(base64_string: str) -> bytes:
    """
    Decode Base64 string to audio bytes
    
    Args:
        base64_string: Base64-encoded audio string
        
    Returns:
        Decoded audio bytes
    """
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"Invalid Base64 encoding: {str(e)}")


def save_temp_audio(audio_bytes: bytes, format: str = "mp3") -> str:
    """
    Save audio bytes to a temporary file
    
    Args:
        audio_bytes: Audio file bytes
        format: Audio format (mp3, wav, etc.)
        
    Returns:
        Path to temporary audio file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}")
    temp_file.write(audio_bytes)
    temp_file.close()
    return temp_file.name


def load_audio_features(audio_path: str) -> Tuple[np.ndarray, int]:
    """
    Load audio file and extract features
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Tuple of (audio_array, sample_rate)
    """
    try:
        # For faster processing, downsample to a fixed rate and convert to mono.
        # This significantly reduces computation while keeping enough detail
        # for AI vs Human voice detection.
        target_sr = 16_000

        # Load audio file
        audio, sr = librosa.load(audio_path, sr=target_sr, mono=True)

        # Optionally limit the analysis duration to speed up processing.
        # Use at most 10 seconds, but never exceed the global max duration.
        max_seconds = min(10, getattr(config, "MAX_AUDIO_DURATION_SECONDS", 60))
        max_len = int(max_seconds * sr)
        if len(audio) > max_len:
            audio = audio[:max_len]

        return audio, sr
    except Exception as e:
        raise ValueError(f"Error loading audio file: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(audio_path):
            os.unlink(audio_path)


def extract_audio_features(audio: np.ndarray, sr: int) -> dict:
    """
    Extract comprehensive features from audio for voice detection
    
    Args:
        audio: Audio array
        sr: Sample rate
        
    Returns:
        Dictionary of extracted features
    """
    features = {}
    
    # Basic audio properties
    features['duration'] = len(audio) / sr
    features['sample_rate'] = sr
    
    # Zero crossing rate (more detailed)
    zcr = librosa.feature.zero_crossing_rate(audio)[0]
    features['zcr_mean'] = np.mean(zcr)
    features['zcr_std'] = np.std(zcr)
    features['zcr_max'] = np.max(zcr)
    features['zcr_min'] = np.min(zcr)
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    features['spectral_centroid_mean'] = np.mean(spectral_centroids)
    features['spectral_centroid_std'] = np.std(spectral_centroids)
    features['spectral_centroid_max'] = np.max(spectral_centroids)
    features['spectral_centroid_min'] = np.min(spectral_centroids)
    
    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
    features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
    features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
    
    # Spectral contrast (moderately expensive but informative)
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
    features['spectral_contrast_mean'] = np.mean(spectral_contrast)
    features['spectral_contrast_std'] = np.std(spectral_contrast)
    
    # MFCC features (commonly used for voice analysis) - more detailed
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    features['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()
    features['mfcc_std'] = np.std(mfccs, axis=1).tolist()
    features['mfcc_max'] = np.max(mfccs, axis=1).tolist()
    features['mfcc_min'] = np.min(mfccs, axis=1).tolist()
    # MFCC delta (rate of change)
    mfcc_delta = librosa.feature.delta(mfccs)
    features['mfcc_delta_mean'] = np.mean(mfcc_delta)
    features['mfcc_delta_std'] = np.std(mfcc_delta)
    
    # Chroma features
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    features['chroma_mean'] = np.mean(chroma, axis=1).tolist()
    features['chroma_std'] = np.std(chroma, axis=1).tolist()
    
    # Pitch features (improved)
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    
    if pitch_values:
        features['pitch_mean'] = np.mean(pitch_values)
        features['pitch_std'] = np.std(pitch_values)
        features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
        features['pitch_max'] = np.max(pitch_values)
        features['pitch_min'] = np.min(pitch_values)
        # Pitch stability (coefficient of variation)
        if features['pitch_mean'] > 0:
            features['pitch_cv'] = features['pitch_std'] / features['pitch_mean']
        else:
            features['pitch_cv'] = 0
    else:
        features['pitch_mean'] = 0
        features['pitch_std'] = 0
        features['pitch_range'] = 0
        features['pitch_max'] = 0
        features['pitch_min'] = 0
        features['pitch_cv'] = 0
    
    # Energy features (RMS)
    rms = librosa.feature.rms(y=audio)[0]
    features['energy_mean'] = np.mean(rms)
    features['energy_std'] = np.std(rms)
    features['energy_max'] = np.max(rms)
    features['energy_min'] = np.min(rms)
    # Energy variation coefficient
    if features['energy_mean'] > 0:
        features['energy_cv'] = features['energy_std'] / features['energy_mean']
    else:
        features['energy_cv'] = 0
    
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
    features['spectral_rolloff_mean'] = np.mean(rolloff)
    features['spectral_rolloff_std'] = np.std(rolloff)
    
    return features



