"""
Audio processing utilities for voice detection
"""
import base64
import io
import tempfile
import os
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
from typing import Tuple, Optional


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
        # Load audio file
        audio, sr = librosa.load(audio_path, sr=None)
        return audio, sr
    except Exception as e:
        raise ValueError(f"Error loading audio file: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(audio_path):
            os.unlink(audio_path)


def extract_audio_features(audio: np.ndarray, sr: int) -> dict:
    """
    Extract features from audio for voice detection
    
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
    
    # Zero crossing rate
    features['zcr_mean'] = np.mean(librosa.feature.zero_crossing_rate(audio)[0])
    features['zcr_std'] = np.std(librosa.feature.zero_crossing_rate(audio)[0])
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    features['spectral_centroid_mean'] = np.mean(spectral_centroids)
    features['spectral_centroid_std'] = np.std(spectral_centroids)
    
    # MFCC features (commonly used for voice analysis)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    features['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()
    features['mfcc_std'] = np.std(mfccs, axis=1).tolist()
    
    # Chroma features
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    features['chroma_mean'] = np.mean(chroma, axis=1).tolist()
    
    # Pitch features
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
    else:
        features['pitch_mean'] = 0
        features['pitch_std'] = 0
        features['pitch_range'] = 0
    
    # Energy features
    rms = librosa.feature.rms(y=audio)[0]
    features['energy_mean'] = np.mean(rms)
    features['energy_std'] = np.std(rms)
    
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
    features['spectral_rolloff_mean'] = np.mean(rolloff)
    features['spectral_rolloff_std'] = np.std(rolloff)
    
    return features

