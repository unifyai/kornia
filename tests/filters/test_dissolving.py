import pytest
import torch

from kornia.core import Tensor
from kornia.filters.dissolving import StableDiffusionDissolving

WEIGHTS_CACHE_DIR = "weights/"


@pytest.mark.slow
class TestStableDiffusionDissolving:
    @pytest.fixture(scope="class")
    def sdm_2_1(self):
        return StableDiffusionDissolving(version="2.1", cache_dir=WEIGHTS_CACHE_DIR)

    @pytest.fixture(scope="class")
    def dummy_image(self):
        # Create a dummy image tensor with shape [B, C, H, W], where B is the batch size.
        return torch.rand(1, 3, 64, 64)

    def test_init(self, sdm_2_1):
        assert isinstance(sdm_2_1, StableDiffusionDissolving), "Initialization failed"

    def test_encode_tensor_to_latent(self, sdm_2_1, dummy_image):
        latents = sdm_2_1.model.encode_tensor_to_latent(dummy_image)
        assert isinstance(latents, Tensor), "Latent encoding failed"
        assert latents.shape == (1, 4, 8, 8), "Latent shape mismatch"

    def test_decode_tensor_to_latent(self, sdm_2_1, dummy_image):
        latents = sdm_2_1.model.encode_tensor_to_latent(dummy_image)
        reconstructed_image = sdm_2_1.model.decode_tensor_to_latent(latents)
        assert isinstance(reconstructed_image, Tensor), "Latent decoding failed"
        assert reconstructed_image.shape == dummy_image.shape, "Reconstructed image shape mismatch"

    def test_dissolve(self, sdm_2_1, dummy_image):
        step_number = 500  # Test with a middle step
        dissolved_image = sdm_2_1(dummy_image, step_number)
        assert isinstance(dissolved_image, Tensor), "Dissolve failed"
        assert dissolved_image.shape == dummy_image.shape, "Dissolved image shape mismatch"

    def test_invalid_version(self):
        with pytest.raises(NotImplementedError):
            StableDiffusionDissolving(version="invalid_version")
