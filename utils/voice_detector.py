"""
Voice detection model to classify AI-generated vs Human voices
"""
import numpy as np
from typing import Dict, Tuple
from utils.audio_processor import extract_audio_features, load_audio_features


class VoiceDetector:
    """
    Detector class for identifying AI-generated vs Human voices
    """
    
    def __init__(self):
        """Initialize the voice detector"""
        pass
    
    def detect(self, audio_path: str, language: str) -> Tuple[str, float, str]:
        """
        Detect if voice is AI-generated or Human
        
        Args:
            audio_path: Path to audio file
            language: Language of the audio
            
        Returns:
            Tuple of (classification, confidence_score, explanation)
        """
        # Load and extract features
        audio, sr = load_audio_features(audio_path)
        features = extract_audio_features(audio, sr)
        
        # Analyze features to determine if AI-generated
        classification, confidence, explanation = self._analyze_features(features, language)
        
        return classification, confidence, explanation
    
    def _analyze_features(self, features: Dict, language: str) -> Tuple[str, float, str]:
        """
        Analyze audio features to classify voice
        
        Args:
            features: Extracted audio features
            language: Language of the audio
            
        Returns:
            Tuple of (classification, confidence_score, explanation)
        """
        # Initialize scores
        ai_score = 0.0
        human_score = 0.0
        reasons = []
        
        # Feature-based heuristics for AI detection
        
        # 1. Pitch consistency (AI voices often have very consistent pitch)
        if features['pitch_std'] < 20:  # Low pitch variation
            ai_score += 0.15
            reasons.append("unusually consistent pitch")
        else:
            human_score += 0.1
        
        # 2. Spectral centroid variation (AI may have less natural variation)
        if features['spectral_centroid_std'] < 500:
            ai_score += 0.1
            reasons.append("limited spectral variation")
        else:
            human_score += 0.1
        
        # 3. Zero crossing rate (natural speech has more variation)
        if features['zcr_std'] < 0.01:
            ai_score += 0.1
            reasons.append("unnatural zero crossing patterns")
        else:
            human_score += 0.1
        
        # 4. Energy variation (human speech has natural energy fluctuations)
        if features['energy_std'] < 0.01:
            ai_score += 0.1
            reasons.append("unnatural energy consistency")
        else:
            human_score += 0.1
        
        # 5. MFCC patterns (AI voices may have different MFCC characteristics)
        mfcc_std_mean = np.mean(features['mfcc_std'])
        if mfcc_std_mean < 5:
            ai_score += 0.1
            reasons.append("atypical MFCC patterns")
        else:
            human_score += 0.1
        
        # 6. Spectral rolloff (natural speech has more variation)
        if features['spectral_rolloff_std'] < 500:
            ai_score += 0.1
            reasons.append("limited spectral rolloff variation")
        else:
            human_score += 0.1
        
        # 7. Pitch range (AI voices may have limited pitch range)
        if features['pitch_range'] < 100:
            ai_score += 0.1
            reasons.append("restricted pitch range")
        else:
            human_score += 0.1
        
        # Normalize scores
        total_score = ai_score + human_score
        if total_score > 0:
            ai_score = ai_score / total_score
            human_score = human_score / total_score
        
        # Determine classification
        if ai_score > human_score:
            classification = "AI_GENERATED"
            confidence = min(0.99, ai_score + 0.1)  # Boost confidence slightly
            explanation = "Unnatural pitch consistency and robotic speech patterns detected"
        else:
            classification = "HUMAN"
            confidence = min(0.99, human_score + 0.1)
            explanation = "Natural speech patterns with expected variations detected"
        
        # Add specific reasons if available
        if reasons and classification == "AI_GENERATED":
            explanation = f"Unnatural patterns detected: {', '.join(reasons[:3])}"
        
        # Ensure confidence is in valid range
        confidence = max(0.5, min(0.99, confidence))
        
        return classification, confidence, explanation

