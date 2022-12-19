import os
import string
import torch
from TTS.api import TTS
from TTS.tts.utils.synthesis import synthesis
from TTS.utils.audio import AudioProcessor
from TTS.tts.utils.speakers import SpeakerManager

CONFIG_SE_PATH = "speaker_encoders/se_1/config_se.json"
CHECKPOINT_SE_PATH = "speaker_encoders/se_1/SE_checkpoint.pth.tar"

OUT_PATH = 'results/'
os.makedirs(OUT_PATH, exist_ok=True)
USE_CUDA = torch.cuda.is_available()


class OurTTSModel:

    def __init__(self):
        model_name = TTS.list_models()[0]
        self.tts = TTS(model_name)
        self.ap = AudioProcessor(**self.tts.synthesizer.tts_config.audio)

        self.tts.synthesizer.tts_model.length_scale = 1  # scaler for the duration predictor. The larger it is, the slower the speech.
        self.tts.synthesizer.tts_model.inference_noise_scale = 0.3  # defines the noise variance applied to the random z vector at inference.
        self.tts.synthesizer.tts_model.inference_noise_scale_dp = 0.3  # defines the noise variance applied to the duration predictor z vector at inference.

    def load_speaker_encoder(self, CHECKPOINT_SE_PATH, CONFIG_SE_PATH):
        self.SE_speaker_manager = SpeakerManager(encoder_model_path=CHECKPOINT_SE_PATH,
                                                 encoder_config_path=CONFIG_SE_PATH,
                                                 use_cuda=USE_CUDA)

    def fit(self, paths, text, out_path):
        reference_files = list(paths)
        for sample in reference_files:
            # !ffmpeg-normalize $sample -nt rms -t=-27 -o $sample -ar 16000 -f
            os.system(f"ffmpeg-normalize {sample} -nt rms -t=-27 -o {sample} -ar 16000 -f")

        reference_emb = self.SE_speaker_manager.compute_embedding_from_clip(reference_files)

        wav, alignment, _, _ = synthesis(
            self.tts.synthesizer.tts_model,
            text,
            self.tts.synthesizer.tts_config,
            "cuda" in str(next(self.tts.synthesizer.tts_model.parameters()).device),
            speaker_id=None,
            d_vector=reference_emb,
            style_wav=None,
            language_id=0,
            use_griffin_lim=True,
            do_trim_silence=True,
        ).values()

        file_name = text.replace(" ", "_")
        file_name = file_name.translate(str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
        print(" > Saving output to {}".format(out_path))
        self.ap.save_wav(wav, out_path)

        return out_path


our_tts = OurTTSModel()
our_tts.load_speaker_encoder(CHECKPOINT_SE_PATH, CONFIG_SE_PATH)
