from typing import List

from linguoos.schemas.precision import ErrorType, PrecisionModule

MODULES: List[PrecisionModule] = [
    PrecisionModule(
        module_id="precision.generalization",
        name="Generalization",
        description="Over-broad claims without limits.",
        error_type=ErrorType.generalization,
    ),
    PrecisionModule(
        module_id="precision.unverifiable",
        name="Unverifiable Claims",
        description="Statements that cannot be proven.",
        error_type=ErrorType.unverifiable,
    ),
    PrecisionModule(
        module_id="precision.scope_mismatch",
        name="Scope Mismatch",
        description="Claim scope does not match evidence.",
        error_type=ErrorType.scope_mismatch,
    ),
    PrecisionModule(
        module_id="precision.causal_overreach",
        name="Causal Overreach",
        description="Causality claimed without basis.",
        error_type=ErrorType.causal_overreach,
    ),
    PrecisionModule(
        module_id="precision.vague_modifiers",
        name="Vague Modifiers",
        description="Adverbs/adjectives that are not measurable.",
        error_type=ErrorType.vague_modifiers,
    ),
]
