from __future__ import annotations

from dataclasses import dataclass

from .codecs import ALGORITHM_NAMES, create_codec
from .profiles import Profile


@dataclass(frozen=True)
class StrategyResult:
    algorithm_id: int
    payload: bytes
    codec_metadata: dict
    candidate_sizes: list[tuple[int, int]]


class CompressionStrategy:
    def compress(self, profile: Profile, data: bytes) -> StrategyResult:
        if profile.primary_algorithm is None:
            return self._auto_select(profile.candidates, data)

        primary = self._compress_with_algorithm(profile.primary_algorithm, data)
        # Preset-first heuristic with honest STORE fallback.
        if len(primary.payload) < len(data):
            return StrategyResult(
                algorithm_id=profile.primary_algorithm,
                payload=primary.payload,
                codec_metadata=primary.metadata,
                candidate_sizes=[(profile.primary_algorithm, len(primary.payload)), (0, len(data))],
            )

        store = self._compress_with_algorithm(0, data)
        return StrategyResult(
            algorithm_id=0,
            payload=store.payload,
            codec_metadata=store.metadata,
            candidate_sizes=[(profile.primary_algorithm, len(primary.payload)), (0, len(store.payload))],
        )

    def _auto_select(self, candidates: tuple[int, ...], data: bytes) -> StrategyResult:
        results: list[tuple[int, bytes, dict, int]] = []
        candidate_sizes: list[tuple[int, int]] = []
        for algorithm_id in candidates:
            try:
                compressed = self._compress_with_algorithm(algorithm_id, data)
                out = self._decompress_with_algorithm(algorithm_id, compressed.payload, compressed.metadata, len(data))
                if out != data:
                    continue
                size = len(compressed.payload)
                candidate_sizes.append((algorithm_id, size))
                results.append((algorithm_id, compressed.payload, compressed.metadata, size))
            except Exception:
                continue

        if not results:
            store = self._compress_with_algorithm(0, data)
            return StrategyResult(algorithm_id=0, payload=store.payload, codec_metadata=store.metadata, candidate_sizes=[(0, len(data))])

        best = min(results, key=lambda item: (item[3], candidates.index(item[0])))
        return StrategyResult(
            algorithm_id=best[0],
            payload=best[1],
            codec_metadata=best[2],
            candidate_sizes=candidate_sizes,
        )

    @staticmethod
    def _compress_with_algorithm(algorithm_id: int, data: bytes):
        codec = create_codec(algorithm_id)
        return codec.compress(data)

    @staticmethod
    def _decompress_with_algorithm(algorithm_id: int, payload: bytes, metadata: dict, original_size: int) -> bytes:
        codec = create_codec(algorithm_id)
        return codec.decompress(payload, metadata, original_size)


def algorithm_label(algorithm_id: int) -> str:
    return ALGORITHM_NAMES.get(algorithm_id, f"ALG-{algorithm_id}")
